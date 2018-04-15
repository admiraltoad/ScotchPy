"""
    Television
    
"""
from ScotchPy.objects import media_file

class tv_media(media_file.media_file):

    def __init__(self, show_name, season, episode, title, extension, destination):
        filename = ""
        if title == "" or title is None:
            filename = "{0} s{1}e{2}{3}".format(show_name, season, episode, extension) 
        else:
            filename = "{0} s{1}e{2} {3}{4}".format(show_name, season, episode, title, extension)
        
        subdirectory = [show_name, "Season {0}".format(season)]
        super(tv_media, self).__init__(destination, filename, media_file.media_type.TV, subdirectory)
        self.show_name = show_name
        self.season = season
        self.episode = episode 

    def get_show_name(self):
        return self.show_name

    def get_season(self):
        return self.season

    def get_episode(self):
        return self.episode