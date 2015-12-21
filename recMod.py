import dispComponents as comps
import random
class RecModule:
  def __init__(self, screen):
    self.screen = screen
    # s - stop, p - play, r = record
    self.state = 's'
    # Record Title
    text = "LOOPER"
    self.titleLabel = comps.Label(self.screen, 48,2,72,text)
    # Play / Rec Button
    px = 32 + 16
    py = 96
    ps = 16

    self.playButton = comps.Button(self.screen, [px, py], ps)
    self.playButton.changeFill(comps.SHAPE.OUTLINE)
    self.playButton.changeShape(comps.SHAPE.TRIANGLE)
    self.playButton.changeColor(comps.COLOR.WHITE)
    
    # Progress Bar
    pbx = 32
    pby = 192
    pbw = 256
    pbh = 8
    self.progressBar = comps.ProgressBar(self.screen, pbx, pby, pbw, pbh)
    # BPM Label
    bpmx = 228
    bpmy = 96
    bpms = 38
    bpmText = "100"
    self.bpmLabel = comps.Label(self.screen, bpmx, bpmy, bpms, bpmText)
    # BPM Animation
    # self.bpmSprite = comps.Sprite(self.screen, 266, 60, 'train14x10.png')
  def update(self, args):
    if(len(args) > 1):
      self.state = args[0]
      self.percentAt = args[1]
    else :
      self.state = 's'
      self.percentAt = .5
    if (self.state == 's'):
      self.playButton.changeColor(comps.COLOR.WHITE)
      self.progressBar.changeColor(comps.COLOR.BLUE)
      #self.playButton.changeShape(comps.SHAPE.SQUARE)
    elif (self.state == 'r'):
      self.playButton.changeColor(comps.COLOR.RED)
      self.progressBar.changeColor(comps.COLOR.RED)
      #self.playButton.changeShape(comps.SHAPE.CIRCLE)
    elif (self.state == 'p'):
      self.playButton.changeColor(comps.COLOR.BLUE)
      self.progressBar.changeColor(comps.COLOR.BLUE)
      #self.playButton.changeShape(comps.SHAPE.TRIANGLE)

    # update percentAt
    self.progressBar.changePercent(self.percentAt)

  def randomPercent(self):
    per = random.random()
    self.progressBar.changePercent(per)
  def draw(self):
    self.screen.fill((0,0,0))
    self.titleLabel.draw()
    self.playButton.draw()
    self.bpmLabel.draw()
    self.progressBar.draw()
    # self.bpmSprite.draw()

'''
 # # # # #   PASTED REFERENCE   # # # # # # 

    # display buttons
    rx = 32
    ry = 96
    rs = 16
    # Color here ??
    self.recButton = Button(self.screen, [rx, ry], rs)
    self.recButton.changeFill(SHAPE.SOLID)
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
'''
