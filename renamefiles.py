"""
    Rename Files
"""
from pymedia import television as pymedia
import pyapp
import os, string, shutil, sys, errno, re, datetime
from xml.etree import ElementTree as etree
import argparse

def get_root_directory():
    return os.path.abspath(".") + "\\"
    
def process_presets(search_directory):
    """ Rename files in the given search_directory. """ 
    now = datetime.datetime.now()
    for root, directories, filenames in os.walk(search_directory):                
        for filename in filenames:
            file_fullpath = os.path.join(search_directory, filename)
            if os.path.isfile(file_fullpath): 
                if pymedia.is_media_file(filename):
                
                    replace_list = []
                    filename = rename(filename, ".", " ", 1024)
                    
                    ## remove all preset xml enteries from filename                    
                    filepath = os.path.dirname(os.path.realpath(__file__))
                    tree = etree.parse(os.path.join(filepath, "renamefiles.preset.xml"))
                    root = tree.getroot()                                        
                    for item in root.iter("item"):        
                        replace_list.append(item.text)
                    replace_list.append("  1")  
                    
                    newfile_name = rename(filename, replace_list)
                    
                    ## wrap movie year with brackets "(1999)"
                    match = re.search("\s\d+", newfile_name)
                    if match is not None:    
                        year = match.group()
                        if int(year) > 1965 and int(year) <= now.year:                            
                            newfile_name = newfile_name.replace(year, " ({0})".format(year.strip()))
                    
                    ## if the name has changed, report and rename it
                    if newfile_name != filename:
                        print(" << " + os.path.join(search_directory, filename))
                        print(" >> " + os.path.join(search_directory, newfile_name))                     
                        newfile_fullpath = os.path.join(search_directory, newfile_name)
                        os.rename(file_fullpath, newfile_fullpath) 
 
        
def check_preset():
    system_arguments = pyapp.get_system_arguments()  
    if len(system_arguments) > 0:
        if system_arguments[0] == "--preset" or system_arguments[0] == "-p":
            return True
    return False   

def get_arguments():    
    ## Define command arguments
    parser = argparse.ArgumentParser(description="Rename Files") 
    parser.add_argument(
        "--replace_this", 
        "-r", 
        required=True, 
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
        help="Run the preset formatting for files. Must be the first given argument."
        )           
    parser.set_defaults(replace_this=None, with_this=None, regular_expression=False, repeat=0, recursive=False, starts_with=False, ends_with=False)

    ## Process system arguments    
    command_arguments = parser.parse_args(args=pyapp.get_system_arguments())
    
    ## Error Handling
    if command_arguments.repeat < 0:
         raise Exception("Arguemnt [--repeat] must be a positive integer.")   
    
    ## Defaults argument values
    if command_arguments.repeat == 0:
        command_arguments.repeat = 1
    
    return command_arguments

def rreplace(string, replace_this, with_this, repeat=1):
    li = string.rsplit(replace_this, repeat)
    return with_this.join(li)

def rename(filename, replace_list, with_this="", repeat=1, starts_with=False, ends_with=False, regular_expression=False):
    """ Rename file using given parameters. """ 
    newfile_name = filename

    for replace_this in replace_list:
        if regular_expression:   
            match = re.search(replace_this, filename)                
            if match is not None:                   
                replace_this = match.group()
        
        ## run find & replace on all valid filenames
        newfile_extension = filename[-4:]
        if newfile_extension.startswith("."):
            newfile_name = newfile_name[:-4]
            if starts_with and newfile_name.startswith(replace_this):
                newfile_name = newfile_name.replace(replace_this, with_this, repeat)
            elif ends_with and newfile_name.endswith(replace_this):
                newfile_name = rreplace(newfile_name, replace_this, with_this, repeat)
            else:
                newfile_name = newfile_name.replace(replace_this, with_this, repeat)
            newfile_name = newfile_name.strip()
            newfile_name = newfile_name + newfile_extension
        else:
            if newfile_name.count(".") == 0:
                if starts_with == True:
                    if newfile_name.startswith(replace_this):
                        newfile_name = newfile_name.replace(replace_this, with_this, repeat)
                else:
                    newfile_name = newfile_name.replace(replace_this, with_this, repeat)
                newfile_name = newfile_name.strip()
            
    return newfile_name
            
def rename_files(search_directory, replace_list, with_this="", repeat=1, recursive=False, starts_with=False, ends_with=False, regular_expression=False, media_only=False):
    """ Rename files in the given search_directory. """ 
    for root, directories, filenames in os.walk(search_directory):
        if recursive:
            for directory in directories:
                subdirectory = os.path.join(search_directory, directory)
                if os.path.isdir(subdirectory):
                    rename_files(subdirectory, replace_list, with_this, repeat, recursive, starts_with, ends_with) 
                
        for filename in filenames:
            file_fullpath = os.path.join(search_directory, filename)
            if os.path.isfile(file_fullpath): 
                newfile_name = filename
                
                if media_only:
                    if pymedia.is_media_file(filename):
                        newfile_name = rename(filename, replace_list, with_this, repeat, recursive, starts_with, ends_with)
                else:
                    newfile_name = rename(filename, replace_list, with_this, repeat, recursive, starts_with, ends_with)
                    
                ## if the name has changed, report and rename it
                if newfile_name != filename:
                    print(" << " + os.path.join(search_directory, filename))
                    print(" >> " + os.path.join(search_directory, newfile_name))                     
                    newfile_fullpath = os.path.join(search_directory, newfile_name)
                    os.rename(file_fullpath, newfile_fullpath) 
                    
if __name__ == "__main__":   
    try:
        pyapp.print_header("Rename Files")
        if check_preset():
            process_presets(get_root_directory());
        else:        
            args = get_arguments()
            if pyapp.query_yes_no("Replace '{0}' with '{1}'?".format(args.replace_this, args.with_this)):
                replace_list = [args.replace_this]               
                rename_files(get_root_directory(), replace_list, args.with_this, args.repeat, args.recursive, args.starts_with, args.ends_with, args.regular_expression)            
                
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        raise        
        sys.exit(-1)    