"""
    Sort Downloads
"""
import argparse
import os, string, shutil, sys, errno, time, filecmp, subprocess, datetime

from ScotchPy.utils import media_utils, file_utils, folder_utils
from ScotchPy import config
from ScotchPy.application import Application, get_root_directory, get_system_arguments

class SortDownloadsApp(Application):
    def __init__(self):     
        super(SortDownloadsApp, self).__init__("Sort Downloads")
        self.args = self.get_arguments()
    
    def run(self):
        """ Run the application instance in the calling directory. """
        run_all = not self.args.tv_only and not self.args.movies_only
        if self.args.tv_only or run_all:
            self.sort_tv(get_root_directory(), self.get_tv_path(), self.args.remove_title, self.args.set_metadata)
        if self.args.movies_only or run_all:
            self.sort_movies(get_root_directory(), self.get_movie_path(), self.args.set_metadata)

    def get_arguments(self):    
        """ Define and return a list of command line arguments. """
        parser = argparse.ArgumentParser(description="Sort Downloads") 
        parser.add_argument(
            "--movies_only", 
            "-m", 
            required=False, 
            action="store_true",
            help="Search media files and sort only movie files."
            ) 
        parser.add_argument(
            "--tv_only", 
            "-t", 
            required=False, 
            action="store_true",
            help="Search media files and sort only tv episode files."
            ) 
        parser.add_argument(
            "--remove_title", 
            "-r", 
            required=False, 
            action="store_true",
            help="Removes the tvshow episode title when sorting downloads."
            )
        parser.add_argument(
            "--set_metadata", 
            "-s", 
            required=False, 
            action="store_true",
            help="Sets metadata on file based on new filename."
            )              
        parser.set_defaults(movies_only=False,tv_only=False,remove_title=False)
    
        return parser.parse_args(args=get_system_arguments())
        
    def get_movie_path(self):
        """ Get the movies directory from the configuration file. """
        destination = config.get_value('movies')
        if destination is None:
            raise Exception("Definition for <movies> is missing from config.xml")
        else:
            return destination.text

    def get_tv_path(self):
        """ Get the tv show directory from the configuration file. """
        destination = config.get_value('tv')
        if destination is None:
            destination = config.get_value('sortdownloads')
            if destination is None:
                raise Exception("Definition for <tv> is missing from config.xml")
        else:
            return destination.text            

    def sort_movies(self, search_directory, movie_destination, set_metadata=False):    
        """ Move video files that match a given pattern from [search_directory] into [movie_destination].   """     
        if not os.path.isdir(movie_destination):
            os.makedirs(movie_destination)
            self.log.write("created:{0};\n".format(movie_destination))

        file_utils.remove_useless_files(search_directory)
        for root, directories, filenames in os.walk(search_directory):
            for directory in directories:
                subdirectory = os.path.join(root, directory)
                file_utils.remove_useless_files(subdirectory)
                folder_utils.remove_if_empty(subdirectory)  

            for filename in filenames:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    new_media = media_utils.create_media_file(movie_destination, filename)    
                    if new_media.is_movie():
                        file_utils.move_file(filepath, new_media.get_full_path())
                        self.log.write("moved_from:{0};moved_to:{1};\n".format(filepath, new_media.get_full_path()))
                else:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        self.log.write("removed:{0};\n".format(filepath))

    def sort_tv(self, search_directory, tvshow_destination, remove_title=False, set_metadata=False):    
        """ Move video files that match a given pattern from [search_directory] into [tvshow_destination].  """ 
        file_utils.remove_useless_files(search_directory)
        for root, directories, filenames in os.walk(search_directory):
            for directory in directories:
                subdirectory = os.path.join(root, directory)
                file_utils.remove_useless_files(subdirectory)
                folder_utils.remove_if_empty(subdirectory)       
            
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):            
                    new_media = media_utils.create_media_file(tvshow_destination, filename, remove_title)
                    if new_media.is_tv():
                        if not os.path.isdir(new_media.get_destination()):
                            os.makedirs(new_media.get_destination())
                            self.log.write("created:{0};\n".format(new_media.get_destination()))  
                        current_path = new_media.get_destination()
                        for subdir in new_media.get_subdirectories():
                            current_path = os.path.join(current_path, subdir)
                            if not os.path.exists(current_path):
                                os.makedirs(current_path) 
                                self.log.write("created:{0};\n".format(current_path))
                        file_utils.move_file(filepath, new_media.get_full_path())
                        self.log.write("moved_from:{0};moved_to:{1};\n".format(filepath, new_media.get_full_path())) 
                else:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        self.log.write("removed:{0};\n".format(filepath))

if __name__ == "__main__":
    try:
        app = SortDownloadsApp()
        app.run()            
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        raise
        sys.exit(-1)