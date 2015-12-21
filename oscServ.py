from OSC import OSCServer
import threading

# Server IP and Port Tuple
# # # # # # # # # # # # # # 
class oscServerGuy(object):
  def __init__(self, savedOSC):
    self.savedOSC = savedOSC
    # takes a synthState obj
    # on callback passes it data
    serverIP = ("127.0.0.1", 57121)
    print( "osc Server sarted on IP & Port: ", serverIP) 
    self.oscServer = OSCServer( serverIP )
    self.oscServer.addMsgHandler("/text", self.callBack)
    self.oscServer.addMsgHandler("/s" , self.callBack)
    self.oscServer.addMsgHandler("/s/k1" , self.callBack)
    self.oscServer.addMsgHandler("/s/k2" , self.callBack)
    self.oscServer.addMsgHandler("/s/k3" , self.callBack)
    self.oscServer.addMsgHandler("/s/k4" , self.callBack)
    self.oscServer.addMsgHandler("/d" , self.callBack)
    self.oscServer.addMsgHandler("/q" , self.callBack)
    self.oscServer.addMsgHandler("/r" , self.callBack)
    self.oscServerThread = threading.Thread( target = self.oscServer.serve_forever )
    self.oscServerThread.start()
  def callBack(self, path, tags, args, source):
    self.savedOSC.receive(path, tags, args)
    self.savedOSC.setHot()
    print(args);
  def close(self):
    self.oscServer.close()
    self.oscServerThread.join()
