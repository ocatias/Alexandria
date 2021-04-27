import os

def get_folder_structure_from_url(url):
    return '/'.join(url.split('/')[2:len(url.split('/'))-1]) + '/'

def get_path_filename(url, archive_folder):
    folder_structure = get_folder_structure_from_url(url)
    path =  os.path.join(archive_folder, folder_structure)

    if not os.path.exists(path):
        os.makedirs(path)

    last_element_of_url = url.split('/')[-1]
    if last_element_of_url == '':
        last_element_of_url = 'index'

    file_name = os.path.join(path, last_element_of_url) + ".page"


    return path, file_name
