import time
import serial

port = '/dev/tty.NoZAP-PL2303-00002006'
baud = 19200
sign = serial.Serial(port, baud)
mess = "\x01\x5a\x30\x30\x02\x41\x41\x06\x1b\x30\x62\x1c\x31\x1a\x31\x0a\x49\x31\x0a\x4f\x31\x57\x65\x6c\x63\x6f\x6d\x65\x04"
sign.write(mess)