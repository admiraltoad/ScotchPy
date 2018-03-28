"""
    pymedia :: television
    
"""
import re, os, datetime
from enum import Enum
from xml.etree import ElementTree as etree

class media_type(Enum):
    MISC = 1
    TV = 2
    MOVIE = 3

class media_file():       
    def __init__(self, type, destination, filename, subdirectories = None):
        if filename is None or filename == "":
            raise Exception("Invalid media file filename. [{0}]".format(filename))
        if type not in media_type:
            raise Exception("Invalid media file type. [{1}]".format(str(type)))
        self.type = type           
        self.destination = destination
        self.filename = filename  
        self.subdirectories = subdirectories
    def is_type(self, type):
        return type == self.type
    def get_type(self):
        return self.type
    def get_filename(self):
        return self.filename
    def get_destination(self):
        return self.destination
    def get_subdirectories(self):
        return self.subdirectories
    def get_full_destination(self):
        return os.path.join(self.destination, self.subdirectories)
    def get_full_path(self):
        return os.path.join(self.get_full_destination(), self.filename)

class tv_media(media_file):
    def __init__(self, show_name, season, episode, title, extension, destination):
        filename = ""
        if title == "" or title is None:
            filename = "{0} s{1}e{2}{3}".format(show_name, season, episode, extension) 
        else:
            filename = "{0} s{1}e{2} {3}{4}".format(show_name, season, episode, title, extension)
        subdirectory = "Season {0}".format(season)
        super(tv_media, self).__init__(media_type.TV, destination, filename, subdirectory)
        self.show_name = show_name
        self.season = season
        self.episode = episode     
    def get_show_name(self):
        return self.show_name
    def get_season(self):
        return self.season
    def get_episode(self):
        return self.episode

class movie_media(media_file):
    def __init__(self, movie_name, year, extension, destination, subdirectory = None):
        filename = "{0} ({1}).{2}".format(movie_name, year, extension)
        super(movie_media, self).__init__(media_type.MOVIE, destination, filename, subdirectory)
        self.movie_name = movie_name
        self.year = year   
    def get_movie_name(self):
        return self.movie_name
    def get_year(self):
        return self.year

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
    return extension in ('.avi','.mkv','.mp4', '.mpg', '.xvid', '.mov')

def get_filename_year(filename):
    filename_year = None
    match = re.search("\s\d+", filename)
    if match is not None:    
        now = datetime.datetime.now()
        year = match.group()
        if filename.endswith(year):
            if int(year) > 1945 and int(year) <= now.year:                            
                filename_year = year.strip()
    return filename_year

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
            
            tvshow_path = os.path.join(name, "Season {0}".format(season))
            new_media_file = tv_media(name, season, episode, title, extension, destination)
        else:        
            movie_name = newfile_name.replace(".", " ")
            movie_year = get_filename_year(newfile_name)
            if newfile_name != filename:
                new_media_file = movie_media(movie_name, movie_year, extension, destination)
    return new_media_file    
        