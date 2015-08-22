from OSC import OSCServer
import threading

# Server IP and Port Tuple
# # # # # # # # # # # # # # 
class oscServerGuy(object):
  def __init__(self, state):
    self.state = state
    # takes a synthState obj
    # on callback passes it data
    serverIP = ("127.0.0.1", 57121)
    print( "osc Server sarted on IP & Port: ", serverIP) 
    self.oscServer = OSCServer( serverIP )
    self.oscServer.addMsgHandler("/text", self.callBack)
    self.oscServer.addMsgHandler("/s" , self.callBack)
    self.oscServer.addMsgHandler("/d" , self.callBack)
    self.oscServer.addMsgHandler("/q" , self.callBack)
    self.oscServerThread = threading.Thread( target = self.oscServer.serve_forever )
    self.oscServerThread.start()
  def callBack(self, path, tags, args, source):
    self.state.receive(path, tags, args)
    self.state.setHot()
    print(args);
  def close(self):
    self.oscServer.close()
    self.oscServerThread.join()
