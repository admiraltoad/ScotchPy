"""
    objects :: media objects
    
"""
import os
from enum import Enum

class MediaType(Enum):
    """  """
    INVALID = 0
    MISC = 1
    TV = 2
    MOVIE = 3

class BaseFile():
    """  """
    def __init__(self):
        self.type = MediaType.INVALID

    def get_type(self):
        return self.type

    def is_tv(self):
        return False

    def is_movie(self):
        return False

class MediaFile(BaseFile):
    """  """
    def __init__(self, destination, filename, extension, m_type = MediaType.MISC, subdirectories = []):
        if filename is None or filename == "":
            raise Exception("Invalid media file filename. [{0}]".format(filename))
        if m_type not in MediaType:
            raise Exception("Invalid media file type. [{1}]".format(str(m_type)))
        self.m_type = m_type           
        self.destination = destination
        self.filename = filename
        self.extension = extension  
        self.subdirectories = [] if subdirectories is None else subdirectories

    def is_tv(self):
        return self.m_type == MediaType.TV

    def is_movie(self):
        return self.m_type == MediaType.MOVIE

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

class MovieMedia(MediaFile):
    
    def __init__(self, movie_name, year, extension, destination):
        filename = "{0} ({1})".format(movie_name, year)
        super(MovieMedia, self).__init__(destination, filename, extension, mf.MediaType.MOVIE)
        self.movie_name = movie_name
        self.year = year

    def get_movie_name(self):
        return self.movie_name

    def get_year(self):
        return self.year

class TVMedia(MediaFile):

    def __init__(self, show_name, season, episode, title, extension, destination):
        filename = ""
        if title == "" or title is None:
            filename = "{0} s{1}e{2}".format(show_name, season, episode) 
        else:
            filename = "{0} s{1}e{2} {3}".format(show_name, season, episode, title)
        
        subdirectory = [show_name, "Season {0}".format(season)]
        super(TVMedia, self).__init__(destination, filename, extension, mf.MediaType.TV, subdirectory)
        self.show_name = show_name
        self.season = season
        self.episode = episode 

    def get_show_name(self):
        return self.show_name

    def get_season(self):
        return self.season

    def get_episode(self):
        return self.episode