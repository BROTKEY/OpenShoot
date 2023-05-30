import cv2
import numpy as np
import math
import socket

ip = "127.0.0.1"
port = 5005
address = (ip, port)

datasocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
datasocket.bind(address)
img = cv2.imread("Luftgewehrscheibe.jpg")
height, width, _ = img.shape
last_pixel = 0

while True:
    data, addr = datasocket.recvfrom(1024)

    data = data.decode("utf-8")
    data = data.split(";")
    pixel = (int((float(data[0])*-1)/3*271 + height/2), int((float(data[1])*-1)/3*271 + width/2))
    if last_pixel == 0:
        last_pixel = pixel
    print(pixel)

    img = cv2.line(img, last_pixel, pixel, (0, 0, 255), 1)

    last_pixel = pixel

    cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit()