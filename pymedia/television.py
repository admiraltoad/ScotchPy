"""
    pymedia :: television
    
"""
import re, os
from xml.etree import ElementTree as etree

class tvEpisode():       
    def __init__(self, name, season, episode, extension):
        self.info = {}
        self.info['name']=name
        self.info['season']=season
        self.info['episode']=episode
        self.info['extension']=extension
        self.info['filename']=name+" "+"s"+season+"e"+episode+"."+extension
    def getName(self):
        return self.info['name']
    def getSeason(self):
        return self.info['season']
    def getEpisode(self):
        return self.info['episode']
    def getExtension(self):
        return self.info['extension']
    def getFilename(self):
        return self.info['filename']

def findSeasonEpisodePattern(filename): 
    found = re.search('\ss\d+\se\d+', filename) 
    if not found:
        found = re.search('\ss\d+e\d+', filename)       
    if not found:
        found = re.search('\sS\d+\sE\d+', filename) 
    if not found:
        found = re.search('\sS\d+E\d+', filename)       
    if not found:
        found = re.search('\sS\d+\se\d+', filename) 
    if not found:
        found = re.search('\sS\d+e\d+', filename)
    if not found:
        found = re.search('\ss\d+\sE\d+', filename)
    if not found:
        found = re.search('\ss\d+E\d+', filename)
    return found

def getTVShowItems():
    filepath = os.path.dirname(os.path.realpath(__file__))
    tree = etree.parse(os.path.join(filepath,'tvshow.match.xml'))
    root = tree.getroot()   
    return root.iter('item')
    
def processTVShowName(tvshowname):
    tvshowname = tvshowname.title()
    tvshowMatch = None
    for item in getTVShowItems():       
        name = item.find('name').text
        if name.lower() == tvshowname.lower():
            tvshowMatch = item.find('match').text
            break
    if tvshowMatch:
        tvshowname = tvshowMatch        
    return tvshowname   
   
def getSeasonEpisodeNumbers(episodeString):
    pattern = episodeString
    pattern = pattern.lower()
    pattern = pattern.replace('s',' ')
    pattern = pattern.replace('e',' ')
    patternArray = pattern.split()
    seasonNum = int(patternArray[0])
    episodeNum =  int(patternArray[1])
    seasonNum = "{:0>2}".format(seasonNum)
    episodeNum = "{:0>2}".format(episodeNum)
    return seasonNum, episodeNum

def getShowName(filename, episodeString):
    patternIDX = int(filename.find(episodeString))
    showname = (filename[:patternIDX]).strip() 
    showname = showname.replace(' -', '')
    showname = processTVShowName(showname)
    return showname
    
def getFileExtension(filename):
    return filename[-3:]

def processFilename(filename):  
    episodeObj = None
    newfilename = filename.replace('.',' ')
    patternFound = findSeasonEpisodePattern(newfilename)
    if patternFound:
        episodeString = patternFound.group(0).strip()       
        showname = getShowName(newfilename, episodeString)
        showname = processTVShowName(showname)
        season, episode = getSeasonEpisodeNumbers(episodeString)
        extension = getFileExtension(newfilename)
        episodeObj = tvEpisode(showname, season, episode, extension)
    return episodeObj
    
        