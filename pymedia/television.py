"""
    pymedia :: television
    
"""
import re, os
from xml.etree import ElementTree as etree

class tv_episode():       
    def __init__(self, name, season, episode, title, extension):
        self.info = {}
        self.info["name"]=name
        self.info["season"]=season
        self.info["episode"]=episode
        self.info["title"]= None if (title=="") else title
        self.info["extension"]=extension
    def get_name(self):
        return self.info["name"]
    def get_season(self):
        return self.info["season"]
    def get_episode(self):
        return self.info["episode"]
    def get_title(self):
        return self.info["title"]
    def get_extension(self):
        return self.info["extension"]
    def get_filename(self, keep_title=False):
        if keep_title or self.get_title() is None:
            return "{0} s{1}e{2}.{3}".format(self.get_name(), self.get_season(), self.get_episode(), self.get_extension())
        else:
            return "{0} s{1}e{2} {3}.{4}".format(self.get_name(), self.get_season(), self.get_episode(), self.get_title(), self.get_extension())

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
    
def process_filename(filename):  
    episode_obj = None
    
    extension = filename[-3:]
    if extension in ('avi','mkv','mp4', 'mpg'):    
        newfilename = filename.replace("."," ")
        tag = find_season_episode_tag(newfilename)
        if tag is not None:
            season_episode_tag = tag.group(0).strip()            
            
            tag_start = int(newfilename.find(season_episode_tag))
            tag_end = int(tag_start + len(season_episode_tag))
                    
            name = (newfilename[:tag_start]).strip()  
            name = process_tvshow_name(name)      
            
            title = (newfilename[tag_end:(len(newfilename)-4)]).strip() 
                
            season, episode = get_season_episode_numbers(season_episode_tag)
                        
            episode_obj = tv_episode(name, season, episode, title, extension)

    return episode_obj    
        