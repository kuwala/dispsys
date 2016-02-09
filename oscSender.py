from OSC import OSCClient, OSCMessage
import events

def debug(txt):
  print(txt)
  pass

class OscSender():
  def __init__(self):
    # setup osc client
    # connect to server
    debug("Connecting to pd note server")
    self.client = OSCClient()
    server_ip = ("127.0.0.1", 57123)
    # Library provides no way of
    # Verifying if the connection worked :(
    self.client.connect( server_ip )
  def routeNote(self, event):
    address = "/playNote"
    note = int(event.note)
    self.sendNote(address, note)
  def notify(self, event):
    # listen to messages from evManger
    if isinstance(event, events.NoteOutEvent):
      self.routeNote(event)
  def sendNote(self, address, note):
    # clreat osc msg
    # send to puredata synth
    # msg = OSCMessage("/playNote", 64)
    try:
      self.client.send(OSCMessage(address, note))
    except Exception as ex:
      debug(ex)
      print("note sending error %d note " % note)
