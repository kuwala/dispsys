import pygame
import pygame.gfxdraw
import math
import os

# My shapes enumerator
# doodat container thinggy
class SHAPE:
  SOLID = 0
  OUTLINE = 1
  CIRCLE = 2
  TRIANGLE = 3
  SQUARE = 4
class COLOR:
  WHITE = (255,255,255)
  BLUE = (0,108,255)
  RED = (255,24,108)

FONT = "Calibri"
class Label:
  def __init__(self, _screen, _x=0,_y=0,_size=16,_txt="test",_color=(255,255,255)):
    self.screen = _screen
    self.pos = [_x,_y]
    self.size = _size
    self.color = _color
    self.txt = str(_txt)
    self.changeText(self.txt);
    
  def updateText(self):
    font = pygame.font.SysFont(FONT, self.size, True, False)
    self.textSurf = font.render(str(self.txt), True, self.color)

  def changeText(self, _txt):
    self.txt = _txt
    self.updateText()
  def changeColor(self, _color):
    self.color = _color
    self.updateText()
  def draw(self):
    self.screen.blit(self.textSurf, self.pos);

class Button:
  shape = SHAPE.CIRCLE
  fill = SHAPE.OUTLINE
  def __init__(self, _screen, _pos=[0,0], _size=32, _color=(255,0,0)):
    self.screen = _screen
    self.pos   = _pos
    self.size  = _size
    self.color = _color

  # No Error Checking on these eeeek !
  def changeShape(self, _shape):
    self.shape = _shape
  def changeFill(self, _fill):
    self.fill = _fill
  def changePos(self, _pos):
    self.pos = _pos
  def changeColor(self, _color):
    self.color = _color

  def draw(self):
    if ( self.shape == SHAPE.CIRCLE ) :
      if ( self.fill == SHAPE.SOLID ) :
        pygame.draw.circle(self.screen, self.color, self.pos, self.size, 0)
      else :
        x = self.pos[0]
        y = self.pos[1]
        gap = self.size / 2
        #arcRect = ( (x - gap, y - gap), (x + gap, y - gap), (x + gap, y + gap), (x - gap, y + gap) ) 
        arcRect = pygame.Rect(x - gap, y - gap, self.size, self.size)
        #pygame.draw.arc(self.screen, self.color, arcRect, 0, 2*pi, 2)
        #pygame.gfxdraw.arc(self.screen, x, y, self.size, 0, 2*pi, self.color )
        pygame.gfxdraw.circle(self.screen, x, y, self.size, self.color)
    else :
      x = self.pos[0]
      y = self.pos[1]
      # my weird triangle
      # Probably replace with a sprite ??
      x = x - 16
      pad = 4
      pointList = ( (x + pad, y) , (x + 32 - pad, y + 16), (x + pad, y + 32) )
      pygame.draw.polygon(self.screen, self.color, pointList, 0)
class Sprite:
  def __init__(self, screen, x, y, fileName='shark14x9.png'):
    self.screen = screen
    self.x = x
    self.y = y
    folder = 'assets'
    file = fileName
    
    tempSurface = pygame.image.load(os.path.join(folder, file)).convert()
    w = tempSurface.get_width()
    h = tempSurface.get_height()
    scale = 3
    self.surface2 = pygame.transform.scale(tempSurface, (w * scale, h * scale))
    # Possible speed increase
    # self.surface = pygame.image.load(os.path.join(folder, file)).convert()

  def changePos(self, x, y):
    self.x = x
    self.y = y
  def draw(self):
    self.screen.blit(self.surface2, (self.x,self.y))
    
    

class ProgressBar:
  def __init__(self, screen, x, y, w = 128, h = 4):
    self.screen = screen
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.percentAt = .001
    self.color = (255,255,255)
    self.colorAt = COLOR.BLUE
  def changePercent(self, per):
    self.percentAt = per
  def changeColor(self, color):
    self.colorAt = color
  def draw(self):
    # draw bg line
    pygame.gfxdraw.box(self.screen, [self.x, self.y, self.w, self.h], self.color)
    # draw percentAt line
    widthAt = self.w * self.percentAt
    pygame.gfxdraw.box(self.screen, [self.x, self.y, widthAt, self.h], self.colorAt)
    
