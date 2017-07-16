"""
    Clean-up Folders
"""
import pyapp
import os, string, shutil, sys, errno 

## Global Members
m_rootDirectory = os.path.abspath('.') + '\\'

def cleanupFolders(rootdir):
    for dirpath, dirs, files in os.walk(rootdir):
        if not dirs:
            if len(files) == 1:
                for file in files:
                    currentFile = os.path.join(dirpath, file)
                    if os.path.isfile(currentFile):
                        shutil.move(currentFile, os.path.join(dirpath, '..', file))
            else:
                for file in files:
                    currentFile = os.path.join(dirpath, file)
                    if os.path.isfile(currentFile) and file.lower() in ('rarbg.txt'):
                        os.remove(currentFile)  
                        
def findEmptyDirs(rootdir):
    for dirpath, dirs, files in os.walk(rootdir):
        if not dirs and not files:
            yield dirpath            
            
def main(rootpath):
    cleanupFolders(rootpath)
    for i in range(3):        
        emptyFolders = set(findEmptyDirs(rootpath)) 
        for folder in emptyFolders:
            print(".. Removing [",folder,"]")
            os.rmdir(folder)

pyapp.print_header("Clean-up Folders", 1, 0)
main(m_rootDirectory)
sys.exit(0)