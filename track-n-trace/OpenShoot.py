import cv2
import numpy as np
import math
import serial
import threading
from websocket import create_connection

debug = True

trigger_state = 1

scaling_factor = 3
crop_factor = 12
area_tolerance = 50


def trace_data_collector():
    ser = serial.Serial('COM5', 115200, timeout=1)
    old = 0
    global trigger_state
    while True:
        ser.flushInput()
        serial_data = ser.readline().decode('ascii')
        data = int(serial_data)
        trigger_state = (data + old) / 2
        old = int(serial_data)


thread = threading.Thread(target=trace_data_collector)
thread.start()


def tracker():
    ws = create_connection("ws://localhost:8000/")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cap.set(cv2.CAP_PROP_FPS, 120)

    # cap = cv2.VideoCapture("../random-bs-go/1.mp4")
    while True:
        _, original_frame = cap.read()
        try:
            frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
            cv2.medianBlur(frame, 5)

            height, width = frame.shape

            frame = frame[int(height/2-height/4):int(height/2+height/4),
                          int(width/2-width/4):int(width/2+width/4)]
            orgheight, orgwidth = frame.shape

            if debug:
                cv2.imshow("bin3", frame)

            bin = cv2.threshold(
                frame, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

            contours, hierarchy = cv2.findContours(
                bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            areas = np.array([cv2.contourArea(cnt) for cnt in contours])
            idx = np.argwhere((areas > (1050-area_tolerance))
                              & (areas < (1050+area_tolerance)))

            if debug:
                cv2.imshow("bin7", bin)

            c = [contours[idx[0][0]]]
            (x, y, w, h) = cv2.boundingRect(c[0])

            bin = cv2.rectangle(bin, (x, y), (x+w, y+h), (0, 0, 0), 2)

            if debug:
                cv2.imshow("bin6", bin)

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

            contours, _ = cv2.findContours(
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

            if debug:
                cv2.imshow("bin2", bin)
                print((center_target[0]-orgwidth/2),
                      (center_target[1]-orgheight/2))

            absolut_center = ((center_target[0]-orgwidth/2)+(center[0] - width/2)/scaling_factor,
                              (center_target[1]-orgheight/2)+(center[1] - height/2)/scaling_factor)

            if debug:
                print(trigger_state)
            distance = np.array(absolut_center) * 0.03
            data = str(distance[0]) + ";" + str(distance[1]) + \
                ";" + str(trigger_state)

            ws.send(bytes(data, 'utf-8'))

            if debug:
                print(absolut_center)
                print(distance)
                print(data)

        except:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    tracker()
