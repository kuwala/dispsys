import pygame

# My shapes enumerator
# doodat container thinggy
class SHAPE:
  SOLID = 0
  OUTLINE = 1


class Label:
  def __init__(self, _screen, _x=0,_y=0,_size=16,_txt="test",_color=(255,255,255)):
    self.screen = _screen
    self.pos = [_x,_y]
    self.size = _size
    self.color = _color
    self.txt = _txt
    self.updateText(self.txt);
    
  def updateText(self, txt):
    font = pygame.font.SysFont("Calibri", self.size, True, False)
    self.textSurf = font.render(txt, True, self.color)

  def draw(self):
    self.screen.blit(self.textSurf, self.pos);

class Button:
  shape = SHAPE.SOLID
  def __init__(self, _screen, _pos=[0,0], _size=16, color=(255,255,255)):
    self.screen = _screen
    self.pos = _pos
    
