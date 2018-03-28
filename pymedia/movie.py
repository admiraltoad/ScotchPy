"""
    pymedia :: movie
    
"""
from pymedia import media as m

class movie_media(m.media_file):
    
    def __init__(self, movie_name, year, extension, destination, subdirectory = None):
        filename = "{0} ({1}).{2}".format(movie_name, year, extension)
        super(movie_media, self).__init__(m.media_type.MOVIE, destination, filename, subdirectory)
        self.movie_name = movie_name
        self.year = year

    def get_movie_name(self):
        return self.movie_name

    def get_year(self):
        return self.year