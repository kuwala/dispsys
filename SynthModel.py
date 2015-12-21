import random

class SynthModel(object):
  def __init__(self):
    self.title = "SynthV"
    self.param1 = "Attack"
    self.param2 = "Decay"
    self.param3 = "Volume"
    self.param4 = "ModFreq"
    self.attack = 40
    self.decay = 50
    self.volume = 100
    self.modFreq = 1
    self.activeParam = self.param1
    self.activeParamValue = self.attack

    self.noteList = [60,60]
    self.colorBlockList = []
    self.initColorBlocks()

    self.drawState = "draw" # draw, dim, paused
    self.dimCounter = 0
    self.dimCounterMax = 50
  def randColor(self):
    color = ( random.randint(0,255), random.randint(0,255), random.randint(0,255) )
    return color
  def setAttack(self, newAttack):
    if (newAttack > 0):
      self.attack = newAttack
  def initColorBlocks(self):
    for x in range(0,30):
      self.colorBlockList.append((30,30,30))
  def changeParam(self, param, value):
    if (param == "Attack"):
      self.activeParam = self.param1
      self.attack = value
      self.activeParamValue = self.attack
    elif (param == "Decay"):
      self.activeParam = self.param2
      self.decay = value
      self.activeParamValue = self.decay
    elif (param == "Volume"):
      self.activeParam = self.param3
      self.volume = value
      self.activeParamValue = self.volume
    elif (param == "ModFreq"):
      self.activeParam = self.param4
      self.modfreq = value
      self.activeParamValue = self.modfreq

  def addNote(self, note):
    self.colorBlockList.append(self.randColor())
    while len(self.colorBlockList) > 30:
      self.colorBlockList.pop(0)
    self.makeActive()

  def makeActive(self):
    # Makes the view redraw this frame
    self.drawState = "draw"
    self.dimCounter = 0
  def CPUTick(self):
    # - - - - an update() - - - - 
    # Receive CPU Tick
    # based on state figure out it
    # needs to draw or not

    # Test draw on osc recieved then slowly fade and pause
    pass
  def updateDrawState(self):
    if (self.drawState == "draw"):
      self.drawState = "dim"
    elif (self.drawState == "dim"):
      self.dimCounter += 1
      if self.dimCounter >= self.dimCounterMax:
        self.dimCounter = 0
        self.drawState = "paused"
    # print(self.drawState)
