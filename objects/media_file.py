"""
    pymedia :: media file
    
"""
import os
from enum import Enum

class media_type(Enum):
    """  """
    INVALID = 0
    MISC = 1
    TV = 2
    MOVIE = 3

class base_file():
    """  """
    def __init__(self):
        self.type = media_type.INVALID

    def get_type(self):
        return self.type

    def is_tv(self):
        return False

    def is_movie(self):
        return False

class media_file(base_file):
    """  """
    def __init__(self, destination, filename, extension, type = media_type.MISC, subdirectories = []):
        if filename is None or filename == "":
            raise Exception("Invalid media file filename. [{0}]".format(filename))
        if type not in media_type:
            raise Exception("Invalid media file type. [{1}]".format(str(type)))
        self.type = type           
        self.destination = destination
        self.filename = filename
        self.extension = extension  
        self.subdirectories = [] if subdirectories is None else subdirectories

    def is_tv(self):
        return self.type == media_type.TV

    def is_movie(self):
        return self.type == media_type.MOVIE

    def get_filename(self):
        return self.filename

    def get_extension(self):
        return self.extension

    def get_destination(self):
        return self.destination

    def get_subdirectories(self):
        return self.subdirectories

    def get_full_destination(self):
        return os.path.join(self.destination, *self.subdirectories)

    def get_full_path(self):
        return os.path.join(self.get_full_destination(), "{0}{1}".format(self.filename, self.extension))