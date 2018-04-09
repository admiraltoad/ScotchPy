"""
    pymedia :: movie
    
"""
from ScotchPy.objects import media_file

class movie_media(media_file.media_file):
    
    def __init__(self, movie_name, year, extension, destination):
        filename = "{0} ({1}){2}".format(movie_name, year, extension)
        super(movie_media, self).__init__(destination, filename, media_file.media_type.MOVIE)
        self.movie_name = movie_name
        self.year = year

    def get_movie_name(self):
        return self.movie_name

    def get_year(self):
        return self.year