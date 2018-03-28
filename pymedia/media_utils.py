"""
    pymedia :: media utilities
    
"""
import os, re, datetime
from pymedia import media as m
from pymedia import television as tv
from pymedia import movie

def is_media_file(filename):
    newfile_name, extension = os.path.splitext(filename)
    return extension in ('.avi','.mkv','.mp4', '.mpg', '.xvid', '.mov')

def get_filename_year(filename):
    """ Return the year given in the filename """
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

def format_filename_year(filename):
    new_filename = filename
    match = re.search("\(\s\d+\)", new_filename)
    if match is None:
        match = re.search("\s\d+", new_filename)
    if match is not None:    
        now = datetime.datetime.now()
        year = int(match.group().replace("(", "").replace(")", ""))
        if new_filename.endswith(match.group()):
            if year > 1945 and year <= now.year:                            
                new_filename = new_filename.replace(year, " ({0})".format(str(year)))
    return new_filename

def create_media_file(destination, filename, remove_title=False):  
    new_media_file = m.media_file(destination, filename)    
    if is_media_file(filename):    
        newfile_name, extension = os.path.splitext(filename)
        newfile_name = newfile_name.replace("."," ")
        season_episode_tag = tv.find_season_episode_tag(newfile_name)
        if season_episode_tag is not None:
            tag = season_episode_tag.group(0).strip()                     
            tag_start = int(newfile_name.find(tag))
            tag_end = int(tag_start + len(tag))                    
            name = (newfile_name[:tag_start]).strip()  
            name = tv.process_tvshow_name(name)      
            name = format_filename_year(name)
            title = (newfile_name[tag_end:(len(newfile_name))]).strip()             
            if remove_title == True or len(title) < 1:
                title = None
            season, episode = tv.get_season_episode_numbers(tag)            
            new_media_file = tv.tv_media(name, season, episode, title, extension, destination)
        else:       
            name, year = get_filename_year(newfile_name)
            if year is not None:
                new_media_file = movie.movie_media(name, year, extension, destination)
    if new_media_file.get_type() == m.media_type.MISC:
        print("?? unable to determine media type for [{0}]".format(filename))
    return new_media_file