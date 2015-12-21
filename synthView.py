import dispComponents as comps
import SynthModel
import random
import pygame
class SynthView:
  def __init__(self, screen, synthModel):
    self.screen = screen
    self.surface = pygame.Surface((320,240))
    # self.surface = pygame.Surface((320,240), pygame.SRCALPHA)
    # self.surface.fill((255,255,255,128))
    # self.screen.blit( self.surface, (0,0))
    self.model = synthModel

    self.titleLabel = comps.Label(self.surface, 36,2,72,self.model.title)
    self.paramLabel = comps.Label(self.surface, 32, 180, 42, self.model.activeParam)
    self.paramValue = comps.Label(self.surface, 186, 180, 42, self.model.activeParamValue)


    # Draw the inital texture
    self.draw()
  def draw(self):
    if self.model.drawState == "draw":
      self.surface.fill((0,0,0))
      # Draw Title
      self.titleLabel.draw()
      # Draw Parameter Label
      self.updateParamLabel()
      self.paramLabel.draw()
      self.paramValue.draw()
      # Draw Rectangles
      self.drawRects()

      # Blit the surface to the screen
      self.surface.set_alpha(255)
      self.screen.blit(self.surface, (0,0))

      # - - - change state after draw - - -
      self.model.drawState = "dim"
    elif self.model.drawState == "dim":
      self.screen.fill((0,0,0))
      dimCounter = self.model.dimCounter
      dimCMax = self.model.dimCounterMax
      alpha = 255 * (  ( 100.0 - dimCounter ) / 100.0) 
      # alpha = 255 * dimCounter / 100
      self.surface.set_alpha(alpha)
      # Blit the surface to the screen
      self.screen.blit(self.surface, (0,0))
    else : # Paused
      pass

  def update(self, args):
    # if nothing
    pass

  def randColor(self, min=0, max=255):
    return (int(random.uniform(min,max)),int(random.uniform(min,max)),int(random.uniform(min,max)) )

  def redrawParamLabel(self):
    self.paramLabel.draw()
    self.paramValue.draw()
  def updateParamLabel(self):
    self.paramLabel.changeText(self.model.activeParam)
    self.paramValue.changeText(self.model.activeParamValue)
    # print("active param %s and active paramValue %s" % (self.model.activeParam, self.model.activeParamValue) )

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
        rcolor = self.model.colorBlockList[cell]
        pygame.draw.rect(self.surface, rcolor, rect, 0)
        cell = cell + 1

