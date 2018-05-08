"""
    Media Utilities
    
"""
import os, re, datetime
import xml.etree.ElementTree as etree

from ScotchPy.objects import media

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
    matches = re.findall("\s\(\d+\)", new_filename)
    if not matches:
        matches = re.findall("\s\d+", new_filename)
    if matches:            
        match = matches[-1] # last match
        now = datetime.datetime.now()        
        year_string = str(match)
        year = int(year_string.replace("(", "").replace(")", ""))
        if new_filename.endswith(year_string):
            if year > 1945 and year <= now.year:                        
                filename_year = str(year)
                new_filename = filename.replace(year_string, "")                
    return new_filename, filename_year

######################## Television Media ########################

def find_episode_pattern(filename):
    """ Find tv episode pattern (season #, episode #) in [filename]. """ 
    print("A:", filename)
    patterns = []
    patterns.append("\ss\d+\se\d+")     
    patterns.append("\ss\d+e\d+")
    patterns.append("\sS\d+\sE\d+") 
    patterns.append("\sS\d+E\d+")  
    patterns.append("\sS\d+\se\d+") 
    patterns.append("\sS\d+e\d+")
    patterns.append("\ss\d+\sE\d+")
    patterns.append("\ss\d+E\d+")

    found = None
    for pattern in patterns:
        found = re.search(pattern, filename)
        if found is not None:
            found = found.group(0).strip()
            break
    print("B:", found)
    if found is None:
        patterns = []
        patterns.append("\sseason\d+episode\d+")
        patterns.append("\sSeason\d+Episode\d+")
        patterns.append("\sseason\s\d+episode\s\d+")
        patterns.append("\sSeason\s\d+Episode\s\d+")

        for pattern in patterns:
            found = re.search(pattern, filename)
            print("C:", found)
            if found is not None:
                found = found.group(0).split()
                print(found)
                break

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
    show_name = tvshow_name if tvshow_name.endswith(".") == False else tvshow_name[:-1]  
    tvshow_path = None
    for root, directories, files in os.walk(search_directory): 
        for directory in directories:              
            subdirectory = os.path.join(root, directory)
            if os.path.isdir(subdirectory):
                if directory.lower() == show_name.lower():
                    return os.path.abspath(os.path.join(subdirectory, os.pardir))
    return tvshow_path

def get_tvshow_items():
    """ Returns match items from xml. """
    filepath = os.path.dirname(os.path.realpath(__file__))
    tvshow_match_xml = os.path.join(filepath, "..", "data", "tvshow.match.xml")
    if not os.path.isfile(tvshow_match_xml):
        raise Exception("[!] Missing match XML file '{0}'".format(tvshow_match_xml))
    tree = etree.parse(tvshow_match_xml)
    root = tree.getroot()   
    return root.iter("item")
    
def process_tvshow_name(tvshow_name):
    """ Process [tvshow_name] through the xml match list. """
    tvshow_match = None
    for item in get_tvshow_items():
        if tvshow_match is not None:
            break      
        name = item.find("name").text
        if name.lower() == tvshow_name.lower():
            tvshow_match = item.find("match").text                 
    return tvshow_name if tvshow_match is None else tvshow_match

######################## Object Creation ########################

def create_movie_media(filename, extension, destination):
    """ Create a new MovieMedia object. """
    movie_file = None
    movie_name, movie_year = get_filename_year(filename)
    if movie_year is not None:
        movie_file = media.MovieMedia(movie_name, movie_year, extension, destination)
    return movie_file

def create_tv_media(filename, extension, destination, remove_title = False):
    """ Create a new TVMedia object. """
    tv_file = None
    if find_episode_pattern(filename) is not None:
        episode_tag, season, episode = get_episode_info(filename)
        if episode_tag is None:
            raise Exception("[!] Failed to process filename as tv show pattern.")
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
        tv_file = media.TVMedia(showname, season, episode, episode_title, extension, tvshow_destination)
    return tv_file

def create_media_file(destination, filename, remove_title=False):
    """ Process [filename] to determine if it is a tv or movie media file.  """ 
    new_MediaFile = media.BaseFile()
    if is_media_file(filename):   
        newfile_name, extension = os.path.splitext(filename)
        newfile_name = newfile_name.replace("."," ")        
        if is_tv_media(newfile_name):                  
            new_MediaFile = create_tv_media(newfile_name, extension, destination, remove_title) 
        elif is_movie_media(newfile_name):
            new_MediaFile = create_movie_media(newfile_name, extension, destination)
        else:
            new_MediaFile = media.MediaFile(destination, filename, extension)
    return new_MediaFile   
