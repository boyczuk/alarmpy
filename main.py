import threading
import winsound

import cv2
import imutils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# grabs return value from camera
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21,21), 0)

# is alarm active
alarm = False
alarm_mode = False
alarm_counter = 0

# when alarm event occurs
def security_alarm():
    global alarm
    for _ in range(5):
        # exit if alarm is out of alarm mode (press t)
        if not alarm_mode:
            break

        print("ALARM")
        winsound.Beep(2500, 1000)
    alarm = False


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    # if in alarm mode
    if alarm_mode:
        # Turn into black and white
        frame_bw  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        # everything above threshold is white, everything below is black
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        # motion sensitivity (lower is more sensitive)
        if threshold.sum() > 300:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            # create different threads for the alarm
            threading.Thread(target=security_alarm).start()

    # key to break out of alarm
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()
