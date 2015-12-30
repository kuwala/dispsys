
class LongRecController(object):
  def __init__(self, model, view):
    self.model = model
    self.view = view

  def CPUTick(self):
    self.view.draw()
    # self.view.smartDraw()
    #self.model.updateDrawState()
  def receiveOSC(self, savedOSC):
    # /t/record 2000
    # /t/play 200
    # /t/stop
    # /t/switch

    # if playbutton pressed
    # updated playIndicator Display

    path = savedOSC.path
    if (path == "/r/play"):
      if len(savedOSC.args) > 0:
        millis = savedOSC.args[0]
        self.model.updateRunTime(millis)
      self.model.play()
      self.model.makeActive()
    elif path == "/r/stop":
      self.model.stop()
      self.model.makeActive()
    elif path == "/r/record":
      if len(savedOSC.args) > 0:
        millis = savedOSC.args[0]
        self.model.updateRunTime(millis)
      self.model.record()
      self.model.makeActive()
    elif path == "/r/switch":
      self.model.switch()
      self.view.updateAB()
      self.model.makeActive()
    elif path =="/r":
      # generic long recorder osc
      if len(savedOSC.args) > 0:
        arg = savedOSC.args[0]
        if arg == "playButton":
          self.view.updateIndicator("playButton")
          self.model.makeActive()
