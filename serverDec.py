import cv2,imutils,socket
import numpy as np
import time
import base64
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_ip =socket.gethostbyname(socket.gethostname())
port=5051
adress = (host_ip,port)
server_socket.bind(adress)

key = b"salam222"
iv = b"sagol222"
xorkey1 = b"33332222"
xorkey2 = b"22223333"
decipher = DES.new(key, DES.MODE_CBC, iv)

def xor_data(data, xor_key):
    return bytes([data[i] ^ xor_key[i % 8] for i in range(len(data))])


while True:
    
    packet,_ = server_socket.recvfrom(BUFF_SIZE)
    xored_data= xor_data(packet,xorkey2)
    dec_data = unpad(decipher.decrypt(xored_data), DES.block_size) 
    xor_data2 = xor_data(dec_data,xorkey1)
    npdata = np.frombuffer(xor_data2,dtype=np.uint8)
    frame = cv2.imdecode(npdata,1)
    if(not (frame is None)):
     cv2.imshow('RECEIVING VIDEO',frame)
    key = cv2.waitKey(1)
    if key==27:
        cv2.destroyAllWindows()
        break

server_socket.close()

