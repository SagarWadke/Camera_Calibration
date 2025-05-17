import numpy as np
import cv2 as cv
import glob
from calibration.utils import show_image

def checker_objp_imgp(chessboardSize, size_of_chessboard_squares_mm,image_format):	
    """
    This function prepares the object points and image points for camera calibration using a checkerboard pattern.
    It reads images from the current directory, finds chessboard corners, and displays the images with detected corners.
    """
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob(image_format)
    print(f"\nTotal number of images: {len(images)}\n")

    for image in images:
        img = cv.imread(image)
        #cv.imshow('png', img)
        #show_image(img)
        cv.waitKey(2)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #cv.imshow('png', gray)
        #show_image(gray)
        cv.waitKey(2)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)
        # If found, add object points, image points (after refining them)

        if ret == True:

            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv.drawChessboardCorners(img, chessboardSize, corners2, ret)

            show_image(img)
            print(f"\nProcessing image: {image}\n")
            cv.waitKey(1000)

    cv.destroyAllWindows()
    return objpoints, imgpoints, images

def asy_cir_objp_imjp(cols,rows,diagonal_spacing_mm,image_format):
    """
    This function prepares the object points and image points for camera calibration using an asymmetric circle pattern.
    It reads images from the current directory, finds circle centers, and displays the images with detected circles.
    """

    def generate_obj_pts(cols, rows, diagonal_spacing_mm):
        num_rows = int(rows / 2)
        objp = np.zeros((num_rows * cols, 3), dtype=np.float32)
        l = 0
        for i in range(cols):
            for j in range(num_rows):
                x = i * diagonal_spacing_mm * np.sqrt(2) / 2
                y = j * diagonal_spacing_mm * np.sqrt(2) + (diagonal_spacing_mm * np.sqrt(2) / 2) * (i % 2)
                objp[l] = (x, y, 0)
                l = l + 1        
        return objp
    # prepare object points (world coordinates of circle centers)
    objp = generate_obj_pts(cols,rows,diagonal_spacing_mm)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob(image_format)
    print(f"\nTotal number of images: {len(images)}\n")

    # Circle detection parameters
    params = cv.SimpleBlobDetector_Params()

    #Change the thresholds
    params.minThreshold = 10
    params.maxThreshold = 200

    #Filter by Area
    params.filterByArea = True
    params.minArea = 64
    params.maxArea =2500

    # #Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # #Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.5

    # #Filter by Convexity
    params.filterByConvexity =True
    params.minConvexity =0.4

    detector = cv.SimpleBlobDetector_create(params)
    rows= int(rows / 2)
    for image in images:
        # Detect circles in the image
        img =cv.imread(image)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        keypoints = detector.detect(gray_img)

        im_with_keypoints = cv.drawKeypoints(img, keypoints, np.array([]), (0,255,0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        ret, corners = cv.findCirclesGrid(im_with_keypoints, (rows,cols), None, flags = cv.CALIB_CB_ASYMMETRIC_GRID)

        if ret == True:

            objpoints.append(objp)
            imgpoints.append(corners)
            
            im_with_keypoints = cv.drawChessboardCorners(img, (rows,cols), corners, ret)

            show_image(im_with_keypoints)
            print(f"\nProcessing image: {image}\n")
            cv.waitKey(1000)
        
    cv.destroyAllWindows()
    return objpoints, imgpoints, images     

def charuco_objp_imjp(cols, rows, square_length, marker_length, aruco_dict, image_format):
    """
    This function prepares the object points and image points for camera calibration using a Charuco board pattern.
    It reads images from the current directory, finds Aruco markers, and displays the images with detected corners of Aruco.
    """
    # Use the user-specified dictionary
    aruco_dict = cv.aruco.getPredefinedDictionary(aruco_dict)

    # Create the Charuco board
    charuco_board = cv.aruco.CharucoBoard(
        (cols,rows),
        squareLength=square_length,
        markerLength=marker_length,
        dictionary=aruco_dict
    )

    # Arrays to store object points and image points from all the images
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in image plane
    ids_all = []  # Charuco IDs

    images = glob.glob(image_format)
    print(f"\nTotal number of images: {len(images)}\n")

    for image in images:
        img = cv.imread(image)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Detect Aruco markers in the image
        corners, ids, _ = cv.aruco.detectMarkers(gray, aruco_dict)

        # If markers are detected, interpolate Charuco corners
        if ids is not None:
            response, charuco_corners, charuco_ids = cv.aruco.interpolateCornersCharuco(
                markerCorners=corners,
                markerIds=ids,
                image=gray,
                board=charuco_board
            )

            if response > 0:
                objpoints.append(charuco_board.getChessboardCorners())
                imgpoints.append(charuco_corners)
                ids_all.append(charuco_ids)

                # Draw the detected Charuco corners
                img = cv.aruco.drawDetectedCornersCharuco(
                    image=img,
                    charucoCorners=charuco_corners,
                    charucoIds=charuco_ids
                )

                # Display the image
                show_image(img)
                print(f"\nProcessing image: {image}\n")
                cv.waitKey(1000)

    cv.destroyAllWindows()
    return objpoints, imgpoints,ids_all,charuco_board, images