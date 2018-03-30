"""
    pymedia :: media utilities
    
"""
import os, re, datetime
from pymedia import media as m
from pymedia import television as tv
from pymedia import movie

def is_media_file(filename):
    """ Check the file extension to see if it is a media file. """
    newfile_name, extension = os.path.splitext(filename)
    return extension in ('.avi','.mkv','.mp4', '.mpg', '.xvid', '.mov')

def get_filename_year(filename):
    """ Return the year given in the filename. """
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

def create_media_file(destination, filename, remove_title=False):
    """ Process [filename] to determine if it is a tv or movie media file.  """ 
    new_media_file = m.media_file(destination, filename)
    if is_media_file(filename):   
        newfile_name, extension = os.path.splitext(filename)
        newfile_name = newfile_name.replace("."," ")
        episode_tag, season, episode = tv.get_episode_info(newfile_name)
        if episode_tag is not None:      
            start = int(newfile_name.find(episode_tag))
            end = int(start + len(episode_tag))             
            showname = (newfile_name[:start]).strip()  
            showname = tv.process_tvshow_name(showname)      
            showname, tvshow_year = get_filename_year(showname)
            if tvshow_year is not None:
                showname = "{0} ({1})".format(showname, tvshow_year)
            episode_title = (newfile_name[end:(len(newfile_name))]).strip()             
            if remove_title == True or len(episode_title) < 1:
                episode_title = None
            tvshow_destination = tv.find_tvshow_path(destination, showname)
            if tvshow_destination is None:
                tvshow_destination = destination
            new_media_file = tv.tv_media(showname, season, episode, episode_title, extension, tvshow_destination)
        else:       
            movie_name, movie_year = get_filename_year(newfile_name)
            if movie_year is not None:
                new_media_file = movie.movie_media(movie_name, movie_year, extension, destination)
        if new_media_file.get_type() == m.media_type.MISC:
            print("?? unable to determine media type for [{0}]".format(filename))
    return new_media_file   