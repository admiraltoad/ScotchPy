"""
    Unpack Files
"""
import os, sys, shutil, errno

from ScotchPy import application as app
from ScotchPy.utils import folder_utils, file_utils

def get_root_directory():
    """ Return the calling directory. """
    return os.path.abspath(".") + "\\"

def get_folders_desc(search_directory):
	""" Get a list of folders under [search_directory] in descending order (lowest ot highest). """
	lowest_dirs = list()
	for root, directories, filenames in os.walk(search_directory):		
		if os.path.normpath(root.lower()) != os.path.normpath(search_directory.lower()): 
			lowest_dirs.append(root)
	return reversed(lowest_dirs)

def remove_empty_folders(search_directory):
	""" Remove folders under [search_directory] if empty. """
	for folder in get_folders_desc(search_directory):
		folder_utils.remove_if_empty(folder)

def unpackfiles(search_directory):
	""" Move all files in subdirectories under [search_directory] to root.  """
	for root, directories, filenames in os.walk(search_directory):
		for filename in filenames:
			source_filename = os.path.join(root, filename)
			if os.path.isfile(source_filename):
				destination = os.path.join(search_directory, filename)
				file_utils.move_file(source_filename, destination)		
	remove_empty_folders(search_directory)

if __name__ == "__main__":   					
    app.print_header("Unpack Files")
    unpackfiles(get_root_directory())
    sys.exit(0)