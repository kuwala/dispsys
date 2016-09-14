from pygameview import PygameView
import pygame
import events
import sys

from oscServ import oscServerGuy
from models import synthState

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
  debug("something wrong with pygame osc server")
  debugException()

evManager = events.EventManager()

debug("Starting osc Controller")
oscController = events.OSCController(evManager, savedOSC)
debug("Starting keyboard Controller")
keyboardController = events.KeyboardController(evManager)
debug("Starting cpu spinner")
cpuSpinner = events.CPUSpinner(evManager)

debug("creating pygame view")
view = PygameView(evManager)

# run the visuals as fast as possible
# but catch KeyboardInterrupt as to not
# leave the OSC thread hanging when force closed

try :
  # start the while loop that runs untill close
  # and does eventManager.Post(CPUTickEvent())
  cpuSpinner.run()
except KeyboardInterrupt:
  evManager.post(events.QuitEvent())

try:
  oscGuy.close()
except:
  debug("failed to close oscGuy")
  debugException()
print("Pygame RpiSynth Shutdown")
