import os, sys
import urllib
import urllib.request
import re
import smtplib, ssl
from email.mime.text import MIMEText
from datetime import datetime

url_file = "urls.txt"
config_file = "config.hide"

pages_in_archive = 0

archive_folder = 'archive'

def get_credentials():
    """
    Loads credentials from configfile
    Returns email, password, your_email
    """
    with open(config_file, "r") as file:
        lines = file.read().split('\n')
        email = lines[0].split('=')[1].replace(" ", "")
        pwd = lines[1].split('=')[1].replace(" ", "")
        your_email = lines[2].split('=')[1].replace(" ", "")

    return email, pwd, your_email

def send_email(message):
    """
    Sends email message from and to the addresses specified in the config file
    """
    port = 465  # For SSL

    email_from, pwd, email_to = get_credentials()

    msg = MIMEText(message)
    msg['Subject'] = 'Alexandria Status Report'
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Date'] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_from, pwd)
        server.sendmail(email_from, email_to, msg.as_string())

    print("Sent email to ", email_to)

def update_archive():
    """Check if any of the pages specified in the url_file have changed.
    Return the pages that have changed and the newly archived pages
    returns (changed_pages, newly_archived_pages)"""

    changed_pages = []
    newly_archived_pages = []

    # Get urls from file and remove empty lines
    f = open(url_file, "r")
    urls = f.read().split('\n')
    urls = filter(lambda x : x.replace(" ", "") != '', urls)

    for url in urls:
        folder_structure = '/'.join(url.split('/')[2:len(url.split('/'))-1])

        path =  os.path.join(archive_folder, folder_structure)

        if not os.path.exists(path):
            os.makedirs(path)

        last_element_of_url = url.split('/')[-1]
        if last_element_of_url == '':
            last_element_of_url = 'index'

        file_name = os.path.join(path, last_element_of_url)
        print(url)

        file_exists = False
        if os.path.exists(file_name):
            print('\tAlready exists')
            time = os.path.getmtime(file_name)
            file_exists = True

        with urllib.request.urlopen(url) as response:
            global pages_in_archive
            pages_in_archive += 1

            if file_exists:
                with open(file_name, 'rb') as file:
                    if response.read()== file.read():
                        print("\tNo changes")
                        continue
                    else:
                        print("\tDifferences found")
            with open(file_name, 'w+b') as out_file:
                data = response.read()
                out_file.write(data)
                if file_exists:
                    changed_pages.append(url)
                else:
                    newly_archived_pages.append(url)
                    print("\tNewly archived")

    return (changed_pages, newly_archived_pages)

def construct_email_message(changed_pages, newly_archived_pages):
    message = "Pages in archives: " + str(pages_in_archive) + "\n"
    message += "Newly scraped pages: " + str(len(newly_archived_pages)) + "\n"
    message += "Updated pages: " + str(len(changed_pages)) + "\n"
    message += "\n"

    if(len(newly_archived_pages) > 0):
        message += "\nThe following pages have been newly archived:\n"
        message += '\t' + '\n\t'.join(newly_archived_pages) + '\n\n'

    if(len(changed_pages) > 0):
        message += "\nThe following pages have changed since the last update:\n"
        message += '\t' +  '\n\t'.join(changed_pages) + '\n\n'

    return message

def main():
    check_initial_config()

    changed_pages, newly_archived_pages = update_archive()
    if len(changed_pages) + len(newly_archived_pages) == 0:
        return

    message = construct_email_message(changed_pages, newly_archived_pages)
    send_email(message)

def check_initial_config():
    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            print("Creating " + config_file)
            file.write(("email_throwaway = \n"
            "email_throwaway_password = \n"
            "your_email = "))

    if not os.path.exists(url_file):
        print("Creating " + url_file)
        open(url_file, 'a').close()

if __name__ == "__main__":
    os.chdir(sys.path[0])
    main()
