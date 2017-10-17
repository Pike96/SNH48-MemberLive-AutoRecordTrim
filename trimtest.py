import wave
import numpy as np

fInput = wave.open('刘崇恬的电台Oct16-08-38.wav')
params = fInput.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = fInput.readframes(nframes)
waveData = np.fromstring(strData,dtype=np.int16)
waveData = waveData*1.0/(max(abs(waveData)))
print(1)