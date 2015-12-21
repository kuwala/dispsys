
class synthState(object):
  args = None
  def __init__(self):
    self.txt = "/start"
    # fresh = cold || hot
    self.fresh ="cold"
    self.path = "/start"
  def receive(self, _path, _tags, _args):
    self.txt  = _path
    self.path = _path
    self.args = _args
  def setHot(self):
    self.fresh = "hot"
  def setCold(self):
    self.fresh = "cold"

