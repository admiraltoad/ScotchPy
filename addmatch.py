import os, pyapp
import xml.etree.cElementTree as etree

def main():
    xml_filename = "matches.xml"
    
    sys_argv = pyapp.get_system_arguments()

    if len(sys_argv) != 2:
        raise Exception("Invalid Match.")

    match = sys_argv[0]
    to_this = sys_argv[1]

    print("!", match, to_this)
    
    if os.path.isfile(xml_filename):
        tree = etree.parse(xml_filename)
        root = tree.getroot()

        entry = root.find("root")
        
        new=etree.Element('match')
        new.text = match
        child[1].append(new)
        
        new=etree.Element('to_this')
        new.text = to_this
        child[1].append(new)

if __name__ == '__main__':
  main()