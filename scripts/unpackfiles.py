"""
    Unpack Files
"""
import os, sys, shutil, errno

from ScotchPy.application import Application, get_root_directory
from ScotchPy.utils import folder_utils, file_utils

class UnpackFilesApp(Application):
	def __init__(self):		
		super(UnpackFilesApp, self).__init__("Unpack Files")
	
	def run(self):
		""" Run the application instance in the calling directory. """
		self.unpackfiles(get_root_directory())

	def unpackfiles(self, search_directory):
		""" Move all files in subdirectories under [search_directory] to root.  """
		file_utils.remove_useless_files(search_directory)		
		for root, directories, filenames in os.walk(search_directory):
			for filename in filenames:
				source_filename = os.path.join(root, filename)
				if os.path.isfile(source_filename):								
					destination = os.path.join(search_directory, filename)
					file_utils.move_file(source_filename, destination)
					self.log.write("moved_from:{0};moved_to:{1};\n".format(source_filename, destination))	
			for directory in directories:
				subdirectory = os.path.join(root, directory)
				folder_utils.remove_if_empty(subdirectory)
		folder_utils.remove_if_empty(search_directory)

if __name__ == "__main__":   	
	try:
		main = UnpackFilesApp()
		main.run()
		sys.exit(0)
	except Exception as ex:
		print("Error:", str(ex), "\n")
		raise        
		sys.exit(-1)				
