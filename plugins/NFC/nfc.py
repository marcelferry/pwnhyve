import core.pn532.pn532 as pn532

# Import pyscard
from smartcard.System import readers
from smartcard.CardConnection import CardConnection
from smartcard.scard import SCARD_SHARE_DIRECT

from core.plugin import BasePwnhyvePlugin
from core.utils import config

# Test based on this article 
# https://osintteam.blog/nfc-card-emulation-1831c67e1304
# https://github.com/m5kro/acr122u-emulation/tree/main

card_reader = pn532.PN532()

class PWN_Nfc(BasePwnhyvePlugin):

    def read(tpil):

        a = tpil.gui.screenConsole(tpil)
        a.addText("reading")

        # Get the list of available readers
        reader_list = readers()
        if not reader_list:
            a.addText("No readers found")
            return

        # Use the first available reader
        reader = reader_list[0]
        a.addText(f"Using reader: {reader}")

        # Create a connection to the reader
        connection = reader.createConnection()
        try:
            # Connect in direct mode with raw protocol
            connection.connect(protocol=CardConnection.RAW_protocol, mode=SCARD_SHARE_DIRECT)
            print("Connected to reader")

            # Begin self test commmands

            # Send the disable auto poll command
            _, sw1, sw2 = card_reader.send_apdu(connection, pn532.ACS_DISABLE_AUTO_POLL)
            if sw1 == 0x90:
                print("Auto poll disabled successfully")
            else:
                print("Failed to disable auto poll")
                return

            # Send the LED orange command
            _, sw1, sw2 = card_reader.send_apdu(connection, pn532.ACS_LED_ORANGE)
            if sw1 == 0x90:
                print("LED set to orange successfully")
            else:
                print("Failed to set LED to orange")
                return

            # Send the get reader firmware command
            response, sw1, sw2 = card_reader.send_apdu(connection, pn532.ACS_GET_READER_FIRMWARE)
            response.append(sw1)
            response.append(sw2)
            try:
                firmware_version = ''.join(chr(b) for b in response)
                print(f"Reader firmware version: {firmware_version}")
            except Exception as e:
                print(f"Failed to get reader firmware: {e}")
                return

            # Send the direct transmit command with GET_PN532_FIRMWARE
            full_command = pn532.ACS_DIRECT_TRANSMIT + [len(pn532.GET_PN532_FIRMWARE)] + pn532.GET_PN532_FIRMWARE
            response, sw1, sw2 = card_reader.send_apdu(connection, full_command)
            if sw1 == 0x90:
                card_reader.pn532_print_firmware(response)
            else:
                print("Failed to get PN532 firmware")
                return

            # End self test commands

            # Begin emulation commands

            # Arguments for TG_INIT_AS_TARGET
            mode = '00' # 00 = Passive Only 01 = DEP Only 02 = PICC Only
            sens_res = '0400' # 0400 or 0800 try both
            nfcid1t = '000000'
            sel_res = '20' # 40 = DEP 60 = DEP and PICC 20 = PICC
            nfcid2t = '0000000000000000'
            pad = '0000000000000000'
            system_code = '0000'
            nfcid3t = '00000000000000000000'
            general_bytes = ''
            historical_bytes = ''

            init_as_target_command = pn532.TG_INIT_AS_TARGET + card_reader.to_bytes([mode]) + card_reader.to_bytes(sens_res) + card_reader.to_bytes(nfcid1t) + card_reader.to_bytes(sel_res) + card_reader.to_bytes(nfcid2t) + card_reader.to_bytes(pad) + card_reader.to_bytes(system_code) + card_reader.to_bytes(nfcid3t) + [len(card_reader.to_bytes(general_bytes))] + card_reader.to_bytes(general_bytes) + [len(card_reader.to_bytes(historical_bytes))] + card_reader.to_bytes(historical_bytes)
            init_as_target_command = pn532.ACS_DIRECT_TRANSMIT + [len(init_as_target_command)] + init_as_target_command

            # Send the direct transmit command with TG_INIT_AS_TARGET
            response, sw1, sw2 = card_reader.send_apdu(connection, init_as_target_command)
            if sw1 == None:
                print("TG_INIT_AS_TARGET command sent successfully")
            else:
                print("Failed to send TG_INIT_AS_TARGET command")
                return

            # Send the direct transmit command with TG_GET_DATA
            full_command = pn532.ACS_DIRECT_TRANSMIT + [len(pn532.TG_GET_DATA)] + pn532.TG_GET_DATA
            response, sw1, sw2 = card_reader.send_apdu(connection, full_command)
            if sw1 == 0x90:
                print(f"TG_GET_DATA returned: {response}")
            else:
                print("Failed to get data with TG_GET_DATA")
                return

            # Send the direct transmit command with TG_SET_DATA and ISO_OK
            tg_set_data_command = pn532.TG_SET_DATA + pn532.ISO_OK
            full_command = pn532.ACS_DIRECT_TRANSMIT + [len(tg_set_data_command)] + tg_set_data_command
            response, sw1, sw2 = card_reader.send_apdu(connection, full_command)
            if sw1 == 0x90:
                print("TG_SET_DATA command sent successfully")
            else:
                print("Failed to send TG_SET_DATA command")

        except Exception as e:
            print(f"Error: {e}")


        tpil.waitForKey()
        a.exit() 
        pass