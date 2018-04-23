"""
    Sort Downloads
"""
import argparse
import os, string, shutil, sys, errno, time, filecmp, subprocess, datetime

from ScotchPy.utils import media_utils, file_utils, folder_utils
from ScotchPy import config
from ScotchPy.application import Application, get_root_directory, get_system_arguments

class SetMetadataApp(Application):
    def __init__(self):     
        super(SetMetadataApp, self).__init__("Set Metadata")       
        self.ffmpeg_exe = os.path.join(self.get_ffmpeg_path(), "ffmpeg.exe") 
    
    def run(self):
        """ Run the application instance in the calling directory. """
        args = self.get_arguments()

        if os.path.isfile(args.input_file) == False:
            raise Exception("Invalid input_file provided [{0}]".format(args.input_file))      

        parent_folder = os.path.join(args.input_file, os.pardir)
        filename = os.path.basename(args.input_file)
        new_media_file = media_utils.create_media_file(parent_folder, filename)
        if new_media_file.is_movie() or new_media_file.is_tv():
            temp_file = os.path.join(new_media_file.get_destination(), new_media_file.get_filename()+".temp"+new_media_file.get_extension())
            self.log.write("set_title:'{0}', '{1}', '{2}'".format(args.input_file, temp_file, new_media_file.get_filename()))
            self.set_title(args.input_file, temp_file, new_media_file.get_filename())            

    def get_arguments(self):    
        """ Define and return a list of command line arguments. """
        parser = argparse.ArgumentParser(description="Set Metadata") 
        parser.add_argument(
            "--input_file", 
            "-i", 
            required=True,
            help="The input file to set the metadata for."
            )             
        return parser.parse_args(args=get_system_arguments())
        
    def get_ffmpeg_path(self):
        """ Get the movies directory from the configuration file. """
        destination = config.get_value('ffmpeg')
        if destination is None:
            raise Exception("Definition for <ffmpeg> is missing from config.xml")
        else:
            return destination.text

    def set_title(self, source, destination, title):
        """ """
        if os.path.isfile(self.ffmpeg_exe) == False:
            raise Exception("Executable is missing at [{0}]".format(self.ffmpeg_exe))
        
        filepath, extension = os.path.splitext(source)
        cmd = None
        if extension.lower() in (".mkv", ".mov", ".mp4", ".m4a"):        
            cmd = '"{0}" -i "{1}" -metadata title="{2}" -n -report -codec copy "{3}"'.format(self.ffmpeg_exe, source, title, destination)
        elif extension.lower() in (".avi"):        
            cmd = '"{0}" -i "{1}" -metadata INAM="{2}" "{3}"'.format(self.ffmpeg_exe, source, title, destination)
        if cmd is not None:     
            self.log.write("\n{0}\nFFMPEG Utility\n{1}\n{0}\n".format("-"*80, cmd))
            self.log.write("start:{0:%Y-%m-%d %H:%M:%S:%f};\n\n".format(datetime.datetime.now()))               
            output, error = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)              
            if output is not None:                                  
                for b in output.decode("utf-8"):
                    self.log.write(str(b))         
            self.log.write("\n\n")
            self.log.write("end:{0:%Y-%m-%d %H:%M:%S:%f};\n".format(datetime.datetime.now()))
            self.log.write("-"*80+"\n\n")
            if os.path.exists(source):
                os.remove(source)
                self.log.write("removed:{0};\n".format(source))
            shutil.move(destination, source)
            self.log.write("moved_from:{0};moved_to:{1};\n".format(destination, source)) 

if __name__ == "__main__":
    try:
        app = SetMetadataApp()
        app.run()            
        sys.exit(0)
    except Exception as ex:
        print("Error:", str(ex), "\n")
        raise
        sys.exit(-1)