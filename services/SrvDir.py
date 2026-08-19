import os

class SrvDir:  

    dir_main = os.getcwd()
    dir_file_storage = os.path.join(dir_main, 'file_storage')
    dir_recording_out = os.path.join(dir_main, dir_file_storage, 'recording_out')



SrvDir = SrvDir()