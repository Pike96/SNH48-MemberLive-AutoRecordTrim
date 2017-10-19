import wave
import numpy as np
import math

du = 0.5
th = 0.02

with wave.open('test2.wav') as fInput:
    params = fInput.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = fInput.readframes(nframes)
    waveData = np.fromstring(strData, dtype=np.int16)
    waveData = waveData * 1.0 / (max(abs(waveData)))
    waveData = np.reshape(waveData, [nframes, nchannels])

outData = waveData
window = int(du * framerate)
num_times = math.floor(nframes / window)
count = 0
number = 0
for i in range(0, num_times + 1):
    start = i * window
    end = min(window * (i + 1) - 1, nframes)
    time = waveData[i * window:min(window * (i + 1) - 1, nframes), 0]
    #data = waveData[:, 0]
    #arr = range(i * time_length, min(time_length * (i + 1) - 1, nframes))
    #time = np.take(waveData[:,0], arr)
    max_value = max(time)
    if max_value > th:
        count = count + 1
        start = (count - 1) * window
        end = start + len(time)
        outData[start:end, 0] = time
        outData[start:end, 1] = waveData[i * window:min(window * (i + 1) - 1, nframes), 1]
x = outData[:end, 0]
x2 = outData[:end, 1]
outData = np.resize(outData,(end,2))
print(1)