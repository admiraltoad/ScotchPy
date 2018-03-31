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

def create_media_file(destination, filename, remove_title=False):
    """ Process [filename] to determine if it is a tv or movie media file.  """ 
    new_media_file = m.base_file()
    if is_media_file(filename):   
        newfile_name, extension = os.path.splitext(filename)
        newfile_name = newfile_name.replace("."," ")        
        if tv.is_tv_media(newfile_name):  
            new_media_file = tv.process_filename(newfile_name, extension, destination, remove_title) 
        elif movie.is_movie_media(newfile_name):
            new_media_file = movie.process_filename(newfile_name, extension, destination)
        else:
            new_media_file = m.media_file(destination, filename)
    return new_media_file   