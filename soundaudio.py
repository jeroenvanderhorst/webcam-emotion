
import sounddevice as sd
import numpy as np

def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print (volume_norm)

with sd.Stream(callback=print_sound):
    sd.sleep(5000)


