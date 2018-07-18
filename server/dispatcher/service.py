import config
import logging
import socket

class Service(object):
    """
    Service class
    """
    
    OPTS = dict()
    SOCKET_TIMEOUT = 0.01
    
    def __init__(self, id, json):
        self.id = id.upper()
        self.type = json["type"]
        self.name = json["name"]
        self.cost = json["cost"]
        self.json = json
        self.dir = config.Config.PREFIX + "/var/%s_%s/" % (self.type, self.id)
        self.cfg = config.CONFIG.getService(self.id)
        for o in self.OPTS:
            if o in self.cfg:
                logging.debug("Setting service %s parameter %s to %s" % (id,o,self.cfg[o]))
            else:
                logging.debug("Setting service %s parameter %s to default (%s)" % (id,o,self.OPTS[o]))
                self.cfg[o] = "%s" % (self.OPTS[o])
        for c in self.cfg:
            if c not in self.OPTS.keys():
                logging.warning("Unknown parameter %s for service %s" % (c,id))
        self.initphase = True

    def stop(self):
        if (os.path.exists(self.mgmtfile)):
            os.remove(self.mgmtfile)
        if (os.path.exists(self.pidfile)):
            os.remove(self.pidfile)
        self.process.kill()
        logging.warning("Stopped service %s[%s]" % (self.name, self.id))
        
    def getCost(self):
        return(self.cost)
        
    def getLine(self):
        if 'stderr' in locals():
            if (self.stderr.poll(0.05)):
                s = self.process.stderr.readline().strip()
                if (s != b""):
                    return(s)
                else:
                    return(None)
        if 'stdout' in locals():
            if (self.stdout.poll(0.05)):
                s = self.process.stdout.readline().strip()
                if (s != b""):
                    return(s)
                else:
                    return(None)
            else:
                return(None)
            
    def mgmtConnect(self, ip, port):
        self.mgmtip = ip
        self.mgmtport = port
        if (ip == "socket"):
            self.mgmt = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        else:
            self.mgmt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        i = 0
        while (i < 50):
            try:
                if (ip == "socket"):
                    self.mgmt.connect(self.mgmtfile)
                else:
                    self.mgmt.connect((ip, int(port)))
            except socket.error:
                time.sleep(self.SOCKET_TIMEOUT)
                i += 1
            else:
                break
        self.mgmt.settimeout(self.SOCKET_TIMEOUT)
        
    def mgmtRead(self, inside=None):
        line = ""
        try:
            while True:
                self.mgmt.settimeout(self.SOCKET_TIMEOUT)
                c = self.mgmt.recv(1).decode("utf-8")
                if c != "\n" and c != "":
                    line += c
                else:
                    break
        except socket.timeout:
            pass
        except OSError:
            if (inside):
                logging.error("%s[%s]-mgmt-in: Cannot reconnect. Exiting!" % (self.type, self.id))
                sys.exit(2)
            else:
                logging.info("%s[%s]-mgmt-in: reconnecting." % (self.type, self.id))
                self.mgmtConnect(self.mgmtip, self.mgmtport)
                return(self.mgmtRead(True))
        else:
            pass
        if (line != ""):
            logging.debug("%s[%s]-mgmt-in: %s" % (self.type, self.id, repr(line)))
            self.mgmtEvent(line)
            return(line)
        else:
            return(None)
        
    def mgmtWrite(self, msg, inside=None):
        try:
            logging.debug("%s[%s]-mgmt-out: %s" % (self.type, self.id, repr(msg)))
            self.mgmt.send(msg.encode())
        except socket.timeout:
            pass
        except OSError:
            if (inside):
                logging.error("%s[%s]-mgmt-out: Cannot reconnect. Exiting!" % (self.type, self.id))
                sys.exit(2)
            else:
                logging.info("%s[%s]-mgmt-out: reconnecting." % (self.type, self.id))
                self.mgmtConnect(self.mgmtip, self.mgmtport)
                return(self.mgmtWrite(msg, True))
        else:
            pass
        
    def mgmtEvent(self, msg):
        pass
    
    def addAuthId(self, authid):
        return(True)
        
    def delAuthId(self, authid):
        return(True)

    def isAlive(self):
        self.process.poll()
        return(self.process.returncode == None)
    
    def getCost(self):
        return(self.cost)
    
    def getName(self):
        return(self.name)
    
    def getType(self):
        return(self.type)
    
    def getId(self):
        return(self.id)
    
    def show(self):
        logging.info("Service %s (%s), id %s" % (self.getName(), self.getType(), self.getId()))