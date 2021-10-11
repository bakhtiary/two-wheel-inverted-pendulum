import os
import time
import traceback
import cv2

import numpy as np

from Boards import big_board_20x20
from Calib_Dir import Calib_Dir
from CameraEye import CameraEye


class Calibrator:
    def __init__(self, calib_board):
        self.board = calib_board
        self.all_ids = []
        self.all_corners = []

    def calibrate(self, calib_dir: Calib_Dir, cameraEye: CameraEye, force_recalib=False):

        if force_recalib or not os.path.isfile(calib_dir.calibration_matrix_filename()):
            self.load_from_dir(calib_dir)
            self.start_calibration(calib_dir, cameraEye)
        else:
            calib_params = self.load_calibration_parameters(calib_dir)
            cameraEye.set_calibration_parameters(*calib_params)

    def start_calibration(self, calib_dir: Calib_Dir, cameraEye: CameraEye):
        i = 0
        start_time = time.time_ns()
        while (True):
            cur_time = time.time_ns()
            i += 1
            ret, frame = cameraEye.get_next_image()
            corners, ids, res3 = cv2.aruco.detectMarkers(frame, self.board.dictionary)
            frame_copy = frame.copy()
            try:
                res2 = cv2.aruco.interpolateCornersCharuco(corners, ids, frame, self.board)
                retval2, charucoCorners, charucoIds = res2
                cv2.aruco.drawDetectedCornersCharuco(frame_copy, charucoCorners)
            except Exception as e:
                traceback.print_exc()

            cv2.aruco.drawDetectedMarkers(frame_copy, corners, ids)

            cv2.imshow('frame', frame_copy)

            key = cv2.pollKey()
            if key != -1:
                char_code = key & 0xFF
                the_char = chr(char_code)
                if char_code == ord('q'):
                    break
                if char_code == ord('2'):
                    cv2.waitKey(0)

                elif char_code == ord('a'):
                    print("going to add this image")
                    try:
                        self.add_to_calibration(frame)
                        cv2.imwrite(calib_dir.get_next_image_name(), frame)
                    except:
                        print("oops couldn't do it")
                        traceback.print_exc()
                elif the_char.lower() in cameraEye.capability_map:
                    cameraEye.send_event(the_char)

                elif char_code == ord('i'):
                    delta_time = (cur_time - start_time) / 1000_000_000
                    print(i, delta_time, i / (delta_time))
                    print(frame.shape)
                    cameraEye.print_spec_values()
                elif char_code == ord('r'):
                    calib_params = self.compute_calibration_parameters(frame)
                    print(calib_params)
                    self.save_calibration_parameters(calib_dir,*calib_params)
                    cameraEye.set_calibration_parameters(*calib_params)
                else:
                    print(f"key: {key} not understood")

    def compute_calibration_parameters(self, frame):
        res = cv2.aruco.calibrateCameraCharucoExtended(
            self.all_corners, self.all_ids, self.board,
            frame.shape[0:2], None, None
        )
        retval, cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsIntrinsics, stdDeviationsExtrinsics, perViewError = res
        print("printing rvecs")
        print(rvecs)
        print("printing tvecs")
        print(tvecs)
        return cameraMatrix, distCoeffs

    def add_to_calibration(self, frame):
        corners, ids, res3 = cv2.aruco.detectMarkers(frame, self.board.dictionary)
        res2 = cv2.aruco.interpolateCornersCharuco(corners, ids, frame, self.board)
        retval2, charucoCorners, charucoIds = res2

        if charucoIds is not None and len(charucoIds) > 6:
            self.all_ids.append(charucoIds)
            self.all_corners.append(charucoCorners)

    def load_from_dir(self, calib_dir: Calib_Dir):

        for image_filename in calib_dir.stored_image_files():
            print(image_filename)
            image = cv2.imread(image_filename)
            self.add_to_calibration(image)

    def save_calibration_parameters(self, calib_dir: Calib_Dir, cameraMatrix, distCoeffs):
        np.savetxt(calib_dir.calibration_matrix_filename(), cameraMatrix)
        np.savetxt(calib_dir.calibration_distCoefs_filename(), distCoeffs)

    def load_calibration_parameters(self, calib_dir):
        mat = np.loadtxt(calib_dir.calibration_matrix_filename())
        dist_coefs = np.loadtxt(calib_dir.calibration_distCoefs_filename())
        return mat, dist_coefs


if __name__ == "__main__":
    from Calib_Dir import Calib_Dir
    from CameraEye import CameraEye

    calib_board, _q = big_board_20x20()

    calibrator = Calibrator(calib_board)
    eye = CameraEye.c29_webcam_linux_eye()
    eye.open_eyes()
    calibrator.calibrate(Calib_Dir("calib_dir/1/"), eye, True)

