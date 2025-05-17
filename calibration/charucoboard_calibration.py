from calibration.objp_imgp_utils import charuco_objp_imjp
import cv2 as cv
from calibration.analysis import select_analysis

def main():
    print('\n Please enter the following reqired parameters:\n')

    input_str = input("\n Enter frame size (width,height) in pixels: ") 
    x_str, y_str = input_str.strip().split(',')
    frame_size = (int(x_str), int(y_str))

    input_str = input("\n Enter charuco board size (total_row,total_col): ") 
    rows, cols= input_str.strip().split(',')  
    rows = int(rows.strip())
    cols = int(cols.strip())

    input_str = input("\n Enter the square_size in m: ") 
    square_length = float(input_str.strip()) 

    input_str = input("\n Enter the marker_size in m: ") 
    marker_length = float(input_str.strip())
 
    image_format_input = input("\n Enter the image format (e.g., 'png' or 'jpg'): ")  # e.g., " png "
    image_format = f"*.{image_format_input.strip()}"  # Converts " png " to "*.png", "*.png"
    
    aruco_dicts = {
    "DICT_4X4_50": cv.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv.aruco.DICT_ARUCO_ORIGINAL
}

    def get_user_selected_dictionary():
        print("Available Aruco Dictionaries:")
        for key in aruco_dicts.keys():
            print(f"- {key}")
        
        user_input = input("\nEnter the name of the Aruco dictionary you want to use: ").strip()
        
        if user_input in aruco_dicts:
            return aruco_dicts[user_input]
        else:
            print("Invalid dictionary name. Please try again.")
            return get_user_selected_dictionary()

    aruco_dict= get_user_selected_dictionary()

    print(f"\n The image format is: {image_format}")
    print(f"\n The charuco board size is: {rows,cols}")
    print(f"\n The square size of charuco board is: {square_length} m")
    print(f"\n The marker size of charuco board is: {marker_length} m")
    print(f"\n The frame size is: {frame_size}\n")  

    # Call the function to get object points and image points
    objpoints, imgpoints,ids_all,charuco_board, images = charuco_objp_imjp(cols,rows,square_length,marker_length,aruco_dict,image_format)

    ret, cameraMatrix, dist, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(
        charucoCorners=imgpoints,
        charucoIds=ids_all,
        board=charuco_board,
        imageSize=frame_size,
        cameraMatrix=None,
        distCoeffs=None)

    print("Camera Calibrated: ", ret)
    print("\n Camera Matrix: \n", cameraMatrix)
    print("\n Distortion parameters\n", dist)
    print("\n Rotation Vectors: \n", rvecs)
    print("\n Translation Vectors: \n", tvecs)
    print("\nWriting camera_matrix and distortion_coeffs to .yml file...\n")

    cv.FileStorage("camera_matrix.yml", cv.FILE_STORAGE_WRITE).write("camera_matrix", cameraMatrix)
    cv.FileStorage("distortion_coeffs.yml", cv.FILE_STORAGE_WRITE).write("distortion_coefficients", dist)

    # Ask the user if they want to perform further analysis
    perform_analysis = input("\nDo you want to perform further analysis? (y/n): ").strip().lower()

    if perform_analysis == 'y':
        # Call the analysis function
        # Replace with actual object points for visualization
        select_analysis(objpoints, imgpoints, rvecs, tvecs, cameraMatrix, dist, images)
    elif perform_analysis == 'n':
        print("Analysis skipped.")
    else:
        print("Invalid input. Skipping analysis.")

if __name__ == "__main__":
    main()