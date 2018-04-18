"""
    Application	
	
"""
import os, string, shutil, sys, errno, datetime 
from xml.etree import ElementTree as etree

## Globals
MAJOR = 2
MINOR = 0

class Log():
    """ """
    def __init__(self, app_name, version):
        appdata_path = os.getenv('APPDATA')
        if appdata_path is None or os.path.isdir(appdata_path) == False:
            raise Exception("[!] Could not find APPDATA folder path.")

        self.filepath = os.path.join(appdata_path, "ScotchPy", app_name, version)
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)   

        self.filename = "{0}-{1:%Y-%m-%d-%H%M%S%f}.log".format(app_name.lower().replace(" ", "_", 48).strip(), datetime.datetime.now())

        self.full_filepath = os.path.join(self.filepath, self.filename)
        if not os.path.isfile(self.full_filepath):                      
            open(self.full_filepath, 'w+')

    def write(self, string):
        """" """
        with open(self.full_filepath, 'a') as out:         
                out.write(string)
        
class Application():
    def __init__(self, name, major=MAJOR, minor=MINOR):
        """ """
        self.name = name 
        self.major = major
        self.minor = minor
        self.version = "{0}.{1}".format(self.major, self.minor)
        self.log = Log(self.name, self.version)       
        self.print_header()

    def print_header(self):
        """ """
        print("-"*24)
        print("{0} ({1})".format(self.name, self.version))
        print("-"*24)            

def get_system_arguments():
    """  """
    sys_argv = list(sys.argv)
    sys_argv.pop(0) ## remove filepath from the system arguments
    if len(sys_argv) == 0:
        sys_argv = None
    return sys_argv  
    
def query_yes_no(question, default=None):
    """Ask a yes/no question via input() and return their answer.

    Args:
        question - is a string that is presented to the user.
        default - is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    Return:
        True for "yes" or False for "no".
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