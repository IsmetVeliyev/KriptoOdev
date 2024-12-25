import cv2,imutils,socket
import numpy as np
import time
import base64
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes


client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
BUFF_SIZE = 65536
host_ip =socket.gethostbyname(socket.gethostname())
port=5051
adress = (host_ip,port)
WIDTH=400

key = b"salam222"
iv = b"sagol222"
xorkey1 = b"33332222"
xorkey2 = b"22223333"
cipher = DES.new(key, DES.MODE_CBC,iv)

vid = cv2.VideoCapture(0)
fps,st,frames_to_count,cnt = (0,0,20,0)


def xor_data(data, xor_key):
    return bytes([data[i] ^ xor_key[i % 8] for i in range(len(data))])


while(vid.isOpened):
    _,frame = vid.read()
    frame = imutils.resize(frame,width=WIDTH)
    _,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
    xor_plaintext=xor_data(buffer.tobytes(),xorkey1)
    padded_plaintext = pad(xor_plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    xor_ciphertext=xor_data(ciphertext,xorkey2)
    client_socket.sendto(xor_ciphertext,adress)
    cv2.imshow('TRANSMITTING VIDEO',frame)
    key = cv2.waitKey(1)
    if key==27:
        break


cv2.destroyAllWindows()
vid.release()
client_socket.close()




