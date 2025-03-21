from gpiozero import Button
import cv2
import datetime
import numpy as np

def draw_caution(frame):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w-1, h-1), (0,0,255), 5)
    return frame

pin = 21
Button(pin).close()
switch = Button(pin, pull_up=True)
    
cap = cv2.VideoCapture(0)

def show_camera():
    last_status = False
    while True:
        is_open = not switch.value
        ret, frame = cap.read()
        if ret:
            dt = datetime.datetime.now()
            str_dt = dt.strftime("%Y/%m/%d %H:%M:%S")
            cv2.putText(frame, str_dt, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
            if is_open:
                if is_open != last_status:
                    filename = dt.strftime("%Y%m%d_%H%M%S") + ".jpg"
                    cv2.imwrite(fr"./output/{filename}", frame)
                    print("photo saved")
                frame = draw_caution(frame)
            last_status = is_open
            cv2.imshow("", frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
    cv2.destroyAllWindows()

show_camera()
cap.release()
switch.close()
