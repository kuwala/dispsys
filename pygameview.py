import pygame
import os
import events

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)


class ButtonSprite(pygame.sprite.Sprite):
  # [ Play ]
  STATE_DIM = 0
  STATE_LIGHT = 1
  STATE_PAUSED = 2
  MAX_DIM_TIME = 160

  def __init__(self, text="button", group=None):
    pygame.sprite.Sprite.__init__(self, group)
    self.text = text
    self.color = WHITE
    self.image = None
    self.updateImage()
    self.rect = self.image.get_rect()
    self.dimTimer = 0
    self.state = ButtonSprite.STATE_LIGHT

  def pressed(self):
    self.state = ButtonSprite.STATE_LIGHT
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

    if self.state == ButtonSprite.STATE_LIGHT:
      self.color = WHITE
      self.updateImage()
      self.state = ButtonSprite.STATE_DIM

    elif self.state == ButtonSprite.STATE_DIM:
      # if dimTimer is not maxed out continue Dimming
      if self.dimTimer < ButtonSprite.MAX_DIM_TIME:
        c = 255 - self.dimTimer
        self.color = ( c, c, c)
        self.updateImage()
      else :
        self.state = ButtonSprite.STATE_DIM
      self.dimTimer += 1
    else :
      # Its not light or dim so its paused
      pass 

class ButtonCounterSprite(ButtonSprite):
  def __init__(self, text="0", group=None):
    ButtonSprite.__init__(self, text, group)
    self.counter = 0
  def update(self):
    # button text increments with every frame.
    self.counter += 1
    ButtonSprite.changeText(self, str(self.counter))
    ButtonSprite.update(self)
class Scene2View:
  def __init__(self, screen):
    self.screen = screen
    self.background = pygame.Surface( screen.get_size() )
    self.background.fill((0,0,0))
    self.spriteGroup = pygame.sprite.RenderUpdates()
    self.setupComponents()

  def clearScreen(self):
    self.screen.blit( self.background, (0,0))
    pygame.display.flip()

  def updateButton(self, event):
    # make button light up based on which button was pressed
    buttonSprite = None
    if event.button == 1:
      buttonSprite = self.getButtonByText("Play")

    elif event.button == 2:
      buttonSprite = self.getButtonByText("Record")

    elif event.button == 3:
      buttonSprite = self.getButtonByText("Stop")

    elif event.button == 4:
      buttonSprite = self.getButtonByText("Switch")

    # check if we got a button
    if not buttonSprite == None:
      buttonSprite.pressed()
 
  def getButtonByText(self, text):
    for buttonSprite in self.spriteGroup:
      if buttonSprite.text == text:
        return buttonSprite

  def setupComponents(self):
    button = ButtonSprite("Play", self.spriteGroup)
    button.rect.topleft = (10,50)
    button = ButtonSprite("Record", self.spriteGroup)
    button.rect.topleft = (110,50)
    button = ButtonSprite("Stop", self.spriteGroup)
    button.rect.topleft = (210,50)
    button = ButtonSprite("Switch", self.spriteGroup)
    button.rect.topleft = (290,50)

  def notify(self, event):
    # passes events to components
    if isinstance(event, events.TickEvent):
      #clear update draw sprites
      self.spriteGroup.clear(self.screen, self.background)
      self.spriteGroup.update()
      dirtyRects = self.spriteGroup.draw( self.screen )

      pygame.display.update( dirtyRects)
    elif isinstance(event, events.ButtonPressedEvent):
      self.updateButton(event)

class SceneView:
  def __init__(self, screen):
    self.screen = screen
    self.background = pygame.Surface( screen.get_size() )
    self.background.fill((0,0,200))
    self.spriteGroup = pygame.sprite.RenderUpdates()
    self.setupComponents()

  def clearScreen(self):
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()

  def updateButton(self, event):
    buttonSprite = None
    if event.button == 1:
      buttonSprite = self.getButtonByText("Go")
    if not buttonSprite == None:
      buttonSprite.pressed()
      buttonSprite.rect.move_ip(2,0)
        
  def getButtonByText(self, text):
    for buttonSprite in self.spriteGroup:
      if buttonSprite.text == text:
        return buttonSprite

  def setupComponents(self):
    button = ButtonSprite("Go", self.spriteGroup)
    button.rect.topleft = ( 100, 100)
    counterButton = ButtonCounterSprite("1000", self.spriteGroup)
    counterButton.rect.topleft=(100,200)

  def notify(self, event):
    # passes events to components
    if isinstance(event, events.TickEvent):
      #clear update draw sprites
      self.spriteGroup.clear(self.screen, self.background)
      self.spriteGroup.update()
      dirtyRects = self.spriteGroup.draw( self.screen )

      pygame.display.update( dirtyRects)
    elif isinstance(event, events.ButtonPressedEvent):
      self.updateButton(event)
      

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

    # Draw a welcome screen
    font = pygame.font.Font(None, 30)
    text = """Welcome (. _ .)"""
    textImg = font.render( text, 1, RED )
    self.background.blit(textImg, (0,0))
    self.screen.blit( self.background, (0,0) )
    pygame.display.flip()

    # Setup SceneViews
    self.test2View = Scene2View(self.screen)
    self.testView = SceneView(self.screen)

    # current scene view
    self.activeScene = self.test2View

    # make groups for sprites

  def interpertButton(self, event):
    """ Change scenes when scene change buttons are pressed
    if the button is a context sensative button then pass it
    to the active scene. also clearScreen on a scene change.
    """
    nextScene = None
    if event.button == "q":
      nextScene = self.test2View
    elif event.button == "w":
      nextScene = self.testView
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


    
