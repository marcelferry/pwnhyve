# Import pyscard
#from smartcard.System import readers
#from smartcard.CardConnection import CardConnection
#from smartcard.scard import SCARD_SHARE_DIRECT

from core.plugin import BasePwnhyvePlugin
from core.utils import config

class NFC(BasePwnhyvePlugin):

    def read(tpil):
        a = tpil.gui.screenConsole(tpil)
        a.text = (scText("Reading"))
        tpil.waitForKey()
        a.exit() 
        pass