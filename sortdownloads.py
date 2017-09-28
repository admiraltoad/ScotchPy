"""
    Sort Downloads
"""
from pymedia import television as media
import pyapp, renamefiles
import argparse
import os, string, shutil, sys, errno, time, filecmp
   
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
 
    return parser.parse_args(args=pyapp.get_system_arguments())

def get_root_directory():
    """ Return the calling directory. """
    return os.path.abspath(".") + "\\"
    
def get_movie_path():
    """ Get the movies directory from the configuration file. """
    destination = pyapp.get_config_value('movies')
    if destination is None:
        raise Exception("Definition for <movies> is missing from config.xml")
    else:
        return destination.text
        
def get_tv_path():
    """ Get the tv show directory from the configuration file. """
    destination = pyapp.get_config_value('tv')
    if destination is None:
        destination = pyapp.get_config_value('sortdownloads')
        if destination is None:
            raise Exception("Definition for <tv> is missing from config.xml")
    else:
        return destination.text
        
def sort_movies(search_directory, movie_destination):    
    ''' Move video files that match a given pattern from [search_directory] into [movie_destination].   '''  
    renamefiles.process_presets(search_directory)
    
    for root, directories, filenames in os.walk(search_directory):
        for directory in directories:
            subdirectory = os.path.join(search_directory, directory)
            if os.path.isdir(subdirectory):
                sort_movies(subdirectory, movie_destination)
                if not os.listdir(subdirectory):
                    os.rmdir(subdirectory)            
            
        for filename in filenames:
            filepath = os.path.join(search_directory, filename)
            if os.path.isfile(filepath):
                if media.is_movie_file(filename):
                    source = filepath
                    destination = os.path.join(movie_destination, filename)                       
                    if os.path.normpath(source.lower()) != os.path.normpath(destination.lower()):   
                        try:
                            if not os.path.exists(destination):   
                                if not os.path.isdir(movie_destination):
                                    os.makedirs(movie_destination)                                    
                                shutil.move(source, destination)
                            else: 
                                if filecmp.cmp(source, destination):
                                    os.remove(source)
                                    print("[-] removed '{0}'".format(source))
                                else:
                                    if pyapp.query_yes_no("'{0}' already exists at target location '{1}' \n Do you want to delete this file??".format(source, destination)):
                                        os.remove(source)
                                        print("[-] removed '{0}'".format(source))
                            print(">> moved '{0}'".format(destination))
                        except Exception as ex:
                            print("!! error processing '{0}'.\n{1}".format(source, str(ex)))       
        
def sort_tv(search_directory, tvshow_destination, remove_title=False):    
    ''' Move video files that match a given pattern from [search_directory] into [tvshow_destination].  ''' 
    for root, directories, filenames in os.walk(search_directory):
        for directory in directories:
            subdirectory = os.path.join(search_directory, directory)
            if os.path.isdir(subdirectory):
                sort_tv(subdirectory, tvshow_destination)
                if not os.listdir(subdirectory):
                    os.rmdir(subdirectory)            
            
        for filename in filenames:
            filepath = os.path.join(search_directory, filename)
            if os.path.isfile(filepath):                
                ## If its a video file, attempt to format it as a tv show
                episode_obj = media.process_filename(filename)  
                
                if episode_obj is not None:
                    source = filepath
                    new_filename = episode_obj.get_filename(remove_title)
                    tvshow_path = os.path.join(tvshow_destination, episode_obj.get_name(), "Season " + episode_obj.get_season())
                    destination = os.path.join(tvshow_path, new_filename)                         
                    if os.path.normpath(destination.lower()) != os.path.normpath(source.lower()):   
                        try:
                            if not os.path.exists(destination):   
                                if not os.path.isdir(tvshow_path):
                                    os.makedirs(tvshow_path)                                    
                                shutil.move(source, destination)
                            else: 
                                if filecmp.cmp(source, destination):
                                    os.remove(source)
                                    print("[-] removed '{0}'".format(source))
                                else:
                                    if pyapp.query_yes_no("'{0}' already exists at target location '{1}' \n Do you want to delete this file??".format(source, destination)):
                                        os.remove(source)
                                        print("[-] removed '{0}'".format(source))
                            print(">> moved '{0}'".format(destination))
                        except Exception as ex:
                            print("!! error processing '{0}'.\n{1}".format(source, str(ex)))   
                            
if __name__ == "__main__":
    try:
        pyapp.print_header("Sort Downloads")   
        args = get_arguments()
        
        if args.tv_only:
            sort_tv(get_root_directory(), get_tv_path(), args.remove_title)
        if args.movies_only:
            sort_movies(get_root_directory(), get_movie_path())    
        else:
            sort_tv(get_root_directory(), get_tv_path(), args.remove_title)
            sort_movies(get_root_directory(), get_movie_path()) 
            
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        raise
        sys.exit(-1)