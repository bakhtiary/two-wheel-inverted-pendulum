import cv2


def big_board_20x20():
    d = cv2.aruco_Dictionary.get(cv2.aruco.DICT_4X4_250)
    return cv2.aruco.CharucoBoard_create(10, 10, 0.20, 0.16, d), 0.20/0.16

def robot_marker_board():
    d = cv2.aruco_Dictionary.get(cv2.aruco.DICT_4X4_250)
    board = cv2.aruco.CharucoBoard_create(7, 7, 0.14, 0.11, d)
    board_length_rate = 0.14 / 0.11
    return board, board_length_rate
