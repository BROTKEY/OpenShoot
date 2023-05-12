import cv2
import numpy as np

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# cap.set(cv2.CAP_PROP_FPS, 120)

cap = cv2.VideoCapture("1.mp4")

scaling_factor = 1
crop_factor = 12
while True:
    ret, original_frame = cap.read()
    try:
        frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
        org_height, org_width = frame.shape
        height, width = frame.shape
        cv2.medianBlur(frame, 5)

        height, width = frame.shape

        bin = cv2.threshold(
            frame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

        contours, hierarchy = cv2.findContours(
            bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        areas = np.array([cv2.contourArea(cnt) for cnt in contours])
        idxs = areas.argsort()
        cnts2 = [contours[i] for i in idxs]
        c = [cnts2[-1]]
        cv2.drawContours(original_frame, c, -1, (255, 255, 255), 1)
        (x, y, w, h) = cv2.boundingRect(c[0])
        cv2.rectangle(bin, (x, y), (x+w, y+h), (0, 0, 0), 2)

        center_target = np.mean([[x, y], [x+w, y+h]], axis=0)

        center_target = np.mean(c[0][0:, 0], axis=0)

        frame = frame[int(center_target[1]-height/crop_factor):int(center_target[1]+height/crop_factor),
                      int(center_target[0]-width/crop_factor):int(center_target[0]+width/crop_factor)]

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
        c = [cnts2[-2]]
        (x, y, w, h) = cv2.boundingRect(c[0])

        center = np.mean([[x, y], [x+w, y+h]], axis=0)

        cv2.circle(bin, np.intp(np.rint(center)), 1,
                   (255, 255, 255), 30*scaling_factor)

        cv2.imshow("bin2", bin)

        absolut_center = ((center_target[0])+(center[0] - width/2)/scaling_factor,
                          (center_target[1])+(center[1] - height/2)/scaling_factor)

        cv2.circle(original_frame, np.intp(
            np.rint(absolut_center)), 1, (255, 255, 255), 20)
    except:
        pass

    cv2.imshow("Frame", original_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
