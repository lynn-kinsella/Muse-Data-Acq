from ctypes import sizeof
from datetime import datetime
import sys
import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from ssqueezepy import ssq_cwt, ssq_stft, cwt
from csv import reader

def viz(x, Tx, Wx):
    plt.imshow(np.abs(Wx), aspect='auto', cmap='turbo')
    plt.show()
    plt.imshow(np.abs(Tx), aspect='auto', vmin=0, vmax=.2, cmap='turbo')
    plt.show()

def load_sample(sample_id):
    data_id = str(sample_id.split("/")[1]) + "_" + str(sample_id.split("/")[2].split(".")[0])
    data = []
    with open(sample_id, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            data.append(row)
    data = np.array(data)
    timestamps, tp9, af7, af8, tp10= data.T
    tp9, af7, af8, tp10 = np.array(list(map(float, tp9))), np.array(list(map(float, af7))), np.array(list(map(float, af8))), np.array(list(map(float, tp10))
)
    start = datetime.strptime(str(timestamps[0]), "%Y-%m-%d %H:%M:%S.%f")
    end = datetime.strptime(str(timestamps[-1]), "%Y-%m-%d %H:%M:%S.%f")
    t = []

    for timestamp in timestamps:
        t.append((datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S.%f") - start).total_seconds())

    print(timestamps[0])
    start = datetime.strptime(str(timestamps[0]), "%Y-%m-%d %H:%M:%S.%f")
    end = datetime.strptime(str(timestamps[-1]), "%Y-%m-%d %H:%M:%S.%f")
    duration = (end-start).total_seconds()
    print("duration: ", duration)
    fs = timestamps.size/duration
    print(fs)

    fig = plt.figure()
    plt.subplot(2,2,1)
    plt.plot(t, tp9)
    plt.title("tp9 time domain")
    plt.subplot(2,2,2)
    plt.plot(t, af7)
    plt.title("af7 time domain")
    plt.subplot(2,2,3)
    plt.plot(t, af8)
    plt.title("af8 time domain")
    plt.subplot(2,2,4)
    plt.plot(t, tp10)
    plt.title("tp10 time domain")
    plt.show()

    plt.subplot(2,2,1)
    Twtp9, Wtp9, *_ = cwt(tp9, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"tp9_cwt.png", np.abs(Twtp9))
    plt.imshow(np.abs(Twtp9), aspect='auto', cmap='turbo')
    plt.title("tp9 cwt")
    
    plt.subplot(2,2,2)
    Twaf7, Waf7, *_ = cwt(af7, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"af7_cwt.png", np.abs(Twaf7))
    plt.imshow(np.abs(Twaf7), aspect='auto', cmap='turbo')
    plt.title("af7 cwt")

    plt.subplot(2,2,3)
    Twaf8, Waf8, *_ = cwt(af8, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"af8_cwt.png", np.abs(Twaf8))
    plt.imshow(np.abs(Twaf8), aspect='auto', cmap='turbo')
    plt.title("af8 cwt")

    plt.subplot(2,2,4)
    Twtp10, Wtp10, *_ = cwt(tp10, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"tp10_cwt.png", np.abs(Twtp10))
    plt.imshow(np.abs(Twtp10), aspect='auto', cmap='turbo')
    plt.title("tp10 cwt")
    plt.show()


    plt.subplot(2,2,1)
    Twtp9, Wtp9, *_ = ssq_cwt(tp9, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"tp9_ssq_cwt.png", np.abs(Twtp9))
    plt.imshow(np.abs(Twtp9), aspect='auto', cmap='turbo')
    plt.title("tp9 ssq_cwt")
    
    plt.subplot(2,2,2)
    Twaf7, Waf7, *_ = ssq_cwt(af7, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"af7_ssq_cwt.png", np.abs(Twaf7))
    plt.imshow(np.abs(Twaf7), aspect='auto', cmap='turbo')
    plt.title("af7 ssq_cwt")

    plt.subplot(2,2,3)
    Twaf8, Waf8, *_ = ssq_cwt(af8, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"af8_ssq_cwt.png", np.abs(Twaf8))
    plt.imshow(np.abs(Twaf8), aspect='auto', cmap='turbo')
    plt.title("af8 ssq_cwt")

    plt.subplot(2,2,4)
    Twtp10, Wtp10, *_ = ssq_cwt(tp10, fs=fs)
    plt.imsave("./processed_signals/"+data_id+"tp10_ssq_cwt.png", np.abs(Twtp10))
    plt.imshow(np.abs(Twtp10), aspect='auto', cmap='turbo')
    plt.title("tp10 ssq_cwt")
    plt.show()



load_sample(sys.argv[1])