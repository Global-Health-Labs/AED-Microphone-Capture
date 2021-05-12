# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:47:04 2021

@author: RyanCalderon
"""
import sys
sys.path.append('../ubicoustics/')
import microphone_helper
import pyaudio
import wave
import recorder
import utils

import json
# import signal

# from pathlib import Path
# import time
# import argparse
# import wget
import os
# from reprint import output
# from helpers import Interpolator, ratio_to_db, dbFS, rangemap
# import numpy as np


audioFormat = microphone_helper.audio_formats['v3']
MICROPHONE_INDEX,audioFormat['MICROPHONES_DESCRIPTION'] = microphone_helper.select_microphone()


# add mic_desc and audioFormat to META FILES


def playback(filename):
    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(audioFormat['CHUNK'])
    
    while data != '':
        stream.write(data)
        data = wf.readframes(audioFormat['CHUNK'])
        
    stream.stop_stream()
    stream.close()
    
    p.terminate()



# def keyboardInterruptHandler(signal, frame):
#     print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
#     exit(0)

# signal.signal(signal.SIGINT, keyboardInterruptHandler)
            
##############################
# Main Execution

# generate meta files
#file_path = 'C:/Users/RyanCalderon/OneDrive - Global Health Labs/Documents/Projects/Event Generated Data/exploritory-clinic-sensors/Software/Audio based sensors/audio-datasets/unlabeled'

file_path = utils.generate_folder_paths()


# find RUN id, based on data folder
sampleId = utils.generate_run_id(file_path)

# create meta data file
meta = utils.create_meta(audioFormat = audioFormat, sampleId = sampleId)

rec = recorder.Recorder(rate=audioFormat['RATE'],channels=audioFormat['CHANNELS'],paFormat=audioFormat['FORMAT'],frames_per_buffer=audioFormat['CHUNK'],input_device_index=MICROPHONE_INDEX)
try:
    recFile = rec.open('{}.wav'.format(os.path.join(file_path,sampleId)), 'wb')
    recFile.start_recording()
    while True:
        pass
except KeyboardInterrupt:
    print('Interrupted')

recFile.close()
      
# metafile = open('{}.json'.format(os.path.join(file_path,sampleId)), "w")
# metafile.write(json.dumps(meta, indent=4, sort_keys=True))
# metafile.close()

# # update meta data file
with open('{}.json'.format(os.path.join(file_path,sampleId)), 'w') as f:
    json.dump(meta,f)