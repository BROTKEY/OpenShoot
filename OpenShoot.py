import cv2
import numpy as np
import math
import socket

ip = "127.0.0.1"
port = 5005
address = (ip, port)

datasocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# cap.set(cv2.CAP_PROP_FPS, 120)

cap = cv2.VideoCapture("1.mp4")

scaling_factor = 3
crop_factor = 12
while True:
    ret, original_frame = cap.read()
    try:
        frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
        org_height, org_width = frame.shape
        orgheight, orgwidth = frame.shape
        cv2.medianBlur(frame, 5)

        height, width = frame.shape

        frame = frame[int(height/2-height/4):int(height/2+height/4),
                      int(width/2-width/4):int(width/2+width/4)]

        cv2.imshow("bin3", frame)

        bin = cv2.threshold(
            frame, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

        contours, hierarchy = cv2.findContours(
            bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        areas = np.array([cv2.contourArea(cnt) for cnt in contours])
        idxs = areas.argsort()
        cnts2 = [contours[i] for i in idxs]
        c = [cnts2[-1]]
        (x, y, w, h) = cv2.boundingRect(c[0])
        cv2.rectangle(bin, (x, y), (x+w, y+h), (0, 0, 0), 2)

        center_target = np.mean([[x, y], [x+w, y+h]], axis=0)

        center_target = np.mean(c[0][0:, 0], axis=0)

        frame = frame[math.ceil(center_target[1]-math.ceil(height/crop_factor)):math.ceil(center_target[1]+math.ceil(height/crop_factor)),
                      math.ceil(center_target[0]-math.ceil(width/crop_factor)):math.ceil(center_target[0]+math.ceil(width/crop_factor))]

        height, width = frame.shape

        frame = cv2.resize(frame, (width*scaling_factor, height*scaling_factor),
                           interpolation=cv2.INTER_LINEAR)
        cv2.medianBlur(frame, 5)

        height, width = frame.shape

        bin = cv2.threshold(
            frame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

        contours, hierarchy = cv2.findContours(
            bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        areas = np.array([cv2.contourArea(cnt) for cnt in contours])
        idxs = areas.argsort()
        cnts2 = [contours[i] for i in idxs]

        if len(cnts2) > 2:
            raise Exception("No contours found")

        c = [cnts2[-2]]
        (x, y, w, h) = cv2.boundingRect(c[0])

        center = np.mean([[x, y], [x+w, y+h]], axis=0)

        cv2.circle(bin, np.intp(np.rint(center)), 1,
                   (255, 255, 255), 30*scaling_factor)

        cv2.imshow("bin2", bin)

        absolut_center = ((center_target[0]-orgwidth/2)+(center[0] - width/2)/scaling_factor,
                          (center_target[1]-orgheight/2)+(center[1] - height/2)/scaling_factor)
        
        distance = np.array(absolut_center) * 0.03
        distance = distance - [-10.27255258,-5.90265774]
        datasocket.sendto((str(distance[0]) + ";" + str(distance[1])).encode(), address)
    except:
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
