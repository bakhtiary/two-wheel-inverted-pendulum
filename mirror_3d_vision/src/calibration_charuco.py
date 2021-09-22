from glob import glob

import numpy as np
import cv2 as cv

# termination criteria
from gl_tools.visualization_of_camera import runCalibrationViewer

spot_dims = (4,5)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((spot_dims[0]*spot_dims[1],3), np.float32)
objp[:,:2] = np.mgrid[0:spot_dims[0],0:spot_dims[1]].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob("charucho_fotos/1.jpg")
image_names = []
d = cv.aruco_Dictionary.get(cv.aruco.DICT_4X4_50)
board = cv.aruco.CharucoBoard_create(9,10,0.10,0.08,d)

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    print(f"paring {fname}")
    corners, ids, res3 = cv.aruco.detectMarkers(img, d)

    # If found, add object points, image points (after refining them)
    if corners:
        # objpoints.append(objp)
        # # corners2 = cv.cir(gray,corners, (11,11), (-1,-1), criteria)
        # imgpoints.append(corners)
        image_names.append(fname)
        # Draw and display the corners
        cv.aruco.drawDetectedMarkers(img,corners)

        cv.imshow('img', img)
        cv.waitKey(500)
    else:
        print("not found")

cv.destroyAllWindows()

# ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
res = cv.aruco.calibrateCameraArucoExtended(np.array(corners), ids,np.array([17]), board, img.shape[0:2], None, None)
retval, cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsIntrinsics, stdDeviationsExtrinsics, perViewErrors = res

print(tvecs)
print(rvecs)

runCalibrationViewer(tvecs, rvecs, image_names)