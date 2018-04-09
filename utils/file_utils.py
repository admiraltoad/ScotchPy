"""
    File Utilities
    
"""
import os, shutil, filecmp

from ScotchPy import application as app

def move_file(source, destination):
    """ Move file from [source] to [destination] """ 
    try:
        if os.path.normpath(source.lower()) != os.path.normpath(destination.lower()): 
            if not os.path.exists(destination):                                
                shutil.move(source, destination)
                print(">> moved '{0}'".format(destination))
            else: 
                if filecmp.cmp(source, destination):
                    os.remove(source)
                    print("[-] removed '{0}'".format(source))
                else:
                    if app.query_yes_no("'{0}' already exists at target location '{1}' \n Do you want to delete this file??".format(source, destination)):
                        os.remove(source)
                        print("[-] removed '{0}'".format(source))                            
    except Exception as ex:
        print("!! error processing '{0}'.\n{1}".format(source, str(ex)))     

def rename_file(source, destination):
    """ Report and rename [source] file to [destination]. """
    if not os.path.isfile(destination):
        print(" << " + source)
        print(" >> " + destination)                     
        os.rename(source, destination) 

def rreplace(string, replace_this, with_this, repeat=1):
    """ Reverse replace. Replace starting from the last instance. """
    li = string.rsplit(replace_this, repeat)
    return with_this.join(li)