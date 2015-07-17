
class synthState(object):
  def __init__(self):
    self.txt = "/start"
  def receive(self, path):
    self.txt = path

