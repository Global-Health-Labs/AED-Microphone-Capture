# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:54:58 2021

@author: RyanCalderon
"""

# -*- coding: utf-8 -*-
'''recorder.py
Provides WAV recording functionality via two approaches:
Blocking mode (record for a set duration):
>>> rec = Recorder(channels=2)
>>> with rec.open('blocking.wav', 'wb') as recfile:
...     recfile.record(duration=5.0)
Non-blocking mode (start and stop recording):
>>> rec = Recorder(channels=2)
>>> with rec.open('nonblocking.wav', 'wb') as recfile2:
...     recfile2.start_recording()
...     time.sleep(5.0)
...     recfile2.stop_recording()
'''
import pyaudio
import wave
import numpy as np

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    rate – Sampling rate
    channels – Number of channels
    format – Sampling size and format. See PortAudio Sample Format.
    input – Specifies whether this is an input stream. Defaults to False.
    input_device_index – Index of Input Device to use. Unspecified (or None) uses default device. Ignored if input is False.
    frames_per_buffer – Specifies the number of frames per buffer.
    
    '''
    
    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024, paFormat=pyaudio.paInt16, input_device_index = None):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.format = paFormat
        self.input_device_index = input_device_index

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer,self.format,self.input_device_index)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer,paFormat,input_device_index):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.format = paFormat
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None
        self.MICROPHONE_INDEX = input_device_index

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=self.format,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=self.format,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        input_device_index=self.MICROPHONE_INDEX,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            #self.wavefile.writeframes(b''.join(np.fromstring(in_data,dtype=np.int16)))
            self.wavefile.writeframes(in_data)
            #self.wavefile.writeframes(b''.join(np.fromstring(in_data,dtype=np.int16)[0::6]))
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self.wavefile.close()
        self._pa.terminate()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(self.format))
        wavefile.setframerate(self.rate)
        return wavefile