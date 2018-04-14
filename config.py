"""
    Configuration	
	
"""
import os
from xml.etree import ElementTree as etree

def get_value(key_name):    
    """ get the key_name node from the config.xml file """
    filepath = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(filepath, 'data', 'config.xml')
    if not os.path.isfile(config_file):
        raise Exception("Missing expected [{0}}].".format(filepath))
        
    root = etree.parse(config_file).getroot()
    return root.find(key_name)