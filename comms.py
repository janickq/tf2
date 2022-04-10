from networktables import NetworkTables
from threading import Thread
import threading

cond = threading.Condition()
notified = [False]
sd = NetworkTables.getTable("SmartDashboard")

class comms:
    

    
    def connectionListener(connected, info):
        print(info, '; Connected=%s' % connected)
        with cond:
            notified[0] = True
            cond.notify()
        print("Connected!")


    NetworkTables.initialize(server='10.66.69.2')
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
    
    
    def read_command():
        return sd.getAutoUpdateValue("Current Command")
        
    def read_pos():
        return
    def writeStr(str1, str2):
        sd.putString(str1, str2)
        
    def writeStrArray(str1, str2):
        sd.putStringArray(str1, str2)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
       
       
        
  