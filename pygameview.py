import pygame
import os, random, string
import events

BLACK = (0,0,0)
RED = (255,0,0)
REDPINK = (255,127,127)
WHITE = (255,255,255)

""" # This is premature optimization
# Unique component idNames
# MODULE_COMPONENT_NAME = moduleNumberDigi + ComponentDigit
REC = 1000
LOOP = 2000
SYNTH = 3000
DRUM = 4000
SEQ = 5000

REC_TITLE_LABEL = 1001
REC_PLAY_BUTTON = 1002
REC_RECORD_BUTTON = 1003
REC_STOP_BUTTON = 1004
REC_SWITCH_BUTTON = 1005
REC_RUNTIME_LABEL = 1006
"""

class Label(pygame.sprite.Sprite):
  # Just a simple text label. you
  # can changeText or changeColor
  def __init__(self, text="label",group=None, size=30, color=(255,255,255) ):
    pygame.sprite.Sprite.__init__(self, group)
    self.text = text
    self.idName = "NotYet"
    self.color = color
    self.fontSize = size
    self.image = None
    self.font = pygame.font.Font(None, self.fontSize)
    self.updateImage()
    self.rect = self.image.get_rect()

  def setID(self, idName):
    self.idName = idName

  def updateImage(self):
    self.image = self.font.render(self.text, 1, self.color)
    
  def update(self):
    pass
  
  def changeText(self, text):
    self.text = str(text)
    self.updateImage()

  def changeColor(self, color):
    self.color = color
    self.updateImage()

class Button(pygame.sprite.Sprite):
  # [ Play ]
  STATE_DIM = 0
  STATE_LIGHT = 1
  STATE_PAUSED = 2
  MAX_DIM_TIME = 10
  
  def __init__(self, text="button", group=None):
    pygame.sprite.Sprite.__init__(self, group)
    self.text = text
    self.color = WHITE
    self.image = None
    self.updateImage()
    self.rect = self.image.get_rect()
    self.dimTimer = 0
    self.state = Button.STATE_LIGHT

  def pressed(self):
    self.state = Button.STATE_LIGHT
    self.dimTimer = 0

  def updateImage(self):
    # redraw self.image, used with when text
    # or color is changed
    font = pygame.font.Font(None, 30)
    self.image = font.render(self.text, 1, self.color)

  def changeText(self, text):
    self.text = text
    self.updateImage()

  def update(self):
    # The button dims itself on each update
    # once it reaches MAX_DIM_TIME it will no
    # longer updateImage()

    if self.state == Button.STATE_LIGHT:
      self.color = WHITE
      self.updateImage()
      self.state = Button.STATE_DIM

    elif self.state == Button.STATE_DIM:
      # if dimTimer is not maxed out continue Dimming
      if self.dimTimer < Button.MAX_DIM_TIME:
        ratePerFrame = 25
        c = 255 - self.dimTimer * ratePerFrame
        self.color = ( c, c, c)
        self.updateImage()
      else :
        self.state = Button.STATE_DIM
      self.dimTimer += 1
    else :
      # Its not light or dim so its paused
      pass 

class ButtonCounterSprite(Button):
  def __init__(self, text="0", group=None):
    Button.__init__(self, text, group)
    self.counter = 0
  def update(self):
    # button text increments with every frame.
    self.counter += 1
    Button.changeText(self, str(self.counter))
    Button.update(self)

class Sprite(pygame.sprite.Sprite):
  def __init__(self, group="none", fileName = "titleScreen320x240.png"):
    pygame.sprite.Sprite.__init__(self, group)
    folder = 'assets'
    file = fileName
    self.image = pygame.image.load(os.path.join(folder, file)).convert()
    self.rect = self.image.get_rect()
  def update(self):
    pass
  



class Scene(object):
  def __init__(self, screen, backgroundColor = (0,0,0) ):
    self.screen = screen
    self.background = pygame.Surface( screen.get_size() )
    self.background.fill((0,0,40))
    self.spriteGroup = pygame.sprite.RenderUpdates()
    self.setupComponents()
  def setupComponents(self):
    # create all the components here
    # and add them to the spriteGroup 
    button = Button("DefaultScene", self.spriteGroup)
    button.name = "DefaultButton"
    button.rect.topleft = ( 50, 50)
  def clearScreen(self):
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()
  def clearUpdateDraw(self):
    # clear, update, draw
    # all sprites in spriteGroup
    self.spriteGroup.clear(self.screen, self.background)
    self.spriteGroup.update()
    dirtyRects = self.spriteGroup.draw(self.screen)
    pygame.display.update(dirtyRects)
  def getCompByName(self, name):
    for component in self.spriteGroup:
      if component.name == name:
        return component

  def notify(self, event):
    if isinstance(event, events.TickEvent):
      self.clearUpdateDraw()

class IntroScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
  def setupComponents(self):
    sprite = Sprite(self.spriteGroup)
    sprite.rect.topleft = (0,0)

class ProgressBar(pygame.sprite.Sprite):
  def __init__(self, spriteGroup = None, width = 64):
    pygame.sprite.Sprite.__init__(self, spriteGroup)
    self.value = .5
    self.bgColor = (64,64,64)
    self.color = (255,255,255)
    self.width = width
    self.height = 2
    self.image = pygame.Surface((self.width, self.height))
    self.rect = self.image.get_rect()
    self.dirty = 1

  def setValue(self, value):
    self.value = value
    self.dirty = 1

  def update(self):
    if self.dirty == 1:
      self.updateImage()
      self.dirty = 0

  def updateImage(self):
    self.image.fill(self.bgColor)
    rect = (0,0, self.width * self.value, self.height)
    pygame.draw.rect(self.image, self.color, rect)
    """ # Beautification saved for later
    centerY = 6
    rect = (0,centerY, self.width, self.height)
    pygame.draw.rect(self.image, self.bgColor, rect)
    rect = (0,centerY, self.width * self.value, self.height)

    pygame.draw.rect(self.image, self.color, rect)
    x = self.width * self.value
    y = 4
    pos = ( int(x), int(y) )
    pygame.draw.circle(self.image, self.color, pos, 4)
    """
    

class DrumScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
  def setupComponents(self):
    label = Label("Drums", self.spriteGroup, 72, (255,127,255))
    label.name = "title_label"
    label.rect.topleft = (74,2)

class LooperModel():
  def __init__(self):
    self.state = "idle"
    self.barLength = 1
  def setState(self, state):
    self.state = state
  def getStateText(self):
    if self.state == "p":
      text = "Play"
    elif self.state == "r":
      text = "Record"
    elif self.state == "s":
      text = "Stop"
    return text

class LoopScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
    self.looperModel = LooperModel()

  def setupComponents(self):
    # speed
    label = Label("Looper", self.spriteGroup, 72, (255,127,127))
    label.name = "title_label"
    label.rect.topleft = (64,2)
    
    # progress bar
    progressBar = ProgressBar(self.spriteGroup, 192)
    progressBar.name = "loop_progress_bar"
    progressBar.rect.topleft = ( 62, 212 )

    # Play/Stop/Rec Button
    label = Label("Play", self.spriteGroup)
    label.name = "play_label"
    label.rect.topleft = (64,64)

  def routeRuntimeEvent(self, event):
    component = None
    component = self.getCompByName("loop_progress_bar")
    component.setValue(event.runtime)

  def routeLooperStateEvent(self, event):
    if not self.looperModel.state == event.state:
      self.looperModel.state = event.state
      component = None
      component = self.getCompByName("play_label")
      component.changeText(self.looperModel.getStateText())
      if event.state == "r":
        component.changeColor(REDPINK)
      else:
        component.changeColor(WHITE)

  def notify(self, event):
    if isinstance(event, events.TickEvent):
      self.clearUpdateDraw()
    elif isinstance(event, events.RuntimeEvent):
      self.routeRuntimeEvent(event)
    elif isinstance(event, events.LooperStateEvent):
      self.routeLooperStateEvent(event)

class SequencerScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
  def setupComponents(self):
    #title
    label = Label("Sequencer", self.spriteGroup, 72, (255,127,127))
    label.name = "title_label"
    label.rect.topleft = (32,2)
    #play / stop/ rec button
    button = Label("Play", self.spriteGroup)
    button.name = "play_button"
    button.rect.topleft = ( 32,64)
    #big sequence numbers
    label = Label("12", self.spriteGroup, 300, (255,255,255))
    label.name = "sequence_label"
    label.rect.topleft = ( 64,44)
    #note speed
    label = Label("Beats", self.spriteGroup, 18, (255,127,127))
    label.name = "bpm_label"
    label.rect.topleft = ( 32,180)
    button = Button("120", self.spriteGroup)
    button.name = "bpm_value_button"
    button.rect.topleft = (32,196)
  def routeSequenceStateEvent(self, event):
    # play stop rec
    component = self.getCompByName("play_button")
    if not component == None:
      state = event.state
      text = None
      if state == "p":
        text = "Play"
      elif state == "r":
        text = "Record"
      elif state == "i":
        text = "Stop"
      if not text == None:
        component.changeText(text)

  def routeSequenceStepEvent(self, event):
    component = self.getCompByName("sequence_label")
    if not component == None:
      step = event.step
      component.changeText(step)

  def notify(self, event):
    if isinstance(event, events.TickEvent):
      self.clearUpdateDraw()
    elif isinstance(event, events.SequenceStateEvent):
      self.routeSequenceStateEvent(event)
    elif isinstance(event, events.SequenceStepEvent):
      self.routeSequenceStepEvent(event)

class SynthBlocks(pygame.sprite.Sprite):
  def __init__(self, spriteGroup = None):
    pygame.sprite.Sprite.__init__(self, spriteGroup)
    self.noteColors = []
    for note in range(0,12):
      self.noteColors.append( self.randColor() )
  def randColor(self):
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

class SynthScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
  def setupComponents(self):
    label = Label("Synth", self.spriteGroup, 72, (127,127,255))
    label.name = "title_label"
    label.rect.topleft = (74, 2)

    # Synth Blocks Visulization

    button = Button("^",self.spriteGroup)
    button.name="select_knob_0"
    button.rect.topleft = ( 36, 220)
    button = Button("^",self.spriteGroup)
    button.name="select_knob_1"
    button.rect.topleft = ( 112, 220)
    button = Button("^",self.spriteGroup)
    button.name="select_knob_2"
    button.rect.topleft = ( 190, 220)
    button = Button("^",self.spriteGroup)
    button.name="select_knob_3"
    button.rect.topleft = ( 260, 220)

    # Attack
    modlabel = Label("Attack", self.spriteGroup, 16, (64,64,255))
    modlabel.name = "attack_label"
    modlabel.rect.topleft = ( 12, 196 )

    progressBar = ProgressBar(self.spriteGroup)
    progressBar.name = "attack_bar"
    progressBar.rect.topleft = ( 12, 212 )
    # Decay
    modlabel = Label("Decay", self.spriteGroup, 16, (64,64,255))
    modlabel.name = "decay_label"
    modlabel.rect.topleft = ( 86, 196 )

    progressBar = ProgressBar(self.spriteGroup)
    progressBar.name = "decay_bar"
    progressBar.rect.topleft = ( 86, 212 )
    # Volume
    modlabel = Label("Amplitude", self.spriteGroup, 16, (255,64,64))
    modlabel.name = "volume_label"
    modlabel.rect.topleft = ( 164, 196 )

    progressBar = ProgressBar(self.spriteGroup)
    progressBar.name = "volume_bar"
    progressBar.rect.topleft = ( 164, 212 )
    # Modulation Param
    modLabel = Label("Modulation", self.spriteGroup, 16, (127,127,127))
    modLabel.name = "modulation_label"
    modLabel.rect.topleft = ( 236, 196 )

    progressBar = ProgressBar(self.spriteGroup)
    progressBar.name = "modulation_bar"
    progressBar.rect.topleft = ( 236, 212 )

  def routeButtonEvent(self, event):
    component = None
    if event.button == 1:
      component = self.getCompByName("modulation_bar")
      if component:
        rand = random.random()
        component.setValue(rand)

  def routeParamEvent(self, event):
    name = event.name
    component = self.getCompByName(name)
    if component:
      component.setValue(event.value)

  def routeSelectKnob(self, event):
    name = "select_knob_" + str(event.knob)
    component = self.getCompByName(name)
    if component:
      component.pressed()

  def notify(self, event):
    if isinstance(event, events.TickEvent):
      self.clearUpdateDraw()
    elif isinstance(event, events.ButtonPressedEvent):
      self.routeButtonEvent(event)
    elif isinstance(event, events.ParamChangedEvent):
      self.routeParamEvent(event)
    elif isinstance(event, events.SelectKnobEvent):
      self.routeSelectKnob(event)

