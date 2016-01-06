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

cpuSpinner.run()

oscGuy.close()
print("The test is now over")
