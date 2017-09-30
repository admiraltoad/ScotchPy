"""
    pymedia :: television
    
"""
import re, os, datetime
from xml.etree import ElementTree as etree

class media_file():       
    def __init__(self, type, destination, filename):
        if filename is None or filename == "":
            raise Exception("Invalid media file filename. [{0}]".format(filename))
        if type not in ("TV", "MOVIE"):
            raise Exception("Invalid media file type. [{1}]".format(type))  
        self.type = type              
        self.destination = destination
        self.filename = filename  
    def get_type(self):
        return self.type
    def get_filename(self):
        return self.filename
    def get_destination(self):
        return self.destination
    def get_full_path(self):
        return os.path.join(self.destination, self.filename)

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

def is_media_file(filename):
    newfile_name, extension = os.path.splitext(filename)
    return extension in ('.avi','.mkv','.mp4', '.mpg', '.xvid')

def format_filename_year(filename):
    new_filename = filename
    match = re.search("\s\d+", new_filename)
    if match is not None:    
        now = datetime.datetime.now()
        year = match.group()
        if new_filename.endswith(year):
            if int(year) > 1945 and int(year) <= now.year:                            
                new_filename = new_filename.replace(year, " ({0})".format(year.strip()))
    return new_filename

def create_media_file(destination, filename, remove_title=False):  
    new_media_file = None    
    if is_media_file(filename):    
        newfile_name, extension = os.path.splitext(filename)
        newfile_name = newfile_name.replace("."," ")
        season_episode_tag = find_season_episode_tag(newfile_name)
        if season_episode_tag is not None:
            tag = season_episode_tag.group(0).strip()                     
            tag_start = int(newfile_name.find(tag))
            tag_end = int(tag_start + len(tag))                    
            name = (newfile_name[:tag_start]).strip()  
            name = process_tvshow_name(name)      
            name = format_filename_year(name)
            title = (newfile_name[tag_end:(len(newfile_name))]).strip()             
            if len(title) < 1:
                title = None
            season, episode = get_season_episode_numbers(tag)
            if remove_title == True or title is None:
                newfile_name = "{0} s{1}e{2}{3}".format(name, season, episode, extension) 
            else:
                newfile_name = "{0} s{1}e{2} {3}{4}".format(name, season, episode, title, extension)
            newfile_destination = os.path.join(destination, name, "Season {0}".format(season))
            new_media_file = media_file('TV', newfile_destination, newfile_name)
        else:        
            newfile_name = newfile_name.replace(".", " ")
            newfile_name = format_filename_year(newfile_name)
            print("{0}{1}".format(newfile_name, extension))
            if newfile_name != filename:
                new_media_file = media_file('MOVIE', destination, "{0}{1}".format(newfile_name, extension))
    return new_media_file    
        