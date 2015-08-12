import os
import pygame
import time, random

class DispSys:
  screen = None
  WHITE = (255, 255, 255)
  BLUE = (0, 0, 255)
  GRAY = (127, 127, 127)
  DGRAY = (64,64,64)
  BLACK = (0, 0, 0)
  RED = (255, 0, 0)
  synthModeTxt = "Hello, Enjoy"
  color = (255,255,255)

  def __init__(self):
    os.environ["SDL_FBDEV"]= "/dev/fb1"
    pygame.init()
    size = (320,240)
    self.screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SynOs Disp Experiment 7.12.15")
    pygame.mixer.quit()

  def test(self):
    self.screen.fill((0,0,0))
    # draw stuff here
    font = pygame.font.SysFont('Calibri', 72, True, False)
    textSurf = font.render(self.synthModeTxt, True, self.color)
    self.screen.blit(textSurf, [20,20])

  def update(self):
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
  


  def drawSynth(self):
    #self.screen.fill(self.DGRAY)
    self.screen.fill(self.BLACK)
    rect = (0,0, 320, 64)
    #pygame.draw.rect(self.screen, self.BLACK, rect, 0)
    self.synthModeTxt = "SYNTH"
    self.drawTextAt(69,2,txt="SYNTH")
    self.drawRects()

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


  def drawRects(self):
    xoff = 0
    yoff = 64
    w = 32
    h = 32
    rows = 3
    cols = 10
    for ycell in range(rows):
      for xcell in range(cols):
        rect =(xoff+ w * xcell, yoff + h * ycell, w, h)
        rcolor = self.randColor()
        pygame.draw.rect(self.screen, rcolor, rect, 0)

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


