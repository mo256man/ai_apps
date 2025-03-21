from gpiozero import Button
import cv2
import datetime
import numpy as np
import time

cap = cv2.VideoCapture(0)

limit_pin = 21
limit_switch = Button(limit_pin, pull_up=True)

door_pin = 20
door_switch = Button(door_pin, pull_up=True)

is_mirror = False
is_last_open = False
try:
    while True:
        ret, frame = cap.read()
        if ret:
            if is_mirror:
                frame = cv2.flip(frame, 1)
                
            if limit_switch.value:
                limit_color = (0, 0, 255)
                limit_value = "ON"
            else:
                limit_color = (255, 255, 0)
                limit_value = "OFF"
                
            if door_switch.value:
                door_color = (255, 255, 0)
                door_value = "CLOSE"
                is_open = False
            else:
                door_color = (0, 0, 255)
                door_value = "OPEN"
                is_open = True
                
            dt = datetime.datetime.now()
            str_now = dt.strftime("%Y/%m/%d %H:%M:%S")
            text = f"time:{str_now}"
            cv2.putText(frame, text, (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,0), 3)
            cv2.putText(frame, "LS:", (20,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,0), 3)
            cv2.putText(frame, limit_value, (150,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, limit_color, 3)
            cv2.putText(frame, "door:", (20,150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,0), 3)
            cv2.putText(frame, door_value, (150,150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, door_color, 3)

            if is_open == True and is_last_open == False:
                str_dt = dt.strftime("%Y%m%d_%H%M%S")
                filename = f"{str_dt}.jpg"
                cv2.imwrite(filename, frame)
                
            cv2.imshow("camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            elif key == ord("m"):
                is_mirror = not is_mirror
            
except KeyboardInterrupt:
    patlite.clear()

cv2.destroyAllWindows()
cap.release()
