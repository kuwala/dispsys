from pygameview import PygameView
import pygame
import events

from oscServ import oscServerGuy
from models import synthState

def debug(txt):
  print(txt)

print("Pygame RpiSynth Display")
print("Made by: Daniel")

savedOSC = synthState()

# Make a OSC Server to recieve data
# from Pure Data Synth
# Data is used to controll Scene changes
# In the view

try:
  oscGuy = oscServerGuy(savedOSC)
  debug("osc server started")
except:
  print("something wrong with pygame osc server")

evManager = events.EventManager()

debug("Starting osc Controller")
oscController = events.OSCController(evManager, savedOSC)
debug("Starting keyboard Controller")
keyboardController = events.KeyboardController(evManager)
debug("Starting cpu spinner")
cpuSpinner = events.CPUSpinner(evManager)

try:
  debug("creating pygame view")
  view = PygameView(evManager)
except:
  debug("pygame view create failed")

# run the visuals as fast as possible
# but catch KeyboardInterrupt as to not
# leave the OSC thread hanging when force closed

try :
  cpuSpinner.run()
except KeyboardInterrupt:
  evManager.post(events.QuitEvent())

try:
  oscGuy.close()
except:
  debug("failed to close oscGuy")
print("Pygame RpiSynth Shutdown")
