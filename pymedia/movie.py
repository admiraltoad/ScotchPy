"""
    pymedia :: movie
    
"""
from pymedia import media as m

class movie_media(m.media_file):
    
    def __init__(self, movie_name, year, extension, destination):
        filename = "{0} ({1}){2}".format(movie_name, year, extension)
        super(movie_media, self).__init__(destination, filename, m.media_type.MOVIE)
        self.movie_name = movie_name
        self.year = year

    def get_movie_name(self):
        return self.movie_name

    def get_year(self):
        return self.year

def is_movie_media(filename):
    movie_name, movie_year = m.get_filename_year(filename)
    if movie_year is None:
        return False
    return True

def process_filename(filename, extension, destination):
    movie_name, movie_year = m.get_filename_year(filename)
    if movie_year is not None:
        new_media_file = movie_media(movie_name, movie_year, extension, destination)