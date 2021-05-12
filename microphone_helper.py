# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:43:37 2021

@author: RyanCalderon
"""

import argparse
import pyaudio


audio_formats = dict({
    'v1':{
        # Variables
        'FORMAT' : pyaudio.paInt16,
        'CHANNELS' : 1,
        'RATE' : 16000,
        'CHUNK' : 1024,#16000,
        'MICROPHONES_DESCRIPTION' : [],
        'extract_channel' : 0
        # 'FPS' : 60.0,
        # 'OUTPUT_LINES' : 33
    },
    'v2': {
        # Variables
        'FORMAT' : pyaudio.paInt16,
        'CHANNELS' : 6,
        'RATE' : 16000,
        'CHUNK' : 16000,
        'MICROPHONES_DESCRIPTION' : [],
        'extract_channel' : 0
        },
    'v3': {
        # Variables
        'FORMAT' : pyaudio.paInt16,
        'CHANNELS' : 2,
        'RATE' : 44100,
        'CHUNK' : 44100,
        'MICROPHONES_DESCRIPTION' : [],
        'extract_channel' : 0
        }
})

# PyAudio Microphone List
def list_microphones():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    MICROPHONES_LIST = []
    MICROPHONES_DESCRIPTION = []
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            desc = "# %d - %s" % (i, p.get_device_info_by_host_api_device_index(0, i).get('name'))
            MICROPHONES_DESCRIPTION.append(desc)
            MICROPHONES_LIST.append(i)
    
    output = []
    output.append("=== Available Microphones: ===")
    output.append("\n".join(MICROPHONES_DESCRIPTION))
    output.append("======================================")
    return "\n".join(output),MICROPHONES_DESCRIPTION,MICROPHONES_LIST

    

def select_microphone():
    
    output,desc,l = list_microphones()
    print(output)
    ###########################
    # Check Microphone
    ###########################
    print("=====")
    print("1 / 2: Checking Microphones... ")
    print("=====")
    
    desc, mics, indices = list_microphones()
    if (len(mics) == 0):
        print("Error: No microphone found.")
        exit()
    
    #############
    # Read Command Line Args
    #############
    MICROPHONE_INDEX = indices[0]
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mic", help="Select which microphone / input device to use")
    args = parser.parse_args()
    try:
        if args.mic:
            MICROPHONE_INDEX = int(args.mic)
            print("User selected mic: %d" % MICROPHONE_INDEX)
        else:
            mic_in = input("Select microphone [%d]: " % MICROPHONE_INDEX).strip()
            if (mic_in!=''):
                MICROPHONE_INDEX = int(mic_in)
    except:
        print("Invalid microphone")
        exit()
    
    # Find description that matches the mic index
    mic_desc = ""
    for k in range(len(indices)):
        i = indices[k]
        if (i==MICROPHONE_INDEX):
            mic_desc = mics[k]
    print("Using mic: %s" % mic_desc)
    
    return MICROPHONE_INDEX,mic_desc