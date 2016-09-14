from OSC import OSCServer
import threading, string
import pygame

debug_on = False
def debug(txt):
  if debug_on:
    print(txt)

def debugException():
  if debug_on:
    print("***Exception error start***")
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
    print("***Exception error end***")

class OSCController:
  """ Checks the SavedOSC for a hot msg
  then creates an event based on the osc
  msg and posts the event
  """
  def __init__(self, evManager, savedOSC):
    self.evManager = evManager
    self.evManager.addListener(self)
    self.savedOSC = savedOSC
  def notify(self, event):
    if isinstance(event, TickEvent):
      path = self.savedOSC.path
      args = self.savedOSC.args
      fresh = self.savedOSC.fresh
      if fresh == "hot":
        # check for which is the main OSC target container
        # this is a good way to do it if you have lots of osc msgs
        # path = string.split( self.savedOSC.path, "/")[1]
        # if path == "test":
        debug("oscController recieved %s" % path)

        # see if osc matchs anything we want to recieve
        # and if so make an event(s) than at then end post it
        # to the evManager
        event = None
        # if an OSC makes more then one event then they are stored in events
        events = []

        if path == "/test":
          # test - testing OSC recieved
          # if it has more then 2 arguments
          # find out whichbutton was pressed
          # /test p 0-3   <-- buton 0-3 was pressed
          # /test r 0-3   <-- buton 0-3 was released
          if len(args) > 1:
            # asume it was pressed
            button = args[1]
            event = ButtonPressedEvent(button)

        # - - - - - - - - Recorder - - - - - - - -
        elif path == "/r":
          event = ButtonPressedEvent("r")
        elif path == "/r/runtime":
          # /r/runtime p 110
          # address p = play r = record 
          # /r/runtime state time_in_10ths_secs
          if len (args) > 0:
            runtime = args[1] 
            event = RuntimeEvent(runtime)
        elif path == "/r/play":
          event = ButtonPressedEvent(1)
        elif path == "/r/record":
          event = ButtonPressedEvent(2)
        elif path == "/r/stop":
          event = ButtonPressedEvent(3)
          # event2 = RuntimeEvent(0)
          # self.evManager.post(event2)
        elif path == "/r/switch":
          event = ButtonPressedEvent(4)

        # - - - - - - - - Synth - - - - - - - -
        elif path == "/s":
          n = args[0]
          if n == -1:
            # synth init / became active
            event = ButtonPressedEvent("s")
          elif not n == None:
            # note played
            event = ButtonPressedEvent("s")
          
        elif path == "/s/attack/param":
          v = args[0]
          event = ParamChangedEvent("attack_bar", v)
        elif path == "/s/decay/param":
          v = args[0]
          event = ParamChangedEvent("decay_bar", v)
        elif path == "/s/volume/param":
          v = args[0]
          event = ParamChangedEvent("volume_bar", v)
        elif path == "/s/modfreq/param":
          v = args[0]
          event = ParamChangedEvent("modulation_bar", v)
        elif path == "/s/selectKnob":
          v = args[0]
          event = SelectKnobEvent(v)

        # - - - - - - - - Drum - - - - - - - -
        elif path == "/d":
          n = args[0]
          if n == -1:
            # drum init / became active
            event = ButtonPressedEvent("d")
          elif not n == None:
            # note played
            event = ButtonPressedEvent("d")
            
        # - - - - - - - - Sequencer - - - - - - - -
        elif path == "/q":
          state = args[0]
          if state == -1:
            event = ButtonPressedEvent("q")
          elif not state == None:
            # note played
            # /s r 12 250
            # /s i o 250
            # /s p 12 250
            # /s state step durationMs
            # event = ButtonPressedEvent("q")
            step = args[1]
            events.append(SequenceStepEvent(step))
            events.append(SequenceStateEvent(state))


        # - - - - - - - - Looper - - - - - - - -
        # /t p 0.25
        # /t s
        # /t r 0.123
        elif path == "/t":
          state = args[0]
          if state == -1:
            # make view active
            events.append(ButtonPressedEvent("t"))
            runtime = args[2]
            newState = args[1]
            events.append(RuntimeEvent(runtime))
            events.append(LooperStateEvent(newState))
            

          elif not state == None:
            runtime = args[1]
            event = RuntimeEvent(runtime)
            event2 = LooperStateEvent(state)
            events.append(event)
            events.append(event2)

        # - - - - - - - - Post Event - - - - - - - -
        # Post the events to listeners
        for event in events:
          self.evManager.post(event)
        if not event == None:
          self.evManager.post(event)

        # Mark the saved OSC as old
        self.savedOSC.fresh = "cold"

