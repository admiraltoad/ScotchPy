"""
    Rename Files
"""
import os, string, shutil, sys, errno, re, datetime
from xml.etree import ElementTree as etree
import argparse

from ScotchPy.utils import media_utils, file_utils
import ScotchPy.application as app
  
def get_arguments():  
    """ Define and return a list of command line arguments. """
    arguments = app.get_system_arguments()
    if arguments is None:              
        return False, arguments
    elif len(arguments) == 2 and not str(arguments[0]).startswith("-") and not str(arguments[1]).startswith("-"):
        return False, arguments
    elif len(arguments) == 1 and not str(arguments[0]).startswith("-"):
        return False, arguments

    ## define command arguments
    parser = argparse.ArgumentParser(description="Rename Files") 
    parser.add_argument(
        "--replace_this", 
        "-r", 
        required=False, 
        help="Replace this string."
        )
    parser.add_argument(
        "--with_this", 
        "-w", 
        required=False, 
        help="With this string."
        )
    parser.add_argument(
        "--regular_expression", 
        "-re", 
        required=False, 
        action="store_true",
        help="Use regular expression with [--replace_this/-r] string."
        ) 
    parser.add_argument(
        "--repeat", 
        "-c", 
        required=False, 
        type=int, 
        help="Repeat this many times."
        )
    parser.add_argument(
        "--recursive", 
        "-v", 
        required=False, 
        action="store_true",
        help="Replace in calling directory recursively."
        )        
    parser.add_argument(
        "--starts_with", 
        "-s", 
        required=False, 
        action="store_true",
        help="Replace if the filename starts with [--replace_this/-r] string."
        )
    parser.add_argument(
        "--ends_with", 
        "-e", 
        required=False, 
        action="store_true",
        help="Replace if the filename ends with [--replace_this/-r] string."
        )   
    parser.add_argument(
        "--preset", 
        "-p", 
        required=False,
        action="store_true",
        help="Run the preset formatting for files. Must be the first given argument."
        )           
    parser.set_defaults(replace_this=None, with_this="", regular_expression=False, repeat=0, recursive=False, starts_with=False, ends_with=False, preset=False)

    ## Process system arguments    
    command_arguments = parser.parse_args(args=arguments)
    
    ## Error Handling
    if command_arguments.preset == False and command_arguments.replace_this is None:
        raise Exception("Argument [--replace_this] is required.")
    if command_arguments.repeat < 0:
        raise Exception("Arguemnt [--repeat] must be a positive integer.")   
    
    ## Defaults argument values
    if command_arguments.repeat == 0:
        command_arguments.repeat = 1
    
    return True, command_arguments
        
def get_root_directory():
    """ Return the calling directory. """
    return os.path.abspath(".") + "\\"

def rename_filename(filename, replace_this, with_this="", repeat=1, starts_with=False, ends_with=False):
    """ [replace_this] [with_this] in the filename. """
    newfile_name = filename
    if starts_with == True:
        if newfile_name.startswith(replace_this):
            newfile_name = newfile_name.replace(replace_this, with_this, repeat)
    elif ends_with == True:
        if newfile_name.endswith(replace_this):
            newfile_name = file_utils.rreplace(newfile_name, replace_this, with_this, repeat)
    else:
        newfile_name = newfile_name.replace(replace_this, with_this, repeat)
    newfile_name = newfile_name.strip()    
    return newfile_name
    
def rename_filename_from_list(filename, replace_list, with_this="", repeat=1, starts_with=False, ends_with=False, regular_expression=False):
    """ Rename file using given parameters. """ 
    newfile_name = filename
    for replace_this in replace_list:
        if regular_expression:   
            match = re.search(replace_this, newfile_name)                
            if match is not None:                   
                replace_this = match.group()
            else:
                replace_this = None
                
        if replace_this is not None:
            newfile_name = rename_filename(newfile_name, replace_this, with_this, repeat, starts_with, ends_with)
    return newfile_name

