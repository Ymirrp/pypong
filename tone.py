from random import sample
from time import time, sleep
import pygame
from pygame.mixer import Sound, get_init, pre_init
from array import array
 
class Tone(Sound):
  def __init__(self, freq, vol=0.1):
    self.freq = freq
    Sound.__init__(self, self.build_samples())
    self.set_volume(vol)
  
  def build_samples(self):
    period = int(round(get_init()[0] / self.freq))
    samples = array('h', [0] * period)
    amp = 2 ** (abs(get_init()[1]) - 1) - 1
    
    for time in range(period):
      if time < period / 2:
        samples[time] = amp
      else:
        samples[time] = -amp
    return samples
  
if __name__ == '__main__':
  pre_init(44100, -16, 1, 1024)
  pygame.init()
  Tone(288).play(16)
  sleep(.5)
  Tone(288).play(16)
  sleep(.5)
  Tone(72).play(32)
  sleep(1)
