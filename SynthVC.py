
class SynthViewController:
  def __init__(self, synthModel, synthView):
    self.synthModel = synthModel
    self.synthView = synthView
  def CPUTick(self):
    self.synthModel.CPUTick() #current does nothing :'(
    self.synthView.draw()
    self.synthModel.updateDrawState() # kind of like cpu tick :'(
  # def recieveOSC(self, path, tags, args):
  def receiveOSC(self, savedOSC):
    # if note is played
    path = savedOSC.path
    args = savedOSC.args
    if (path =="/s"):
      note = args[0]
      if note != -1: # make sure its a note and not init signal
        self.synthModel.addNote(note)
      else :
        self.synthModel.makeActive()
    # Parameters changes / knobs
    elif (path == "/s/k1"):
      # in futuure chanve osc to /synth/attack - /synth/modfreq
      self.synthModel.changeParam("Attack", args[0])
      self.synthView.updateParamLabel()
      self.synthModel.makeActive()
      #self.synthView.redrawParamLabel()
    elif (path == "/s/k2"):
      self.synthModel.changeParam("Decay", args[0])
      self.synthView.updateParamLabel()
      self.synthModel.makeActive()
    elif (path == "/s/k3"):
      self.synthModel.changeParam("Volume", args[0])
      self.synthView.updateParamLabel()
      self.synthModel.makeActive()
    elif (path == "/s/k4"):
      self.synthModel.changeParam("ModFreq", args[0])
      self.synthView.updateParamLabel()
      self.synthModel.makeActive()
    # update model
    # update view 
  
