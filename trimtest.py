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
lenWindow = int(du * framerate)
numWindow = math.floor(nframes / lenWindow)
count = 0
for i in range(0, numWindow + 1):
    tempCh1 = waveData[i * lenWindow:min(lenWindow * (i + 1) - 1, nframes), 0]
    max_value = max(tempCh1)
    if max_value > th:
        count = count + 1
        start = (count - 1) * lenWindow
        end = start + len(tempCh1)
        outData[start:end, 0] = tempCh1
        outData[start:end, 1] = waveData[i * lenWindow:min(lenWindow * (i + 1) - 1, nframes), 1]
outData = np.resize(outData,(end,2))
print(1)
