import time
import picamera
import numpy as np
import keyboard

class Imageifier:
  def __init__(self,file,startupDelay = 2,delay = 0.01,resolution = (1024,768),preveiw = False,framerate = 60):
    self.File = file
    self.Delay = startupDelay
    self.Delay2 = delay
    self.Resolution = resolution
    self.Preview = preveiw
    self.Framerate = framerate
  def TakeImage(self):
    with picamera.Picamera as camera:
      camera.resolution = self.Resolution
      if(self.Preveiw):
        camera.start_preview()
      time.sleep(self.Delay)
      out = np.empty(self.Resolution,dtype = np.uint8)
      camera.capture(out,'rgb')
      np.save(self.File+".npy",out)
  def VideoLoop(self,Object,Exit):
    with picamera.Picamera as camera:
      camera.resolution = self.Resolution
      camera.framerate = self.Framerate
      if (self.Preveiw):
        camera.start_preveiw()
      time.sleep(self.Delay)
      camera.start_recording(Object,format = 'rgb')
      while not Exit.Value:
        donothingvar = 0
        Exit.Update()
      camera.stop_recording()
  def ImageLoop(self,Object,Exit):
    with picamera.Picamera as camera:
      camera.resolution = self.Resolution
      camera.framerate = self.Framerate
      time.sleep(self.Delay)
      while not Exit.Value:
        out = np.empty(self.Resolution,dtype = np.uint8)
        camera.capture(out,'rgb')
        Object.run(out)
        time.sleep(self.Delay2)
class Exit:
  def __init__(self):
    self.starttime = time.time()
    self.Value = False
    self.MAX = 60*5 #five minutes
  def Update(self):
    if ((time.time()-self.starttime)>self.MAX):
      self.Value = True
    elif (keyboard.is_pressed('q')):
      self.Value = True
