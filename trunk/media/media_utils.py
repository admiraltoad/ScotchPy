"""
    Media Utilities
    
"""
import os, re, datetime
import xml.etree.ElementTree as etree

from media import television as tv
from media import movie
from media import media

def is_media_file(filename):
    """ Check the file extension to see if it is a media file. """
    newfile_name, extension = os.path.splitext(filename)
    if newfile_name != "" and newfile_name is not None:
        return extension in ('.avi','.mkv','.mp4', '.mpg', '.xvid', '.mov')
    return False 

def is_tv_media(filename):
    """ Check if the [filename] is a tv format 'name s#e# *title*'. """
    return find_episode_pattern(filename) is not None

def is_movie_media(filename):
    """ Check if the [filename] is a movie format 'name (year)'. """
    if not is_tv_media(filename):
        movie_name, movie_year = get_filename_year(filename)
        if movie_year is not None:
            return True
    return False

def get_filename_year(filename):
    """ Search for a year at the end of the filename. Return them seperately. """
    new_filename = filename
    filename_year = None
    match = re.search("\s\(\d+\)", new_filename)
    if match is None:
        match = re.search("\s\d+", new_filename)
    if match is not None:    
        now = datetime.datetime.now()
        year_string = match.group()
        year = int(year_string.replace("(", "").replace(")", ""))
        if new_filename.endswith(year_string):
            if year > 1945 and year <= now.year:                        
                filename_year = str(year)
                new_filename = filename.replace(year_string, "")
    return new_filename, filename_year

######################## Television Media ########################

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
    """ Returns match items from xml. """
    filepath = os.path.dirname(os.path.realpath(__file__))
    tree = etree.parse(os.path.join(filepath,"tvshow.match.xml"))
    root = tree.getroot()   
    return root.iter("item")
    
def process_tvshow_name(tvshow_name):
    """ Process [tvshow_name] through the xml match list. """
    tvshow_match = None
    for item in get_tvshow_items():       
        name = item.find("name").text
        if name.lower() == tvshow_name.lower():
            tvshow_match = item.find("match").text
            break
    if tvshow_match is not None:
        tvshow_name = tvshow_match        
    return tvshow_name

######################## Object Creation ########################

def create_movie_media(filename, extension, destination):
    """ Create a new movie_media object. """
    movie_file = None
    movie_name, movie_year = get_filename_year(filename)
    if movie_year is not None:
        movie_file = movie.movie_media(movie_name, movie_year, extension, destination)
    return movie_file

def create_tv_media(filename, extension, destination, remove_title = False):
    """ Create a new tv_media object. """
    tv_file = None
    if find_episode_pattern(filename) is not None:
        episode_tag, season, episode = get_episode_info(filename)
        if episode_tag is None:
            raise Exception("Failed to process filename as tv show pattern.")
        tag_start = int(filename.find(episode_tag))
        tag_end = int(tag_start + len(episode_tag))             
        showname = (filename[:tag_start]).strip()  
        showname = process_tvshow_name(showname)      
        showname, tvshow_year = get_filename_year(showname)
        if tvshow_year is not None:
            showname = "{0} ({1})".format(showname, tvshow_year)
        episode_title = (filename[tag_end:(len(filename))]).strip()             
        if remove_title == True or len(episode_title) < 1:
            episode_title = None
        tvshow_destination = find_tvshow_path(destination, showname)
        if tvshow_destination is None:
            tvshow_destination = destination
        tv_file = tv.tv_media(showname, season, episode, episode_title, extension, tvshow_destination)
    return tv_file

def create_media_file(destination, filename, remove_title=False):
    """ Process [filename] to determine if it is a tv or movie media file.  """ 
    new_media_file = media.base_file()
    if is_media_file(filename):   
        newfile_name, extension = os.path.splitext(filename)
        newfile_name = newfile_name.replace("."," ")        
        if is_tv_media(newfile_name):  
            new_media_file = create_tv_media(newfile_name, extension, destination, remove_title) 
        elif is_movie_media(newfile_name):
            new_media_file = create_movie_media(newfile_name, extension, destination)
        else:
            new_media_file = media.media_file(destination, filename)
    return new_media_file   
