import dispComponents as comps
import SynthModel
import random
import pygame
class SynthModule:
  def __init__(self, screen, synthModel):
    self.screen = screen
    self.synthModel = synthModel
    self.paramState = 'a'

    text = "SYNTH2"
    self.titleLabel = comps.Label(self.screen, 36,2,72,text)
    self.paramText1 = "Attack"
    self.paramText2 = "Decay"
    self.paramText3 = "Volume"
    self.paramText4 = "FreqMod"
    self.paramLabel = comps.Label(self.screen, 32, 180, 42, self.paramText1)
  def draw(self):
    self.screen.fill((0,0,0))
    # Draw Title
    self.titleLabel.draw()
    # Draw Parameter Label
    self.paramLabel.draw()
    # Draw Rectangles
    self.drawRects()
    self.synthModel.addNote(60)

  def update(self, args):
    # if
    pass

  def randColor(self, min=0, max=255):
    return (int(random.uniform(min,max)),int(random.uniform(min,max)),int(random.uniform(min,max)) )

  def drawRects(self):
    xoff = 0
    yoff = 64
    w = 32
    h = 32
    rows = 3
    cols = 10
    cell = 0
    for ycell in range(rows):
      for xcell in range(cols):
        rect =(xoff+ w * xcell, yoff + h * ycell, w, h)
        # rcolor = self.randColor()
        rcolor = self.synthModel.colorBlockList[cell]
        pygame.draw.rect(self.screen, rcolor, rect, 0)
        cell = cell + 1

