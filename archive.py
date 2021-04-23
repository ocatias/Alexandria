import os
import urllib
import urllib.request
import re

url_file = "urls.txt"


archive_folder = 'archive'

if __name__ == "__main__":

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
            if file_exists:
                with open(file_name, 'rb') as file:
                    if response.read()== file.read():
                        print("\tNo changes")
                        continue
                    else:
                        print("\tDifferences found")
            with open(file_name, 'w+b') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)
