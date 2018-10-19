
import logging

class Log(object):
    
    def __init__(self, handler=None, level=logging.WARNING):
        logging.basicConfig(level=level,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    )
        self.logger = logging.getLogger()
        if (handler):
            self.logger.addHandler(handler)
        self.logger.setLevel(level)
    
    def debug(self, msg, *args, **kwargs):
        return self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        return self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        return self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        return self.logger.error(msg, *args, **kwargs)
                
class Audit(object):
    
    ADD = "ADD"
    DEL = "DEL"
    KILL = "KILL"
    START  = "START"
    STOP  = "STOP"
    MODIFY = "MOD"
    UPLOAD = "UPLOAD"
    NPAYMENT = "NEED_PAYMENT"
    AUTHID =  "AUTHID"
    SESSION = "SESSION"
    SERVICE = "SERVICE"
    SWALLET = "SDP_WALLET"
    PWALLET = "PROVIDER_WALLET"
    SDP = "SDP"
    
    def __init__(self, handler=None, level=logging.INFO):
        self.logger = logging.getLogger('audit')
        if (handler):
            formatter = logging.Formatter('%(asctime)s %(message)s')
            handler.setFormatter(formatter)
        else:
            handler = logging.StreamHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def audit(self, action, type, obj=None, lthn=None, wallet=None, paymentid=None, srcip=None, dstip=None, msg=None):
        txt = "%s,%s,%s,%s,%s,%s,%s,%s,%s" % (action, type, obj, lthn, wallet, paymentid, srcip, dstip, msg)
        return(self.logger.info(txt))

L = None
A = None

