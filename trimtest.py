import ffmpeg
import wave
import numpy as np
import math
import struct

du = 0.5
th = 0.02
inputFName = '刘崇恬的电台Oct19-07-45-04'
outputFName = inputFName + '[Trimmed].wav'

# Convert
stream = ffmpeg.input(inputFName + '.mp4')
stream = ffmpeg.output(stream, inputFName + '.wav')
try:
    ffmpeg.run(stream)
except:
    print('Error in converting')

# Read
with wave.open(inputFName + '.wav') as fInput:
    params = fInput.getparams()
    nchannels, sampwidth, framerate, nframes, comptype, compname = params[:6]
    strData = fInput.readframes(nframes)
    waveData = np.fromstring(strData, dtype=np.int16)
    waveData = waveData * 1.0 / (max(abs(waveData)))
    waveData = np.reshape(waveData, [nframes, nchannels])

# Trim
outData = waveData
lenWindow = int(du * framerate)
numWindow = math.floor(nframes / lenWindow)
count = 0
end = nframes
for i in range(0, numWindow + 1):
    tempCh1 = waveData[i * lenWindow:min(lenWindow * (i + 1) - 1, nframes), 0]
    max_value = max(tempCh1)
    if max_value > th:
        count += 1
        start = (count - 1) * lenWindow
        end = start + len(tempCh1)
        outData[start:end, 0] = tempCh1
        outData[start:end, 1] = waveData[i * lenWindow:min(lenWindow * (i + 1) - 1, nframes), 1]
outData = np.resize(outData,(end,2))

# Save
outData = np.reshape(outData,[end * nchannels, 1])
with wave.open(outputFName, 'wb') as outwave:
    outwave.setparams((nchannels, sampwidth, framerate, end, comptype, compname))
    for v in outData:
        outwave.writeframes(struct.pack('h', int(v * 64000 / 2)))  # outData:16位，-32767~32767，注意不要溢出
