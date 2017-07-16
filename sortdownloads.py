"""
    Sort Downloads
"""
from pymedia import television as tv
import pyapp
import os, string, shutil, sys, errno, time, filecmp 

## Global Members
m_tvshowsDirectory = r'F:\_TVShows'
m_rootDirectory = os.path.abspath('.') + '\\'

def debug(message): 
    bDebug = False
    if bDebug:
        print(message)

def main(rootDir):
    ## search for video files in the calling (root) directory   
    for root, directories, filenames in os.walk(rootDir):
        for directory in directories:
            main(os.path.join(rootDir, directory)) 
            
        for filename in filenames:
            filepath = os.path.join(rootDir, filename)
            if os.path.isfile(filepath):
                if tv.getFileExtension(filename) in ('avi','mkv','mp4', 'mpg'):
                    ## If its a video file, attempt to format it as a tv show
                    episodeObj = tv.processFilename(filename)   
                    if episodeObj != None:
                        debug("Processing ["+filename+"] ...")
                        source = filepath
                        new_filename = episodeObj.getFilename() 
                        tvshow_path = os.path.join(m_tvshowsDirectory,episodeObj.getName(),"Season " + episodeObj.getSeason())
                        destination = os.path.join(tvshow_path, new_filename) 
                        debug("[#][01]: "+source.lower()+", "+destination.lower())                        
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
                                debug("[#][02]: "+source.lower()+", "+destination.lower())  
                                if filecmp.cmp(source, destination):
                                    os.remove(source)
                                    print("[-] removed: " + source)  
                                else:
                                    if pyapp.query_yes_no("'{}' already exists at target location '{}' \n Do you want to delete this file??".format(source, destination)):
                                        os.remove(source)
                                        print("[-] removed: " + source)  

pyapp.print_header("Sort Downloads", 1, 0)
main(m_rootDirectory)
sys.exit(0)