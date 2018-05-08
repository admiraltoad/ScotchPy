"""
    Sort Downloads
"""
import argparse
import os, string, shutil, sys, errno, time, filecmp, subprocess, datetime

from ScotchPy.utils import media_utils, file_utils, folder_utils
from ScotchPy import config
from ScotchPy.application import Application
from ScotchPy import application as app

class SetMetadataApp(Application):
    def __init__(self):     
        super(SetMetadataApp, self).__init__("Set Metadata")       
        self.ffmpeg_exe = os.path.join(self.get_ffmpeg_path(), "ffmpeg.exe") 
    
    def run(self):
        """ Run the application instance in the calling directory. """
        args = self.get_arguments()        
        for input_file in args.input_files:
            parent_folder = None
            if os.path.isfile(input_file) == False:
                raise Exception("Invalid input_file provided [{0}]".format(input_file))
            
            if os.path.isabs(input_file):
                parent_folder = os.path.join(input_file, os.pardir)
            else:
                parent_folder = app.get_root_directory()

            filename = os.path.basename(input_file)
            new_media_file = media_utils.create_media_file(parent_folder, filename)
            if new_media_file.is_movie() or new_media_file.is_tv():
                temp_file = os.path.join(new_media_file.get_destination(), new_media_file.get_filename()+".temp"+new_media_file.get_extension())
                self.log.write("set_title:'{0}', '{1}', '{2}'".format(input_file, temp_file, new_media_file.get_filename()))
                self.set_title(input_file, temp_file, new_media_file.get_filename())   
            else:
                raise Exception("Invalid media file type [{0}]".format(input_file))         

    def get_arguments(self):    
        """ Define and return a list of command line arguments. """
        parser = argparse.ArgumentParser(description="Set Metadata") 
        parser.add_argument(
            "--input_files", 
            "-i", 
            required=True,
            action='append',
            type=str,
            help="The input file to set the metadata for."
            )             
        return parser.parse_args(args=app.get_system_arguments())
        
    def get_ffmpeg_path(self):
        """ Get the movies directory from the configuration file. """
        destination = config.get_value('ffmpeg')
        if destination is None:
            raise Exception("Definition for <ffmpeg> is missing from config.xml")
        else:
            return destination.text

    def set_title(self, source, destination, title):
        """ Set metadata title using ffmpeg utility. """
        if os.path.isfile(self.ffmpeg_exe) == False:
            raise Exception("Executable is missing at [{0}]".format(self.ffmpeg_exe))
        
        (filepath, extension) = os.path.splitext(source)
        cmd = None
        if extension.lower() in (".mkv", ".mov", ".mp4", ".m4a"):        
            cmd = '"{0}" -v 2 -i "{1}" -metadata title="{2}" -n -codec copy "{3}"'.format(self.ffmpeg_exe, source, title, destination)
        elif extension.lower() in (".avi"):        
            cmd = '"{0}" -v 2 -i "{1}" -metadata INAM="{2}" "{3}"'.format(self.ffmpeg_exe, source, title, destination)
        else:
            raise Exception("Unknown file extension [{0}]".format(extension))
        if cmd is not None:
            print("Running the ffmpeg utility, this may take several minutes...")     
            self.log.write("\n{0}\nFFMPEG Utility\n{1}\n{0}\n".format("-"*80, cmd))
            self.log.write("start:{0:%Y-%m-%d %H:%M:%S:%f};\n\n".format(datetime.datetime.now()))               
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
            (out, err) = p.communicate()      
            if out is not None:
                print("out:", out.decode('utf-8'))
            if err is not None:
                print("err:", err.decode('utf-8'))
            self.log.write("end:{0:%Y-%m-%d %H:%M:%S:%f};\n".format(datetime.datetime.now()))
            self.log.write("-"*80+"\n\n")
            if app.query_yes_no("Replace '{0}'?".format(source)):
                if os.path.exists(source):
                    os.remove(source)
                    self.log.write("removed:{0};\n".format(source))
                file_utils.move_file(destination, source)
                self.log.write("moved_from:{0};moved_to:{1};\n".format(destination, source)) 

if __name__ == "__main__":
    try:
        main = SetMetadataApp()
        main.run()            
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        raise
        sys.exit(-1)