class CPUSpinner:
  def __init__(self, evManager):
    self.evManager = evManager
    self.evManager.addListener(self)
  def run(self):
    self.running = True
    while self.running:
      ev = TickEvent()
      self.evManager.post(ev)
  def notify(self, event):
    if isinstance(event, QuitEvent):
      self.running = False

class KeyboardController:
  """Gets keyboard keys via pygame and sends to evManager"""
  def __init__(self, evManager):
    self.evManager = evManager
    self.evManager.addListener(self)

  def notify(self, event):
    if isinstance(event, TickEvent):
      for event in pygame.event.get():
        ev = None
        if event.type == pygame.KEYDOWN:
          # A keyboard key has been pressed
          # find out which one
          if event.key == pygame.K_1:
            ev = ButtonPressedEvent(1)
          elif event.key == pygame.K_2:
            ev = ButtonPressedEvent(2)
          elif event.key == pygame.K_3:
            ev = ButtonPressedEvent(3)
          elif event.key == pygame.K_4:
            ev = ButtonPressedEvent(4)
          elif event.key == pygame.K_q:
            ev = ButtonPressedEvent("q")
          elif event.key == pygame.K_w:
            ev = ButtonPressedEvent("w")
          elif event.key == pygame.K_s:
            ev = ButtonPressedEvent("s")
          elif event.key == pygame.K_d:
            ev = ButtonPressedEvent("d")
          elif event.key == pygame.K_t:
            ev = ButtonPressedEvent("t")
          elif event.key == pygame.K_l:
            ev = ButtonPressedEvent("l")
          elif event.key == pygame.K_r:
            ev = ButtonPressedEvent("r")
          elif event.key == pygame.K_i:
            ev = ButtonPressedEvent("i")
          elif event.key == pygame.K_m:
            ev = ButtonPressedEvent("m")
          elif event.key == pygame.K_5:
            ev = ButtonPressedEvent(5)
          elif event.key == pygame.K_ESCAPE:
            ev = QuitEvent()
        elif event.type == pygame.QUIT:
          ev = QuitEvent()
        # - - - - Post it - - - -  - - - - -
        # If event was one of the ones we are
        # looking for post it to the evManager
        if not ev == None:
          self.evManager.post(ev)
      # End of the for loop
    
class Event:
  """This is a superclass for any events that might
  be generated by an object and sent to the EventManager
  """
  pass

class TickEvent(Event):
  def __init__(self):
    self.name = "butts"

class SelectKnobEvent(Event):
  def __init__(self, knob):
    self.knob = knob

class ButtonPressedEvent(Event):
  def __init__(self, button):
    self.button = button

class LooperStateEvent(Event):
  def __init__(self, state):
    self.state = state

class SequenceStateEvent(Event):
  def __init__(self, state):
    self.state = state
    # states: play, stop, record
class SequenceStepEvent(Event):
  def __init__(self, step):
    self.step = step

class NoteEvent(Event):
  def __init__(self, note):
    self.note = note

class NoteOutEvent(Event):
  def __init__(self, note):
    self.note = note

class ParamChangedEvent(Event):
  def __init__(self, name, value):
    self.name = name
    self.value = value

class RuntimeEvent(Event):
  def __init__(self, runtime):
    self.runtime = runtime

class TimerFiredEvent(Event):
  pass


class QuitEvent(Event):
  pass

class EventManager:
  """This object is reponsible for being the mediator between the PygameView
  and the OSCReceivedController
  """
  def __init__(self):
    from weakref import WeakKeyDictionary
    self.listeners = WeakKeyDictionary()
  def addListener(self, listener):
    self.listeners[listener] = 1

  def removeListener(self, listener):
    if listener in self.listeners.keys():
      del self.listeners[ listener ]

  def post(self, event):
    if not isinstance(event, TickEvent):
      debug("This event was posted %s" % event.__class__.__name__)
    for listener in self.listeners.keys():
      # Note: if weakref has died, it will be
      # Automatically removed, so we dont
      # have to worry about it showing up in listeners
      listener.notify(event)

