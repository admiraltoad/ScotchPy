"""
    File Utilities
    
"""
import os, shutil, filecmp
import xml.etree.ElementTree as etree

from ScotchPy import application as app

def remove_file(filepath):
    os.remove(filepath)
    print("[-] removed '{0}'".format(filepath))

def move_file(source, destination):
    """ Move file from [source] to [destination] """ 
    try:
        if os.path.normpath(source.lower()) != os.path.normpath(destination.lower()): 
            if not os.path.exists(destination):                                
                shutil.move(source, destination)
                print("[>] moved '{0}'".format(destination))
            else: 
                if filecmp.cmp(source, destination):
                    remove_file(source)
                else:
                    if app.query_yes_no("\n\n'{0}' already exists at target location '{1}' \n Do you want to delete this file??".format(source, destination)):
                        remove_file(source)                        
    except Exception as ex:
        raise Exception("[!] Error Processing: '{0}'.\n{1}".format(source, str(ex)))     

def rename_file(source, destination):
    """ Report and rename [source] file to [destination]. """
    if not os.path.isfile(destination):
        print("[-] '{0}'".format(source))
        print("[+] '{0}'".format(destination))                     
        os.rename(source, destination) 

def rreplace(string, replace_this, with_this, repeat=1):
    """ Reverse replace. Replace starting from the last instance. """
    li = string.rsplit(replace_this, repeat)
    return with_this.join(li)

def get_remove_files():
    """ Returns remove file items from xml. """
    filepath = os.path.dirname(os.path.realpath(__file__))
    tvshow_match_xml = os.path.join(filepath, "..", "data", "removefiles.xml")
    if not os.path.isfile(tvshow_match_xml):
        raise Exception("[!] Missing match XML file '{0}'".format(tvshow_match_xml))
    tree = etree.parse(tvshow_match_xml)
    root = tree.getroot() 
    return root.iter("file")

def get_remove_extensions():
    """ Returns remove file items from xml. """
    filepath = os.path.dirname(os.path.realpath(__file__))
    tvshow_match_xml = os.path.join(filepath, "..", "data", "removefiles.xml")
    if not os.path.isfile(tvshow_match_xml):
        raise Exception("[!] Missing match XML file '{0}'".format(tvshow_match_xml))
    tree = etree.parse(tvshow_match_xml)
    root = tree.getroot() 
    return root.iter("ext")

def remove_useless_files(search_directory):
    """ """
    for _, _, filenames in os.walk(search_directory):   
        for filename in filenames:
            current_file = os.path.join(search_directory, filename)
            if os.path.isfile(current_file):
                _, extension = os.path.splitext(filename)
                for r_ext in get_remove_extensions():
                    if r_ext.text.lower() == extension.lower():
                        remove_file(current_file)
                else:
                    for r_file in get_remove_files():
                        if r_file.text.lower() == filename.lower():
                            remove_file(current_file)