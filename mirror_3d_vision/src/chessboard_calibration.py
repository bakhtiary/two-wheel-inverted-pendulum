from glob import glob

import numpy as np
import cv2 as cv

import cv2.aruco

# termination criteria
from gl_tools.visualization_of_camera import runCalibrationViewer

spot_dims = (4,5)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((spot_dims[0]*spot_dims[1],3), np.float32)
objp[:,:2] = np.mgrid[0:spot_dims[0],0:spot_dims[1]].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob("mirrors_fotos/separate_rigs/*.jpg")
image_names = []
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    print(f"paring {fname}")

    ret, corners = cv.findCirclesGrid(gray, spot_dims)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        # corners2 = cv.cir(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        image_names.append(fname)
        # Draw and display the corners
        cv.drawChessboardCorners(img, spot_dims, corners, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
    else:
        print("not found")

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


print(tvecs)
print(rvecs)
print(ret)
print(mtx)
print(dist)

img = cv.imread(images[0])
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imshow('img', dst)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )

cv.waitKey(0)

runCalibrationViewer(tvecs, rvecs, image_names)