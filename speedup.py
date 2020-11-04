import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
from scipy.io import wavfile
import os
import glob


def speed_change(in_wav, out_wav, lib_file="./speed_change.dll", speed_rate=2):
    """
    args:
        in_wav: 输入wav文件的路径
        out_wav: 语速改变后wav文件的输出路径
        lib_file: 编译的c代码
        speed_rate: 语速提升多少
    """

    fs, wav = wavfile.read(in_wav) #读取wav文件的采样率和数据
    wav_len = len(wav) # 输入长度
    out_len = round(wav_len/speed_rate) #输出长度

    ## 调用编译好的c库
    lib = ctypes.cdll.LoadLibrary 
    sonic_lib = lib(lib_file) 
    wav_speech_change = sonic_lib.wavChangeSpeed
    wav_speech_change.argtypes = [ndpointer(ctypes.c_short), ndpointer(
        ctypes.c_short), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float]
    wav_speech_change.restypes = None
    result = np.zeros([out_len], dtype=np.int16)
    wav_speech_change(wav, result, 1, fs, wav.shape[0], speed_rate)

    wavfile.write(out_wav, fs, result) # 将变化语速后的数据写成wav文件

    return result

if __name__ == "__main__":
    wav_input = "./test/normal.wav"
    wav_output = "./test/speedup.wav"
    lib_file = "./speed_change.dll"
    ## 编译c代码，生成库
    os.system("gcc -o " + lib_file + " -shared -fPIC runsonic.c sonic.c sonic.h")
    ## 变速
    speed_change(wav_input, wav_output, lib_file="./speed_change.dll")



