import pygame
import dispComponents as comps

class LongRecView(object):
  def __init__(self, screen, longRecModel):
    self.screen = screen
    self.surface = pygame.Surface((320,240))
    self.title = comps.Label(self.surface, 32, 2, 74, "Record")
    self.model = longRecModel
    rtx = 48
    rty = 92
    rtsize = 72
    rttext = "2:23"
    self.runTimeLabel = comps.Label(self.surface, rtx, rty, rtsize, rttext)
    self.paramLabel = comps.Label(self.surface,  16, 180, 42, "Play Rec Stop AB")
    self.abLabel = comps.Label(self.surface, 264, 2, 74, "A")
  def draw(self):
    self.surface.fill((0,0,0)) # Clear surface
    self.title.draw()
    self.updateRunTime(self.model.runTime)
    self.runTimeLabel.draw()
    self.paramLabel.draw()
    self.abLabel.draw()
    self.screen.blit(self.surface, (0,0))
  def updateRunTime(self, text):
    self.runTimeLabel.changeText(text)
    self.runTimeLabel.changeColor(self.model.runTimeColor)
  def updateAB(self):
    self.abLabel.changeText(self.model.ab)
  def update(self):
    pass