def rename_files_in_dir(search_directory, replace_list, with_this="", repeat=1, recursive=False, starts_with=False, ends_with=False, regular_expression=False, media_only=False):
    """ Rename files in the given search_directory. """ 
    for root, directories, filenames in os.walk(search_directory):
        if recursive:
            for directory in directories:
                subdirectory = os.path.join(search_directory, directory)
                if os.path.isdir(subdirectory):
                    rename_files_in_dir(subdirectory, replace_list, with_this, repeat, recursive, starts_with, ends_with) 
                
        for filename in filenames:
            file_fullpath = os.path.join(search_directory, filename)
            if os.path.isfile(file_fullpath): 
                newfile_name, extension = os.path.splitext(filename)
                if media_only:
                    if media_utils.is_media_file(filename):
                        newfile_name = rename_filename_from_list(newfile_name, replace_list, with_this, repeat, starts_with, ends_with)
                else:
                    newfile_name = rename_filename_from_list(newfile_name, replace_list, with_this, repeat, starts_with, ends_with)
                newfile_name = newfile_name + extension 

                ## if the name has changed, report and rename it
                if newfile_name != filename:
                    newfile_fullpath = os.path.join(search_directory, newfile_name)
                    file_utils.rename_file(file_fullpath, newfile_fullpath)

def process_no_arguments(search_directory, arguments):
    """ Process filenames when no arguments (--item/-i) are given. """
    if arguments is not None:
        if len(arguments) == 2:
            rename_files_in_dir(search_directory,[str(arguments[0])],str(arguments[1]))
        elif len(arguments) == 1:
            rename_files_in_dir(search_directory,[str(arguments[0])])

def process_presets(search_directory, recursive=False):
    """ Process filenames using the given list of preset rules. """ 
    now = datetime.datetime.now()
    for root, directories, filenames in os.walk(search_directory):
        if recursive:
            for directory in directories:
                subdirectory = os.path.join(search_directory, directory)
                if os.path.isdir(subdirectory):
                    process_presets(subdirectory, recursive) 
                    
        for filename in filenames:
            file_fullpath = os.path.join(search_directory, filename)
            if os.path.isfile(file_fullpath): 
                if media_utils.is_media_file(filename):    
                    newfile_name, extension = os.path.splitext(filename)

                    replace_list = []
                    newfile_name = rename_filename(newfile_name, ".", " ", 1024)
                    
                    ## remove all preset xml enteries from filename                    
                    filepath = os.path.dirname(os.path.realpath(__file__))
                    preset_xml = os.path.join(filepath, "..", "data", "renamefiles.preset.xml")
                    if not os.path.isfile(preset_xml):
                        raise Exception("Missing preset XML file [{0}]".format(preset_xml))
                    tree = etree.parse(preset_xml)
                    root = tree.getroot()                                        
                    for item in root.iter("item"):        
                        replace_list.append(item.text)
                    replace_list.append("  1")
                    
                    newfile_name = rename_filename_from_list(newfile_name, replace_list)
                    newfile_name = newfile_name + extension 

                    ## if the name has changed, report and rename it
                    if newfile_name != filename:
                        newfile_fullpath = os.path.join(search_directory, newfile_name)
                        file_utils.rename_file(file_fullpath, newfile_fullpath)

def check_preset():
    """ Return True if the first commandline argument is --preset or -p """
    system_arguments = app.get_system_arguments()  
    if len(system_arguments) > 0:
        if system_arguments[0] == "--preset" or system_arguments[0] == "-p":
            return True
    return False

if __name__ == "__main__":   
    try:
        app.print_header("Rename Files")
        
        check, args = get_arguments()
        if check == False:
            process_no_arguments(get_root_directory(), args)
        elif check_preset():
            process_presets(get_root_directory(), args.recursive)
        else:
            print("repeat={0}, recursive={1}, starts_wth={2}, ends_with={3}, regex={4}".format(args.repeat, args.recursive, args.starts_with, args.ends_with, args.regular_expression))
            if app.query_yes_no("Replace '{0}' with '{1}'?".format(args.replace_this, args.with_this)):
                replace_list = [args.replace_this]               
                rename_files_in_dir(get_root_directory(), replace_list, args.with_this, args.repeat, args.recursive, args.starts_with, args.ends_with, args.regular_expression)            
                
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")       
        sys.exit(-1)    