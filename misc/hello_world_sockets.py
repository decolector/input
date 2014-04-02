from socket import *
s = socket(AF_INET, SOCK_STREAM)
addr = ("192.168.1.105",9520)
s.connect(addr)
string = '015A3030024141061B30621C311A310A49310A4F3157656C636F6D6504'
hex_str = string.decode("hex")
data = bytearray(hex_str)
s.send(data)
s.close()