import core.pn532.reader as reader

from core.plugin import BasePwnhyvePlugin
from core.utils import config

card_reader = reader.pPN532()

class PWN_Nfc(BasePwnhyvePlugin):

    def read(tpil):

        a = tpil.gui.screenConsole(tpil)
        a.addText("reading")

        tpil.waitForKey()
        a.exit() 
        pass