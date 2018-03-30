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

def find_episode_pattern(filename):
    """ Find tv episode pattern (season #, episode #) in [filename]. """ 
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
    if found is not None:
        found = found.group(0).strip() 
    return found

def get_episode_info(filename):
    """ Find tv episode info (season #, episode #) in [filename]. """ 
    episode_tag, season, episode = None, None, None
    episode_tag = find_episode_pattern(filename)
    if episode_tag is not None:
        pattern = episode_tag.lower().replace("s"," ").replace("e"," ")
        pattern_array = pattern.split()
        season = int(pattern_array[0])
        episode =  int(pattern_array[1])
        season = "{:0>2}".format(season)
        episode = "{:0>2}".format(episode)
    return episode_tag, season, episode

def find_tvshow_path(search_directory, tvshow_name):    
    """ Find [tvshow_name] folder name in [search_directory].  """  
    tvshow_path = None
    for root, directories, files in os.walk(search_directory): 
        for directory in directories:              
            subdirectory = os.path.join(root, directory)
            if os.path.isdir(subdirectory):
                if directory.lower() == tvshow_name.lower():
                    return os.path.abspath(os.path.join(subdirectory, os.pardir))
    return tvshow_path

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