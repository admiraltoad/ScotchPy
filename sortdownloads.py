"""
    Sort Downloads
"""
from pymedia import television as tv
import pyapp
import os, string, shutil, sys, errno, time, filecmp 

def get_root_directory():
    return os.path.abspath('.') + '\\'

def get_tvshow_path():
    destination = pyapp.get_config_value('sortdownloads')
    if destination is None:
        raise Exception("Definition for <sortdownloads> is missing from config.xml")
    else:
        return destination.text

def sortdownloads(root_directory, tvshow_destination):    
    ## search for video files in the calling (root) directory   
    for root, directories, filenames in os.walk(root_directory):
        for directory in directories:
            sortdownloads(os.path.join(root_directory, directory), tvshow_destination) 
            
        for filename in filenames:
            filepath = os.path.join(root_directory, filename)
            if os.path.isfile(filepath):
                if tv.getFileExtension(filename) in ('avi','mkv','mp4', 'mpg'):
                    ## If its a video file, attempt to format it as a tv show
                    episodeObj = tv.processFilename(filename)   
                    if episodeObj != None:
                        source = filepath
                        new_filename = episodeObj.getFilename() 
                        tvshow_path = os.path.join(tvshow_destination, episodeObj.getName(), "Season " + episodeObj.getSeason())
                        destination = os.path.join(tvshow_path, new_filename)                         
                        if os.path.normpath(destination.lower()) != os.path.normpath(source.lower()):                         
                            if not os.path.exists(destination):
                                try:
                                    if not os.path.isdir(tvshow_path):
                                        os.makedirs(tvshow_path)                                    
                                    shutil.move(source, destination)
                                    print("# moved: " + destination)
                                except:
                                    print("!! error processing: " + source)
                            else: 
                                if filecmp.cmp(source, destination):
                                    os.remove(source)
                                    print("[-] removed: " + source)  
                                else:
                                    if pyapp.query_yes_no("'{}' already exists at target location '{}' \n Do you want to delete this file??".format(source, destination)):
                                        os.remove(source)
                                        print("[-] removed: " + source)  

if __name__ == "__main__":
    pyapp.print_header("Sort Downloads")   
    sortdownloads(get_root_directory(), get_tvshow_path())
    sys.exit(0)