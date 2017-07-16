"""
    Rename Files
"""
from pymedia import television as tv
import pyapp
import os, string, shutil, sys, errno 
from xml.etree import ElementTree as etree
import argparse

def get_system_arguments():
    sys_argv = list(sys.argv)
    sys_argv.pop(0) ## remove filepath from the system arguments
    return sys_argv

def process_presets():
    rename_files(".", " ", 100)
    filepath = os.path.dirname(os.path.realpath(__file__))
    tree = etree.parse(os.path.join(filepath,'renamefiles.preset.xml'))
    root = tree.getroot()
    for item in root.iter('item'):        
        rename_files(item.text)
        
class arguments(object):
    pass    
        
def check_preset():
    system_arguments = get_system_arguments()  
    if len(system_arguments) > 0:
        if system_arguments[0] == "--preset" or system_arguments[0] == "-p":
            return True
    return False        

def get_arguments():    
    command_arguments = arguments()
    
    ## Define command arguments
    parser = argparse.ArgumentParser(description='Rename Files') 
    parser.add_argument(
        '--replace_this', 
        '-r', 
        required=True, 
        help='Replace this string.'
        )
    parser.add_argument(
        '--with_this', 
        '-w', 
        required=False, 
        help='With this string.'
        )
    parser.add_argument(
        '--repeat', 
        '-c', 
        required=False, 
        type=int, 
        help='Repeat the operation this many times.'
        )
    parser.add_argument(
        '--starts_with', 
        '-s', 
        required=False, 
        action='store_true',
        help='Replace first instance if the filename starts with [--replace_this/-r] string.'
        )
    parser.add_argument(
        '--ends_with', 
        '-e', 
        required=False, 
        action='store_true',
        help='Replace last instance if the filename ends with [--replace_this/-r] string.'
        )   
    parser.add_argument(
        '--preset', 
        '-p', 
        required=False,
        help='Run the preset formatting for files. Must be the first given argument.'
        )           
    parser.set_defaults(replace_this=None, with_this=None, repeat=0, starts_with=False, ends_with=False)

    ## Process system arguments    
    parser.parse_args(args=get_system_arguments(), namespace=command_arguments)
    
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
    
def rename_files(replace_this, with_this="", repeat=1, starts_with=False, ends_with=False):
    ## search all files in the calling (root) directory 
    root_directory = os.path.abspath('.') + '\\'
    for root, directories, filenames in os.walk(root_directory):
        for filename in filenames:
            file_fullpath = os.path.join(root_directory, filename)
            if os.path.isfile(file_fullpath):  
                newfile_name = filename

                ## run find & replace on all valid filenames
                ## run find & replace on all valid filenames
                newfile_extension = filename[-4:]
                if newfile_extension.startswith('.'):
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
                    if newfile_name.count('.') == 0:
                        if starts_with == True:
                            if newfile_name.startswith(replace_this):
                                newfile_name = newfile_name.replace(replace_this, with_this, repeat)
                        else:
                            newfile_name = newfile_name.replace(replace_this, with_this, repeat)
                        newfile_name = newfile_name.strip()
                        
                ## if the name has changed, report and rename it
                if newfile_name != filename:
                    print(" - " + filename)
                    print(" - " + newfile_name)                     
                    newfile_fullpath = os.path.join(root_directory, newfile_name)
                    os.rename(file_fullpath, newfile_fullpath) 
                    
def main():  
    try:
        if check_preset():
            process_presets();
        else:        
            args = get_arguments()
            if pyapp.query_yes_no("Replace '{}' with '{}'?".format(args.replace_this, args.with_this)):
                rename_files(args.replace_this, args.with_this, args.repeat, args.starts_with)
            
    except Exception as ex:
        if len(ex.args) == 1:
            print("Error:", ex.args[0])       
        else:
            raise
    
pyapp.print_header("Rename Files", 1, 0)
main()
sys.exit(0)