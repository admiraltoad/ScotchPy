"""
    Folder Utilities
    
"""
import os

def remove_if_empty(folder_path):
    """ Remove [folder_path] if the folder is empty. """
    if os.path.isdir(folder_path) and not os.listdir(folder_path):
        os.rmdir(folder_path)
        print("[-] removed '{0}'".format(folder_path))