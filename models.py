
class synthState(object):
  def __init__(self):
    self.txt = "/start"
    # fresh = cold || hot
    self.fresh ="cold"
  def receive(self, path):
    self.txt = path
  def setHot(self):
    self.fresh = "hot"
  def setCold(self):
    self.fresh = "cold"

