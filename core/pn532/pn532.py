
# Define the APDU commands
ACS_DISABLE_AUTO_POLL = ['ff', '00', '51', '3f', '00']
ACS_LED_ORANGE = ['ff', '00', '40', '0f', '04', '00', '00', '00', '00']
ACS_GET_READER_FIRMWARE = ['ff', '00', '48', '00', '00']
ACS_DIRECT_TRANSMIT = ['ff', '00', '00', '00']
GET_PN532_FIRMWARE = ['d4', '02']
TG_INIT_AS_TARGET = ['d4', '8c']
TG_GET_DATA = ['d4', '86']
TG_SET_DATA = ['d4', '8e']
ISO_OK = ['90', '00']

# Define the PN532 functions
PN532_OK = [0xD5, 0x03]
PN532_FUNCTIONS = {
    0x01: 'ISO/IEC 14443 Type A',
    0x02: 'ISO/IEC 14443 Type B',
    0x04: 'ISO/IEC 18092',
}

class PN532():

    def to_bytes(self, hex_list):
        # Convert a list of hex strings to a list of bytes
        return [int(byte, 16) if isinstance(byte, str) else byte for byte in hex_list]

    def send_apdu(self, connection, apdu_hex):
        # Send an APDU command and print the response
        apdu = to_bytes(apdu_hex)
        print(f"Sending APDU: {apdu}")
        try:
            response, sw1, sw2 = connection.transmit(apdu)
            print(f"Response: {response}")
            print(f"Status words: {sw1:02X} {sw2:02X}")
            
            if not response:
                print(f"No data returned, but status words: {sw1:02X} {sw2:02X}")
                return None, sw1, sw2

            return response, sw1, sw2

        except Exception as e:
            print(f"Exception during APDU transmission: {e}")
            return None, None, None

    def pn532_print_firmware(self, data):
        # Print the PN532 firmware information Thanks to RFIDIOT for this code :)
        if data[:2] != PN532_OK:
            print('  Bad data from PN532:', data)
        else:
            print('       IC:', data[2])
            print('      Rev: %d.%d' % (data[3] >> 4, data[3] & 0x0F))
            print('  Support:', end=' ')
            support = data[4]
            spacing = ''
            for n in PN532_FUNCTIONS.keys():
                if support & n:
                    print(spacing + PN532_FUNCTIONS[n])
                    spacing = '           '

