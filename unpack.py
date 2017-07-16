"""
    unpack 1.0
"""
import pyapp, os, sys, shutil, errno

m_rootDir = os.path.abspath('.') + '\\'

def copyfile(src, dst):
    try:
        shutil.copy2(src, dst)
    except OSError as exc:
        exc = 0 # ignore		

def main(searchDir):
	for root, directories, filenames in os.walk(searchDir):
		for directory in directories:
			currentDir = os.path.join(searchDir, directory)
			if os.path.isdir(currentDir):
				print("[" + currentDir + "]")
				main(currentDir)
				try:							
					for subroot, subdirectories, subfilenames in os.walk(currentDir):
						for filename in subfilenames:
							currentFile = os.path.join(currentDir, filename)
							if os.path.isfile(currentFile):
								print("..  " + filename)
								destinationFile = os.path.join(searchDir, filename)
								shutil.copy2(currentFile, destinationFile)
								os.remove(currentFile);
								
					os.rmdir(currentDir)
				except:
					print("! Error processing [" + currentDir + "]")
					
pyapp.print_header("Unpack", 1, 0)
main(m_rootDir)
sys.exit(0)