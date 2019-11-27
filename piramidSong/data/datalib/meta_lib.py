#! /usr/bin/python3 -i

import sys

import os
cwd = os.getcwd()

cwd = '/'.join(cwd.split('/')[:-1])

def add_to_path(str):
    try:
        sys.path.index(str)
    except:
        sys.path.append(str)
        print(str + "\t add to the path list")
    else:
        print(str + "\t is already in the path list")

# this add all the libraris and scripts made for this project

add_to_path( cwd + "/datalib/")
add_to_path( cwd + "/khinsider-master/")
add_to_path( cwd + "/hilbert_curve/")

import wave
import numpy as np
import scipy as sp

from matplotlib import pyplot as plt

import pprint
import struct

import pandas as pd

import time

import threading


def stereo_chanel_data(wav_obj_pointer, verbose=False):
    wav_obj_pointer.rewind()
    
    signed_data_l = []
    signed_data_r = []

    total_frames = wav_obj_pointer.getnframes()
    amount = 0

    for frame_index in range(1 , total_frames - 1, 1):
        wav_obj_pointer.setpos(frame_index)

        try:
            l_int = struct.unpack("<h",wav_obj_pointer.readframes(1)[:2])[0]
            r_int = struct.unpack("<h",wav_obj_pointer.readframes(1)[-2:])[0]

        except:
            if verbose:
                print("error with frame \t" , frame_index , " N_CHANEL_DATA ERROR \n")
        else:
            signed_data_l.append(l_int)
            signed_data_r.append(r_int)

            if frame_index % (44100*20) == 0 and verbose:
                print(round((frame_index / total_frames) * 100, 4), "\t%")
                print(l_int, "\t", r_int)
                print(len(signed_data_l), "\t", len(signed_data_r))

    return [signed_data_l, signed_data_r]

def mono_chanel_data(wav_obj_pointer, verbose=False):
    wav_obj_pointer.rewind()
    
    signed_data = []

    total_frames = wav_obj_pointer.getnframes()
    amount = 0

    for frame_index in range(1 , total_frames - 1, 1):
        wav_obj_pointer.setpos(frame_index)

        try:
            g_int = struct.unpack("<h",wav_obj_pointer.readframes(1)[:2])[0]
        except:
            if verbose:
                print("error with frame \t" , frame_index , " N_CHANEL_DATA ERROR \n")
        else:
            signed_data.append(g_int)

            if frame_index % (44100*20) == 0 and verbose:
                print(round((frame_index / total_frames) * 100, 4), "\t%")
                print(l_int, "\t", r_int)
                print(len(signed_data_l), "\t", len(signed_data_r))

    return signed_data

def sound_csv(files, basic_verbose = False, verbose=False):
    
    for index in range(len(files)):
        
        if verbose:
            print(files[index][1], "\t in execution at : \t 0 % and going")
        elif basic_verbose:
            print(files[index][1], "\t in execution with index\t", index)
        else:
            pass
            
        [sound_obj_ref , sound_name] = files[index]
        
        data_l_r = stereo_chanel_data(sound_obj_ref, verbose)
        
        carry_data = np.matrix(data_l_r).T
        
        sound_frame_data = pd.DataFrame(carry_data, columns=["left", "rigth"])
                
        sound_frame_data.to_csv( (DATA_PATH + sound_name[:-4] + ".csv"), sep='\t', encoding='utf-8')
        
        if verbose or basic_verbose:
            print("\n", sound_name , "\tDONE\n")

            
def meta_data(files, path, verbose=False):
    specs_matrix = []
    
    for index in range(len(files)):
        if verbose:
            print(files[index][1], "\t in transcription")
        else:
            pass
        
        [sound_obj_ref , sound_name] = files[index]
        
        specs_matrix.append([sound_name] + list(sound_obj_ref.getparams()))
        
        if verbose:
            print("\n", sound_name , "\tDONE\n")
    
    meta_sound_data = pd.DataFrame(specs_matrix, columns=
                                   ["file name", "nchannels", "sampwidth", "framerate", "nframes", "comptype", "compname"])
                
    meta_sound_data.to_csv( (path + "meta_sound_data.csv"), sep='\t', encoding='utf-8')
    
def data_2_wav(data, specs, path, verbose=False):
    os.system("touch " + path)
    if verbose:
        print("creating destination file\t" + path)
    
    try:           
        output.close()
    except:
        if verbose:
            print("alocating file")
            
        output = wave.open(path, 'w')
    else:
        output = wave.open(path, 'w')
        if verbose:
            print("file already exists")
    
    if verbose:
            print("setting sound specs")
    
    specs[0] = 1
    specs[3] = len(data)
    
    output.setparams(specs)
    
    if verbose:
        print("formating data...")
        
    _carry = []
    for ii in list(data):
        _carry.append(struct.pack('<h', ii))

    _carry = b''.join(_carry)
    
    if verbose:
            print("writing...")
    
    output.writeframes(_carry)
    
    output.close()
    
    if verbose:
        print("DONE")
        
def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255
    return [int(R), int(G), int(B)]

def Int2nM(x, rang_vals, verbose = False):
    [min_val, max_val] = rang_vals
    THz_o = 380.0
    THz_f = 750.0
    
    d = THz_f - THz_o
    d_val = max_val - min_val
    
#     x = x / (10 ** 12)
    
    ratio = (d / d_val)
    
    if verbose:
        print(x) 
        print(ratio)
    
    x = (x - min_val) * ratio + THz_o
    
    if verbose:
        print(x)
    
    return x