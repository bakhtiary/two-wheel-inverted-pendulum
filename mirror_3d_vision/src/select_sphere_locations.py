from math import sqrt

import cv2

clickx, clicky = 0, 0
radius = 0
drawing = False
image_name = '1.jpg'
circles_filename = image_name + ".txt"
image = cv2.imread(image_name)


def save_circles(filename, circles):
    with open(filename, "w") as f:
        for circle in circles:
            f.write(f"{int(circle[0])},{int(circle[1])},{int(circle[2])}\n")
    return circles


def load_circles(filename):
    loaded_circles = []
    try:
        with open(filename) as f:
            for line in f.readlines():
                circle = list(map(lambda x: int(float(x)), line.split(",")))
                loaded_circles.append(circle)
    except FileNotFoundError as e:
        print("starting fresh")
    return loaded_circles


circles = load_circles(circles_filename)


def draw_window():
    output = image.copy()
    cv2.circle(output, (clickx, clicky), int(radius), (0, 255, 0), 1)
    for circle in circles:
        cv2.circle(output, (circle[0], circle[1]), int(circle[2]), (0, 128, 255), 1)
    cv2.imshow('image', output)


def select_circle(event, x, y, flags, param):
    # grab references to the global variables
    global clickx, clicky, radius, drawing
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        # refPt = [(x, y)]
        clickx, clicky = x, y
        radius = 0
        drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        # refPt.append((x, y))
        drawing = False
        # draw a rectangle around the region of interest
    elif drawing:
        radius = sqrt((clickx - x) ** 2 + (clicky - y) ** 2)
    draw_window()


draw_window()
cv2.setMouseCallback("image", select_circle)

def removeDuplicates(lst):
    return list(set([tuple(i) for i in lst]))

while True:
    key = cv2.waitKeyEx(0)
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('s'):
        save_circles(circles_filename, circles)
        print("saved\n")
    if key & 0xFF == ord('r'):
        circles = removeDuplicates(circles)
        print("removed duplicates\n")
    if key & 0xFF == ord('a'):
        circles.append((clickx, clicky, radius))
    if key & 0xFF == ord('+'):
        radius += 1
    if key & 0xFF == ord('-'):
        radius -= 1
    if key == 2555904:
        clickx += 1
    if key == 2424832:
        clickx -= 1
    if key == 2621440:
        clicky += 1
    if key == 2490368:
        clicky -= 1

    draw_window()

cv2.destroyAllWindows()
