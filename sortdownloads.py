"""
    Sort Downloads
"""
from pymedia import television as tv
import pyapp
import os, string, shutil, sys, errno, time, filecmp 
import argparse

def get_root_directory():
    return os.path.abspath('.') + '\\'

def get_tvshow_path():
    destination = pyapp.get_config_value('sortdownloads')
    if destination is None:
        raise Exception("Definition for <sortdownloads> is missing from config.xml")
    else:
        return destination.text

def get_arguments():    
    ## Define command arguments
    parser = argparse.ArgumentParser(description="Sort Downloads") 
    parser.add_argument(
        "--trim_title", 
        "-t", 
        required=False, 
        action="store_true",
        help="Remove the tvshow episode title when sorting downloads."
        )                
    parser.set_defaults(trim_title=False)
 
    return parser.parse_args(args=pyapp.get_system_arguments())
       
def sortdownloads(search_directory, tvshow_destination, trim_title=False):    
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
                    new_filename = episode_obj.get_filename(trim_title)
                    tvshow_path = os.path.join(tvshow_destination, episode_obj.get_name(), "Season " + episode_obj.get_season())
                    destination = os.path.join(tvshow_path, new_filename)                         
                    if os.path.normpath(destination.lower()) != os.path.normpath(source.lower()):                         
                        if not os.path.exists(destination):
                            try:
                                if not os.path.isdir(tvshow_path):
                                    os.makedirs(tvshow_path)                                    
                                shutil.move(source, destination)
                                print(">> moved '{0}'".format(destination))
                            except Exception as ex:
                                raise Exception("!! error processing '{0}'.\n{1}".format(source, str(ex)))
                        else: 
                            if filecmp.cmp(source, destination):
                                os.remove(source)
                                print("[-] removed '{0}'".format(source))
                            else:
                                if pyapp.query_yes_no("'{}' already exists at target location '{}' \n Do you want to delete this file??".format(source, destination)):
                                    os.remove(source)
                                    print("[-] removed '{0}'".format(source))
        
        

if __name__ == "__main__":
    try:
        pyapp.print_header("Sort Downloads")   
        args = get_arguments()
        sortdownloads(get_root_directory(), get_tvshow_path(), args.trim_title)        
                
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        raise
        sys.exit(-1)