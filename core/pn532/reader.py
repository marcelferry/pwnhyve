import time
import binascii

from pn532pi import Pn532, pn532
from pn532pi import Pn532Hsu
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi

# Set the desired interface to True
SPI = False
I2C = False
HSU = True

class pPN532():

    def __init__(self):
        if SPI:
            PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
            self.nfc = Pn532(PN532_SPI)
        # When the number after #elif set as 1, it will be switch to HSU Mode
        elif HSU:
            PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
            self.nfc = Pn532(PN532_HSU)

        # When the number after #if & #elif set as 0, it will be switch to I2C Mode
        elif I2C:
            PN532_I2C = Pn532I2c(1)
            self.nfc = Pn532(PN532_I2C)
        pass

    def setup(self):
        print("-------Peer to Peer HCE--------")

        self.nfc.begin()

        versiondata = nfc.getFirmwareVersion()
        if not versiondata:
            print("Didn't find PN53x board")
            raise RuntimeError("Didn't find PN53x board")  # halt

        # Got ok data, print it out!
        print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                    (versiondata >> 8) & 0xFF))

        # Set the max number of retry attempts to read from a card
        # This prevents us from waiting forever for a card, which is
        # the default behaviour of the PN532.
        #nfc.setPassiveActivationRetries(0xFF)

        # configure board to read RFID tags
        self.nfc.SAMConfig()
    
    def readInfo(self):
        # Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
        # 'uid' will be populated with the UID, and uidLength will indicate
        # if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
        success, uid = self.nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

        if (success):
            print("Found a card!")
            print("UID Length: {:d}".format(len(uid)))
            print("UID Value: {}".format(binascii.hexlify(uid)))
            # Wait 1 second before continuing
            time.sleep(1)
            return True
        else:
            # pn532 probably timed out waiting for a card
            print("Timed out waiting for a card")
            return False
    
    def writeInfo(self):
        print("wait for a tag")
        # wait until a tag is present
        tagPresent = False
        while not tagPresent:
            time.sleep(.1)
            tagPresent, uid = self.nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

        # if NTAG21x enables r/w protection, uncomment the following line 
        # nfc.ntag21x_auth(password)

        status, buf = self.nfc.mifareultralight_ReadPage(3)
        capacity = int(buf[2]) * 8
        print("Tag capacity {:d} bytes".format(capacity))

        for i in range(4, int(capacity/4)):
            status, buf = self.nfc.mifareultralight_ReadPage(i)
            print(binascii.hexlify(buf[:4]))

        # wait until the tag is removed
        while tagPresent:
            time.sleep(.1)
            tagPresent, uid = self.nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