class funcGraph:
  def __init__(self, screen, x , y ):
    self.screen = screen
    self.x = x
    self.y = y
    self.w = 240
    self.h = 160
    self.a = 72
    self.xStep = math.pi / 64
    self.bgColor = (25,25,25)
    self.lineColor = (220,220,255)
    self.surf = pygame.Surface((self.w, self.h))
    # Optional
    self.ys = [] # array of Y values
    self.numXPoints = 6
    # Angle for grpha animation
    self.gAngle = 0
    self.gAngleRate = 0.02
    self.fillArray()

  def drawSin(self):
    lastX = self.x
    lastY = self.y + self.h/2
    # Draw the bg First
    pygame.draw.rect(self.screen, self.bgColor, (self.x, self.y, self.w, self.h))
    # Draw the line segment between two points at a time
    for i in range(self.w):
      # y = sin(x)
      pointY = math.sin(i * self.xStep) * self.a
      # Calculate graph offset
      # So that its centered veritcally
      
      newX = self.x + i
      newY = self.y+ self.h/2 + pointY
      pygame.draw.line(self.screen, self.lineColor, (lastX, lastY), (newX, newY) )
      lastX = newX
      lastY = newY
      #print pointY
    #blit surf to screen
    #self.surf.blit(self.screen, (0,0))

  def drawBG(self):
    pygame.draw.rect(self.screen, self.bgColor, (self.x, self.y, self.w, self.h))

  def drawBallSin(self):
    self.drawBG()
    offX = self.x
    offY = self.y + self.h / 2
    r= 4
    length = len(self.ys)
    xBalls = length / self.numXPoints
    rate = length / xBalls
    for i in range(xBalls):
      xPoint = i*rate + offX 
      yPoint = self.ys[i*rate] + offY
      #pygame.draw.circle(self.screen, self.lineColor, (int(xPoint), int(yPoint)), r)
      pygame.gfxdraw.filled_circle(self.screen, int(xPoint), int(yPoint), int(r), self.lineColor)
    #for i , yPoint in enumerate(self.ys):
    #  xPoint = int(i) + offX 
    #  yPoint = yPoint + offY
    #  pygame.draw.circle(self.screen, self.lineColor, (xPoint, int(yPoint)), 4)

  def drawPoints(self):
    # fill array with y values
    # draw 
    pass

  def fillArray(self):
    self.ys = [] 
    stepSize = math.pi / 96
    amp = self.a
    for s in range(self.w):
      self.ys.append(math.sin(s * stepSize + self.gAngle) * amp )
  def updateAngle(self):
    self.gAngle = self.gAngle + self.gAngleRate
  def draw(self):
    self.updateAngle()
    self.fillArray()
    self.drawBallSin()

    


class visModule:
  def __init__(self, screen):
    self.screen = screen
    text = "Vis av Vive"
    self.titleLabel = Label(self.screen,4,2,72,text)
    self.graph = funcGraph(self.screen,40,72)
  def update(self, path, args):
    pass
  def draw(self):
    self.screen.fill((0,0,0))
    self.titleLabel.draw()
    self.graph.updateAngle()
    self.graph.draw()



class SeqModule:
  def __init__(self, screen):
    self.screen = screen

    # display title
    text = "SEQUENCER"
    self.titleLabel = Label(self.screen,4,2,72,text)
    
    # display Step Text
    step = 11
    sx = 64
    sy = 32
    ss = 288 # step size
    self.stepLabel = Label(self.screen, sx, sy, ss, step) 

    # display buttons
    rx = 32
    ry = 96
    rs = 16
    # Color here ??
    self.recButton = Button(self.screen, [rx, ry], rs)
    self.recButton.changeFill(SHAPE.SOLID)

    # Play Button
    px = 32
    py = 142
    ps = 16
    self.playButton = Button(self.screen, [px, py], ps)
    self.playButton.changeShape(SHAPE.TRIANGLE)

    # display duration param
    dx = 16
    dy = 204
    ds = 32   # font size
    dur = 250 # duration text
    self.durLabel = Label(self.screen, dx, dy, ds, dur)
  def update(self, path, args):
    if (len(args) > 2) :
      state = args[0]
      step = args[1]
      dur = args[2]
    else :
      state = "i"
      step = -1
      dur = 123
    
    white = (255,255,255)
    red = (255,0,0)
    blue = (0,0,255)

    # Update Button Colors
    if (state == "i") :
      self.playButton.changeColor(white)
      self.recButton.changeColor(white)
      self.stepLabel.changeColor(white)
    elif (state == "p") :
      self.playButton.changeColor(blue)
      self.recButton.changeColor(white)
      self.stepLabel.changeColor(white)
    elif (state == "r") :
      self.playButton.changeColor(white)
      self.recButton.changeColor(red)
      self.stepLabel.changeColor(red)

    # Update values
    self.stepLabel.changeText(step)
    self.durLabel.changeText(dur)


    # root note shift param
    # octave shift
  def draw(self):
    # clear screen
    self.screen.fill((0,0,0))
    # draw each of the Components
    self.titleLabel.draw()
    self.stepLabel.draw()
    self.recButton.draw()
    self.playButton.draw()
    self.durLabel.draw()
  def input(self, note, state):
    # update 
    pass

