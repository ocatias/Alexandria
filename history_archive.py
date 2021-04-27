import sqlite3
import archive_helpers as helpers
import os, sys
import urllib.request

config_file = "config.hide"

#[('moz_origins',), ('moz_places',), ('moz_historyvisits',), (
#'moz_inputhistory',), ('moz_bookmarks',), ('moz_bookmarks_deleted',),
#('moz_keywords',), ('sqlite_sequence',), ('moz_anno_attributes',),
#('moz_annos',), ('moz_items_annos',), ('moz_meta',), ('sqlite_stat1',)]

archive_folder = "archive_history"

def main():
    with open(config_file, "r") as file:
        lines = file.read().split('\n')
        path_db = [line for line in lines if 'firefox_user_folder' in line][0]
        path_db = path_db.split('=')[1].replace(' ', '')
        path_db = os.path.join(path_db, "places_demo.sqlite")

    print(path_db)
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    # data = cur.execute("PRAGMA table_info(moz_places);")
    data = cur.execute("SELECT url from moz_places;")
    #print(len(data))
    amount = 0
    for row in data:
        amount += 1
        url = row[0]

        if url[-1] == '/':
            url = url[0:len(url) -1]

        path, file_name = helpers.get_path_filename(url, archive_folder)

        print(url)
        if os.path.exists(file_name):
            print("\tAlready exists")
            continue

        try:
            with urllib.request.urlopen(url) as response:
                with open(file_name, 'w+b') as out_file:
                    data = response.read()
                    out_file.write(data)
        except:
            print("\tcould not load site")

if __name__ == "__main__":
    os.chdir(sys.path[0])
    main()
