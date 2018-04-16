"""
    Sort Downloads
"""
import argparse
import os, string, shutil, sys, errno, time, filecmp

from ScotchPy.utils import media_utils, file_utils, folder_utils
from ScotchPy import config
from ScotchPy  import application as app

def get_arguments():    
    """ Define and return a list of command line arguments. """
    parser = argparse.ArgumentParser(description="Sort Downloads") 
    parser.add_argument(
        "--movies_only", 
        "-m", 
        required=False, 
        action="store_true",
        help="Search media files and sort only movie files."
        ) 
    parser.add_argument(
        "--tv_only", 
        "-t", 
        required=False, 
        action="store_true",
        help="Search media files and sort only tv episode files."
        ) 
    parser.add_argument(
        "--remove_title", 
        "-r", 
        required=False, 
        action="store_true",
        help="Removes the tvshow episode title when sorting downloads."
        )                
    parser.set_defaults(movies_only=False,tv_only=False,remove_title=False)
 
    return parser.parse_args(args=app.get_system_arguments())

def get_root_directory():
    """ Return the calling directory. """
    return os.path.abspath(".") + "\\"
    
def get_movie_path():
    """ Get the movies directory from the configuration file. """
    destination = config.get_value('movies')
    if destination is None:
        raise Exception("Definition for <movies> is missing from config.xml")
    else:
        return destination.text

def should_remove_file(filepath):
    """ """
    filename, extension = os.path.splitext(filepath)
    if extension.lower() in [".nfo"]:
        return True
    for item in media_utils.get_remove_files():
        if filepath.lower() == item.text.lower():
            return True
    return False

def get_tv_path():
    """ Get the tv show directory from the configuration file. """
    destination = config.get_value('tv')
    if destination is None:
        destination = config.get_value('sortdownloads')
        if destination is None:
            raise Exception("Definition for <tv> is missing from config.xml")
    else:
        return destination.text

def sort_movies(search_directory, movie_destination):    
    """ Move video files that match a given pattern from [search_directory] into [movie_destination].   """     
    if not os.path.isdir(movie_destination):
        os.makedirs(movie_destination)  

    for root, directories, filenames in os.walk(search_directory):
        for directory in directories:
            folder_utils.remove_if_empty(os.path.join(root, directory))  

        for filename in filenames:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                if should_remove_file(filename):
                    os.remove(filepath)
                else:
                    new_media = media_utils.create_media_file(movie_destination, filename)
                    if new_media.is_movie():                     
                        file_utils.move_file(filepath, new_media.get_full_path())                       
        
def sort_tv(search_directory, tvshow_destination, remove_title=False):    
    """ Move video files that match a given pattern from [search_directory] into [tvshow_destination].  """ 
    for root, directories, filenames in os.walk(search_directory):
        for directory in directories:
            folder_utils.remove_if_empty(os.path.join(root, directory))       
         
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):   
                if should_remove_file(filename):
                    os.remove(filepath)
                else:              
                    new_media = media_utils.create_media_file(tvshow_destination, filename, remove_title)
                    if new_media.is_tv():
                        if not os.path.isdir(new_media.get_destination()):
                            os.makedirs(new_media.get_destination())
                        current_path = new_media.get_destination()
                        for subdir in new_media.get_subdirectories():
                            current_path = os.path.join(current_path, subdir)
                            if not os.path.exists(current_path):
                                os.makedirs(current_path)                    
                        file_utils.move_file(filepath, new_media.get_full_path())  
                            
if __name__ == "__main__":
    try:
        app.print_header("Sort Downloads")   

        args = get_arguments()
        run_all = not args.tv_only and not args.movies_only
        if args.tv_only or run_all:
            sort_tv(get_root_directory(), get_tv_path(), args.remove_title)
        if args.movies_only or run_all:
            sort_movies(get_root_directory(), get_movie_path())
            
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        sys.exit(-1)