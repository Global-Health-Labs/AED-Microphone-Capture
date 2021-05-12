# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:19:20 2021

@author: RyanCalderon
"""


import os
import re
import datetime



# def generate_folder_paths(self, runSelect=None):
#     '''
#     Parameters
#     ----------
#     runSelect : integer value to select RUN folder, should exist
#     '''
#     output = [dI for dI in os.listdir('.') if os.path.isdir(os.path.join('.',dI))]
#     out = ['000']
#     if not runSelect:
#         for dirName in output:
#             out += (re.findall('\d+', dirName ))
            
#         run_num = int(max(out)) + 1
#     else:
#         run_num = runSelect
                
#     # format with leading zeros
#     self.run_number = str(run_num).zfill(3)
    
#     runFolder = 'trial_run_{}'.format(self.run_number)
    
#     if not runFolder:
#         os.makedirs (runFolder)

        
    # # create paths
    # self.train_path = os.path.join(runFolder,'train')
    # if not os.path.isdir(self.train_path):
    #     os.makedirs (self.train_path)
    # self.prediction_path = os.path.join(runFolder,'prediction')
    # if not os.path.isdir(self.prediction_path):
    #     os.makedirs (self.prediction_path)
    # self.results_path = os.path.join(runFolder,'results')
    # if not os.path.isdir(self.results_path):
    #     os.makedirs (self.results_path)
    
def generate_folder_paths():
    
    toppath = '../audio-datasets/'
    unlabeled = 'unlabeled/'
    if not os.path.isdir(toppath):
        os.makedirs(toppath)
        os.makedirs(toppath + unlabeled)
        
    return toppath + unlabeled
    
    
    
def generate_run_id(file_path):
    output = [dI for dI in os.listdir(file_path) if os.path.isfile(os.path.join(file_path,dI))]
    out = ['0000']
    for dirName in output:
        out += (re.findall('\d+', dirName ))
    run_num = int(max(out)) + 1
    
    return str(run_num).zfill(4)
    
    
    
def create_meta(audioFormat : dict, sampleId) -> dict:
    
    # translation from pyaudio
    bitdepth = {
        16 : 8,
        8 : 16,
        4 : 24,
        2 : 32}
    
    meta_file = dict({
        'bitdepth':bitdepth[audioFormat['FORMAT']],
        'bitrate': None,
        'channels': audioFormat['CHANNELS'],
        'samplerate': audioFormat['RATE'],
        'duration' : None,
        'filesize' : None,
        'duration' : None,
        'geotag' : None,
        'id' : sampleId,
        'description' : None,
        'microphone_description': audioFormat['MICROPHONES_DESCRIPTION'],
        'created' : datetime.datetime.now(datetime.timezone.utc).isoformat(sep=' ')
    })
    
    return meta_file

    