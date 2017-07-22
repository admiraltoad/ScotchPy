"""
    Unpack Files
"""
import pyapp, os, sys, shutil, errno

m_rootDir = os.path.abspath('.') + '\\'

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
								shutil.move(currentFile, destinationFile)								
								
					os.rmdir(currentDir)
				except:
					print("! Error processing [" + currentDir + "]")

if __name__ == "__main__":   					
    pyapp.print_header("Unpack Files")
    main(m_rootDir)
    sys.exit(0)