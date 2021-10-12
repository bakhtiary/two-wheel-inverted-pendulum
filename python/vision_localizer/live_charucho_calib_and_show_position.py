import traceback

import numpy as np

from Boards import big_board_20x20, robot_marker_board
from Calib_Dir import Calib_Dir
from Calibrator import Calibrator
from CameraEye import CameraEye
import multiprocessing as mp
import cv2

from gl_tools.visualization_of_board import runBoardLocationViewer


class Board_Location_Finder:

    def __init__(self, board_factory_func, eye: CameraEye):
        self.board_factory_func = board_factory_func
        self.cameraEye: CameraEye = eye
        self.location_pipe = mp.Queue()

    def start(self):
        self.job = mp.Process(target=Board_Location_Finder.run, args=(self,))
        self.job.start()

    def run(self):
        self.cameraEye.open_eyes()
        board, length_rate = self.board_factory_func()
        while True:

            retval, image = self.cameraEye.get_next_image()
            cv2.imshow("frame", image)
            cv2.pollKey()

            markerCorners, markerIds, rejected = cv2.aruco.detectMarkers(image, board.dictionary)

            try:
                retval, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(markerCorners, markerIds, image, board)

                rvec = np.zeros((3))
                tvec = np.zeros((3))
                success = cv2.aruco.estimatePoseCharucoBoard(np.array(charucoCorners), np.array(charucoIds), board, self.cameraEye.calibration_matrix, self.cameraEye.dist_coef, rvec, tvec)
                if success:
                    self.location_pipe.put((rvec, tvec))
            except:
                traceback.print_stack()



class Board_Location_Viewer:
    def __init__(self, finder):
        self.location_pipe = finder.location_pipe
        self.job = None

    def start(self):
        self.job = mp.Process(target=Board_Location_Viewer._run, args=(self,))
        self.job.start()

    def _run(self):
        runBoardLocationViewer(self.location_pipe)

    def wait_till_finish(self):
        self.job.join()


if __name__ == "__main__":
    calib_board,_ = big_board_20x20()

    calibrator = Calibrator(calib_board)

    eye = CameraEye.c29_webcam_linux_eye()
    eye.open_eyes()
    calibrator.calibrate(Calib_Dir("calib_dir/1/"), eye)
    eye.close_eyes()

    mp.set_start_method('spawn')
    finder = Board_Location_Finder(robot_marker_board, eye)
    viewer = Board_Location_Viewer(finder)

    finder.start()
    viewer.start()

    viewer.wait_till_finish()

