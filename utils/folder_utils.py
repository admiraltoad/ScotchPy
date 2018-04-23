"""
    Folder Utilities
    
"""
import os

def remove_if_empty(folder_path):
    """ Remove [folder_path] if the folder is empty. """
    if os.path.isdir(folder_path) and not os.listdir(folder_path):
        os.rmdir(folder_path)
        print("[-] removed '{0}'".format(folder_path))

def get_folders_desc(self, search_directory):
    """ Get a list of folders under [search_directory] in descending order (lowest ot highest). """
    lowest_dirs = list()
    for root, directories, filenames in os.walk(search_directory):		
        if os.path.normpath(root.lower()) != os.path.normpath(search_directory.lower()): 
            lowest_dirs.append(root)
    return reversed(lowest_dirs)