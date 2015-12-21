import random
import dispComponents as comps
class LongRecModel(object):
  def __init__(self):
    self.runTime = "0:00.00"
    self.ab = "A"
    self.drawState = "draw" # draw, paused
    self.runTimeColor = comps.COLOR.WHITE
  def updateDrawState(self):
    if self.drawState == "draw":
      self.drawState = "paused"
    else :
      self.drawState = "draw"
  def updateRunTime(self, millisecs):
    # time 
    """
    hundredths = millisecs / 10
    hundredths = hundredths % 100
    secs = millisecs / 1000
    secs = secs % 60
    min = millisecs / 60000
    text = str(min) + ":" + str(secs).zfill(2)+"." + str(hundredths).zfill(2)
    """
    text = str(millisecs)
    self.runTime = text
  def makeActive(self):
    self.drawState = "draw"
  def receiveOSC(self, savedOSC):
    pass
  def play(self):
    self.runTimeColor = comps.COLOR.WHITE
  def stop(self):
    self.runTimeColor = comps.COLOR.WHITE
  def record(self):
    self.runTimeColor = comps.COLOR.RED
  def switch(self):
    if self.ab == "A":
      self.ab = "B"
    else :
      self.AB = "A"
  
  
