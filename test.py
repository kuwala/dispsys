from pygameview import PygameView
import events

from oscServ import oscServerGuy
from models import synthState

print("Pygame RpiSynth test started")

savedOSC = synthState()
oscGuy = oscServerGuy(savedOSC)

evManager = events.EventManager()

oscController = events.OSCController(evManager, savedOSC)
keyboardController = events.KeyboardController(evManager)
cpuSpinner = events.CPUSpinner(evManager)

view = PygameView(evManager)
# run the visuals as fast as possible
# but catch KeyboardInterrupt as to not
# leave a thread hanging when force closed

try :
  cpuSpinner.run()
except KeyboardInterrupt:
  evManager.post(events.QuitEvent())

oscGuy.close()
print("The test is now over")
