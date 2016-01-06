# The Display Modules Manager System
# Uses pygame as the display library
# displays to /dev/fb1
#
# It creates the Modules for
# Synth, Seq, Drum ...
# Essentially the controller ??
# Maybe also Routes input

import os
import pygame
import time, random, string
# from dispComponents import DLabel
import dispComponents as comps
import recMod
import synthView
import SynthModel
import SynthVC
import longRecView, longRecModel, longRecController


class LcdDisp:
  screen = None
  WHITE = (255, 255, 255)
  BLUE = (0, 0, 255)
  GRAY = (127, 127, 127)
  DGRAY = (64,64,64)
  BLACK = (0, 0, 0)
  RED = (255, 0, 0)
  synthModeTxt = "Hello, Enjoy"
  color = (255,255,255)
  seqMod = None
  def __init__(self):
    os.environ["SDL_FBDEV"]= "/dev/fb1"
    pygame.init()
    size = (320,240)
    self.screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SynOs Disp Experiment 7.12.15")
    #turn off audio so that pd can grab audio focus
    pygame.mixer.quit()
    # hide mouse coursor
    pygame.mouse.set_visible(False)
    
    # Components test here
    self.seqMod = comps.SeqModule(self.screen)
    self.visMod = comps.visModule(self.screen)

    # Modules go here
    self.recMod = recMod.RecModule(self.screen)

    self.synthModel = SynthModel.SynthModel()
    self.synthView = synthView.SynthView(self.screen, self.synthModel)
    self.synthController = SynthVC.SynthViewController(self.synthModel, self.synthView)
    self.activeModuleController = self.synthController

    # Long Rec View
    self.longRecModel = longRecModel.LongRecModel()
    self.longRecView = longRecView.LongRecView(self.screen, self.longRecModel)
    self.longRecController = longRecController.LongRecController(self.longRecModel, self.longRecView)
  def visModTest(self):
    self.visMod.draw()

  def setState(self, savedOSC):
    self.savedOSC = savedOSC

  def updateNewSequencer(self):
    self.seqMod.update(self.savedOSC.path, self.savedOSC.args)
  def drawNewSequencer(self):
    self.seqMod.draw()

  def drawRecMod(self):
    self.recMod.draw()

  def updateRecorder(self):
    self.recMod.update(self.savedOSC.args)
  def drawRecorder(self):
    self.recMod.draw()

  def drawNewSynth(self):
    self.synthView.draw()

  def updateAndRouteOSC(self, path, tags, args):
    # if path is synth route to synth
    if (string.split(path, "/")[1] == "synth"):
      # update synthModel via synthController
      pass
    

  def update(self):
    # - - - - New Functions - - - - - 
    # update witch module is active 
    # based on last OSC recieved
    # 
    # send active module a CPU Tick via module.update()
    # each module figures out if module needs to draw
    # based on its own state
    
    # - - - - - -
    # Route OSC based on first address container
    # - - - - - -
    if self.savedOSC.fresh == "hot":
      selected = string.split(self.savedOSC.path, "/")[1]
      # s = synth, d = drums, t = tape, q = synth, r = longRecord
      if selected == "s":
        self.activeModuleController = self.synthController
        self.activeModuleController.receiveOSC(self.savedOSC)
      elif selected == "d":
        self.drawDrums()
        self.activeModuleController = None
      elif selected == "t":
        self.activeModuleController = None
        self.updateRecorder()
        self.drawRecorder()
      elif selected == "q":
        self.activeModuleController = None
        self.updateNewSequencer()
        self.drawNewSequencer()
      elif selected == "r":
        self.activeModuleController = self.longRecController
        self.longRecController.receiveOSC(self.savedOSC)
      self.savedOSC.setCold()

    if (self.activeModuleController != None):
      self.activeModuleController.CPUTick()
    """
    # route osc -bad
    # - -rename state to saved OSC
    if self.savedOSC.fresh == "hot":
      if self.savedOSC.txt == "/d":
        self.drawDrums()
        self.activeModuleController = None
      elif self.savedOSC.txt == "/s":
        self.activeModuleController = self.synthController
        self.activeModuleController.receiveOSC(self.savedOSC)
        # self.drawNewSynth()
        # self.drawSynth()
      elif self.savedOSC.txt == "/s/k1":
        self.activeModuleController = self.synthController
        self.activeModuleController.receiveOSC(self.savedOSC)
      elif self.savedOSC.txt == "/s/k2":
        self.activeModuleController = self.synthController
        self.activeModuleController.receiveOSC(self.savedOSC)
      elif self.savedOSC.txt == "/s/k3":
        self.activeModuleController = self.synthController
        self.activeModuleController.receiveOSC(self.savedOSC)
      elif self.savedOSC.txt == "/s/k4":
        self.activeModuleController = self.synthController
        self.activeModuleController.receiveOSC(self.savedOSC)
      elif self.savedOSC.txt == "/q":
        self.activeModuleController = None
        self.updateNewSequencer()
        self.drawNewSequencer()
      elif self.savedOSC.txt == "/r":
        self.activeModuleController = None
        self.updateRecorder()
        self.drawRecorder()
      self.savedOSC.setCold()
    """

  def drawHello(self):
    self.screen.fill((0,0,0))
    # draw stuff here
    font = pygame.font.SysFont('Calibri', 72, True, False)
    textSurf = font.render(self.synthModeTxt, True, self.color)
    self.screen.blit(textSurf, [20,20])

  def drawScreen(self):
    # update the display
    pygame.display.update()

  def drawDrums(self):
    self.screen.fill(self.BLACK)
    self.synthModeTxt = "DRUMZ"
    self.drawTextAt(69,2,txt="DRUMZ")
    self.drawCircles()

  def drawCircles(self):
    pad = 8 #left and top
    pad2 = 16 #right and bottom

    xoff = 0
    yoff = 64

    w = 64
    h = 64
    headH = 48
    rows = 2
    cols = 10
    for ycell in range(rows):
      for xcell in range(cols):
        rect =(xoff+ w * xcell + pad, yoff + h * ycell + headH/2 , w - pad2, h - headH)
        
        #outlineRect = (xoff+ w * xcell, yoff + h * ycell, w, h)
        headRect = (xoff+ w * xcell + pad, yoff + h * ycell + pad, w - pad2, headH - pad2)
        
        bottomRect = (xoff+ w * xcell + pad, yoff + h * ycell + pad + pad2, w - pad2, headH - pad2)
        rcolor = self.randColor()

        # Draw Bottom
        pygame.draw.ellipse(self.screen, rcolor, bottomRect, 0)
        pygame.draw.rect(self.screen, rcolor, rect, 0)
        #pygame.draw.rect(self.screen, rcolor, outlineRect, 1)
        headColor = self.scaleColor(rcolor, 1.50)
        pygame.draw.ellipse(self.screen, headColor, headRect, 0)
  
  
  def drawSequencer(self, seq=0):
    self.screen.fill(self.BLACK)
    self.synthModeTxt = "SEQUENCER"
    text = "SEQUENCER"
    self.drawTextAt(4,2,72,text)

    state = 0
    seq = 14
    self.drawSeqButs()
    self.drawSeqNum(seq)
    dur = 250
    self.drawSeqDur(dur)

  def drawSeqNum(self, seq=12):
    text = str(seq)
    x = 64
    y = 32
    sz = 288
    self.drawTextAt(x,y,sz,text)
  def drawSeqDur(self, dur=250):
    x = 0 + 16
    y = 172 + 32  
    text = str(dur)
    self.drawTextAt(x,y,size=32,txt=text,color=self.RED)

  def drawGrid(self, cellSize=32):
    w = 320
    h = 240
    cols = w / cellSize + 1
    rows = h / cellSize + 1
    color = self.WHITE

    for row in range(rows):
      x = 0
      x2 = w
      y = row * cellSize
      y2 = y
      pygame.draw.line(self.screen, color, (x,y), (x2, y2))
    for col in range(cols):
      x = col * cellSize
      y = 0
      x2 = x
      y2 = h
      pygame.draw.line(self.screen, color, (x,y), (x2,y2))

  def drawSeqButs(self, state=0):
    # Record Button
    recOutline = 0
    rx = 32
    ry = 96
    width = 16
    color = self.RED
    pygame.draw.circle(self.screen,  color, (rx,ry), width, 0)
    
    # Play Button
    playOutline = 0
    px = 16
    py = 142
    pad = 4
    #triangle = ( (8, 8), (24,16), (8, 24) )
    triangle = ( ( px + pad , py  ), ( px + 32 - pad, py + 16 ), ( px + pad , py + 32 ) )

    pygame.draw.polygon(self.screen, color, triangle)

    button = comps.Button(self.screen, (132,196))
    button.draw()

  def scaleColor(self,color, scale):
    newColor = ()
    for part in color:
      newPart = part * scale
      if newPart > 255:
        newPart = 255
      elif newPart < 0:
        newPart = 0
      newColor = newColor + (newPart,)
    return newColor

  def randColor(self, min=0, max=255):
    return (int(random.uniform(min,max)),int(random.uniform(min,max)),int(random.uniform(min,max)) )

  def drawTextAt(self, x, y, size=72,txt="???", color=(255,255,255)):
    font = pygame.font.SysFont("Calibri", size, True, False)
    textSurf = font.render(txt, True, color)
    self.screen.blit(textSurf, [x,y])


