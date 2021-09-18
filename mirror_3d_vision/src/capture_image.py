# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(0)
focus = 10
vid.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # turn the autofocus off
vid.set(cv2.CAP_PROP_FOCUS, focus)

current_image_number = 2
while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    key = cv2.waitKey(1)
    if key != -1:
        if key & 0xFF == ord('q'):
            break

        if key & 0xFF == ord('s'):
            cv2.imwrite(f"{current_image_number}.jpg", frame)
            current_image_number += 1

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