class RecScene(Scene):
  def __init__(self, screen):
    Scene.__init__(self, screen)
  def setupComponents(self):
    # Title
    label = Label("Recorder", self.spriteGroup, 72, (127,255,127))
    label.name = "title_label"
    label.rect.topleft = (48,2)
    # RunTime
    label = Label("00:00.0", self.spriteGroup, 72)
    label.name = "runtime"
    label.rect.topleft = (64,100)
    # Play Rec Stop Switch
    button = Button("Play", self.spriteGroup)
    button.name = "play"
    button.rect.topleft = (16, 200)
    button = Button("Record", self.spriteGroup)
    button.name = "record"
    button.rect.topleft = (72, 200)
    button = Button("Stop", self.spriteGroup)
    button.name = "stop"
    button.rect.topleft = (164, 200)
    button = Button("Switch", self.spriteGroup)
    button.name = "switch"
    button.rect.topleft = (232, 200)

  def routeButtonEvent(self, event):
    buttonSprite = None
    if event.button == 1:
      buttonSprite = self.getCompByName("play")
    elif event.button == 2:
      buttonSprite = self.getCompByName("record")
    elif event.button == 3:
      buttonSprite = self.getCompByName("stop")
    elif event.button == 4:
      buttonSprite = self.getCompByName("switch")
    if buttonSprite:
      buttonSprite.pressed()

  def routeRuntimeEvent(self, event):
    labelSprite = None
    if not event.runtime == None:
      labelSprite = self.getCompByName("runtime")
    if labelSprite:
      timeText = self.calculateRuntime(event.runtime)
      labelSprite.changeText(timeText)

  def calculateRuntime(self, millis):
    # time is recieved in millisecs
    tenths = millis / 100
    tenths = tenths % 10
    secs = millis / 1000
    secs = secs % 60
    mins = millis / 60000
    text = str(mins).zfill(2) + ":" + str(secs).zfill(2) + "." + str(tenths)
    return text

  def notify(self, event):
    if isinstance(event, events.TickEvent):
      self.clearUpdateDraw()
    elif isinstance(event, events.ButtonPressedEvent):
      self.routeButtonEvent(event)
    elif isinstance(event, events.RuntimeEvent):
      self.routeRuntimeEvent(event)

class PygameView:
  def __init__(self, evManager):
    self.evManager = evManager
    self.evManager.addListener(self)

    # point the os video frame buffer to fb1
    # the LCD on the rpi is connect to this
    os.environ["SDL_FBDEV"]= "/dev/fb1"
    pygame.init()
    # turn off audio so that pd (puredata) can grab audio focus
    pygame.mixer.quit()
    # hide mouse coursor
    pygame.mouse.set_visible(False)

    # setup screen surface
    self.screen = pygame.display.set_mode( (320, 240) )
    pygame.display.set_caption("Rpi Synth")
    self.background = pygame.Surface( self.screen.get_size() )
    self.background.fill( BLACK )

    # Setup SceneViews
    self.introScene = IntroScene(self.screen)
    self.synthScene = SynthScene(self.screen)
    self.drumScene = DrumScene(self.screen)
    self.sequencerScene = SequencerScene(self.screen)
    self.loopScene = LoopScene(self.screen)
    self.recScene = RecScene(self.screen)

    # current scene view
    # set intro scene as the first view
    self.activeScene = self.introScene

    # make groups for sprites

  def interpertButton(self, event):
    """ Change scenes when scene change buttons are pressed
    if the button is a context sensative button then pass it
    to the active scene. also clearScreen on a scene change.
    """
    nextScene = None
    if event.button == "q":
      nextScene = self.sequencerScene
    elif event.button == "i":
      nextScene = self.introScene
    elif event.button == "d":
      nextScene = self.drumScene
    elif event.button == "r":
      nextScene = self.recScene
    elif event.button == "t":
      nextScene = self.loopScene
    elif event.button == "s":
      nextScene = self.synthScene
    elif event.button == "w":
      nextScene = self.synthScene
    else:
      # other event pass to scene
      self.activeScene.notify(event)

    if not nextScene == None:
      if not nextScene == self.activeScene:
        self.activeScene = nextScene
        self.activeScene.clearScreen()

  def notify(self, event):
    if isinstance( event, events.TickEvent):
      self.activeScene.notify(event)
    elif isinstance( event, events.ButtonPressedEvent):
      # self.updateButton(event)
      self.interpertButton(event)
    else :
      # its some other event lets
      # let the active sceen know
      self.activeScene.notify(event)

    
