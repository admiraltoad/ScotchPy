"""
    Application	
	
"""
import os, string, shutil, sys, errno 
from xml.etree import ElementTree as etree

## Global Variables 
MAJOR = 2
MINOR = 0

def print_header(name):
	print("----------------------------------------------")
	print(name + " (v" + str(MAJOR) + "." + str(MINOR) + ")")
	print("----------------------------------------------")

def get_system_arguments():
    sys_argv = list(sys.argv)
    sys_argv.pop(0) ## remove filepath from the system arguments
    if len(sys_argv) == 0:
        sys_argv = None
    return sys_argv  
    
def query_yes_no(question, default=None):
    """Ask a yes/no question via input() and return their answer.

    :question - is a string that is presented to the user.
    :default - is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    :return - True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")