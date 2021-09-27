# import the opencv library
import cv2
import numpy as np
import time

# define a video capture object
vid = cv2.VideoCapture(0)
focus = 10
vid.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # turn the autofocus off
vid.set(cv2.CAP_PROP_FOCUS, focus)

current_image_number = 2
i = 0
image = np.zeros((30, 30, 3), np.uint8)
start_time = time.time_ns()
while (True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    cur_time = time.time_ns()

    # cc = frame[0:64, 0:64,:].copy()
    # print(f"copy done {cc.shape}")
    # Display the resulting frame
    i+=1
    delta_time = (cur_time - start_time)/1000_000_000
    print(i, delta_time, i/(delta_time))

    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    key = cv2.pollKey()
    if key != -1:
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'):
            cv2.imwrite(f"{current_image_number}.jpg", frame)
            current_image_number += 1
        else:
            print(f"key: {key} not understood")

        if key & 0xFF == ord('+'):
            focus *= 1.1
            vid.set(cv2.CAP_PROP_FOCUS, focus)

        if key & 0xFF == ord('-'):
            focus *= 0.9
            vid.set(cv2.CAP_PROP_FOCUS, focus)


# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
