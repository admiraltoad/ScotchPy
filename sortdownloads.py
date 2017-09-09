"""
    Sort Downloads
"""
from pymedia import television as media
import pyapp
import os, string, shutil, sys, errno, time, filecmp

def get_root_directory():
    return os.path.abspath('.') + '\\'
    
def get_arguments():    
    ## Define command arguments
    parser = argparse.ArgumentParser(description="Sort Downloads") 
    parser.add_argument(
        "--movies", 
        "-m", 
        required=False, 
        action="store_true",
        help="Search media files and sort movie files."
        ) 
    parser.add_argument(
        "--tv", 
        "", 
        required=False, 
        action="store_true",
        help="Search media files and sort tv episode files."
        ) 
    parser.add_argument(
        "--keep_title", 
        "-k", 
        required=False, 
        action="store_true",
        help="Keep the tvshow episode title when sorting downloads."
        )                
    parser.set_defaults(movies=True,tv=True,keep_title=False)
 
    return parser.parse_args(args=pyapp.get_system_arguments())
    
def get_movie_path():
    destination = pyapp.get_config_value('movies')
    if destination is None:
        raise Exception("Definition for <movies> is missing from config.xml")
    else:
        return destination.text
        
def get_tv_path():
    destination = pyapp.get_config_value('tv')
    if destination is None:
        destination = pyapp.get_config_value('sortdownloads')
        if destination is None:
            raise Exception("Definition for <tv> is missing from config.xml")
    else:
        return destination.text
        
def sort_movies(search_directory, movie_path):    
    ''' Move video files in search_directory recursively into movie_path. 
        Ignore video files that appear to be tv episodes.
    '''  
    for root, directories, filenames in os.walk(search_directory):
        for directory in directories:
            subdirectory = os.path.join(search_directory, directory)
            if os.path.isdir(subdirectory):
                sortdownloads(subdirectory, tvshow_destination)
                if not os.listdir(subdirectory):
                    os.rmdir(subdirectory)            
            
        for filename in filenames:
            filepath = os.path.join(search_directory, filename)
            if os.path.isfile(filepath):                
                ## If its a video file, attempt to format it as a tv show
                episode_obj = media.process_filename(filename)  
                
                if episode_obj is None and media.is_media_file(filename):
                    source = filepath
                    destination = os.path.join(movie_path, filename)                       
                    if os.path.normpath(source.lower()) != os.path.normpath(destination.lower()):   
                        try:
                            if not os.path.exists(destination):   
                                if not os.path.isdir(movie_path):
                                    os.makedirs(movie_path)                                    
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
        
def sort_tv(search_directory, tvshow_destination, keep_title=False):    
    ## search for video files in the calling (root) directory   
    for root, directories, filenames in os.walk(search_directory):
        for directory in directories:
            subdirectory = os.path.join(search_directory, directory)
            if os.path.isdir(subdirectory):
                sortdownloads(subdirectory, tvshow_destination)
                if not os.listdir(subdirectory):
                    os.rmdir(subdirectory)            
            
        for filename in filenames:
            filepath = os.path.join(search_directory, filename)
            if os.path.isfile(filepath):                
                ## If its a video file, attempt to format it as a tv show
                episode_obj = tv.process_filename(filename)  
                
                if episode_obj is not None:
                    source = filepath
                    new_filename = episode_obj.get_filename(keep_title)
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
        
        if args.tv:
            sort_tv(get_root_directory(), get_tv_path(), args.keep_title)
        if args.movies:
            sort_movies(get_root_directory(), get_movie_path())
        
        sort_movies(get_root_directory(), get_movie_path())        
                
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        raise
        sys.exit(-1)