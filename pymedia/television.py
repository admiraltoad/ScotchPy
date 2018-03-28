"""
    pymedia :: television
    
"""
import re, os
from xml.etree import ElementTree as etree
from pymedia import media as m

class tv_media(m.media_file):

    def __init__(self, show_name, season, episode, title, extension, destination):
        filename = ""
        if title == "" or title is None:
            filename = "{0} s{1}e{2}{3}".format(show_name, season, episode, extension) 
        else:
            filename = "{0} s{1}e{2} {3}{4}".format(show_name, season, episode, title, extension)
        subdirectory = [show_name, "Season {0}".format(season)]
        super(tv_media, self).__init__(destination, filename, m.media_type.TV, subdirectory)
        self.show_name = show_name
        self.season = season
        self.episode = episode 

    def get_show_name(self):
        return self.show_name

    def get_season(self):
        return self.season

    def get_episode(self):
        return self.episode

def find_season_episode_tag(filename): 
    found = re.search("\ss\d+\se\d+", filename) 
    if not found:
        found = re.search("\ss\d+e\d+", filename)       
    if not found:
        found = re.search("\sS\d+\sE\d+", filename) 
    if not found:
        found = re.search("\sS\d+E\d+", filename)       
    if not found:
        found = re.search("\sS\d+\se\d+", filename) 
    if not found:
        found = re.search("\sS\d+e\d+", filename)
    if not found:
        found = re.search("\ss\d+\sE\d+", filename)
    if not found:
        found = re.search("\ss\d+E\d+", filename)
    return found

def get_season_episode_numbers(season_episode_tag):
    pattern = season_episode_tag
    pattern = pattern.lower()
    pattern = pattern.replace("s"," ")
    pattern = pattern.replace("e"," ")
    patternArray = pattern.split()
    season_num = int(patternArray[0])
    episode_num =  int(patternArray[1])
    season_num = "{:0>2}".format(season_num)
    episode_num = "{:0>2}".format(episode_num)
    return season_num, episode_num

def get_tvshow_items():
    filepath = os.path.dirname(os.path.realpath(__file__))
    tree = etree.parse(os.path.join(filepath,"tvshow.match.xml"))
    root = tree.getroot()   
    return root.iter("item")
    
def process_tvshow_name(tvshow_name):
    tvshow_match = None
    for item in get_tvshow_items():       
        name = item.find("name").text
        if name.lower() == tvshow_name.lower():
            tvshow_match = item.find("match").text
            break
    if tvshow_match is not None:
        tvshow_name = tvshow_match        
    return tvshow_name