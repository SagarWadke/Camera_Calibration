from calibration.objp_imgp_utils import asy_cir_objp_imjp
import cv2 as cv
from calibration.analysis import select_analysis

def main():

    print('\n Please enter the following reqired parameters:\n')

    input_str = input("\n Enter frame size (width,height) in pixels: ")  # e.g., "640,480"
    x_str, y_str = input_str.strip().split(',')
    frame_size = (int(x_str), int(y_str))

    input_str = input("\n Enter Asymmetric circle board size (total_row,total_col): ") #e.g., ",14"
    rows, cols= input_str.strip().split(',')  # e.g., "9,14"
    rows = int(rows.strip())
    cols = int(cols.strip())

    input_str = input("\n Enter the diagonal spacing mm: ") 
    diagonal_spacing_mm = float(input_str.strip()) # e.g., 18.0

    image_format_input = input("\n Enter the image format (e.g., 'png' or 'jpg'): ")  # e.g., " png "
    image_format = f"*.{image_format_input.strip()}"  # Converts " png " to "*.png", "*.png"
    
    print(f"\n The image format is: {image_format}")
    print(f"\n The Asymmetric circle board size is: {rows},{cols}")
    print(f"\n The diagonal spacing is: {diagonal_spacing_mm} mm")
    print(f"\n The frame size is: {frame_size}\n")  

    # Call the function to get object points and image points
    objpoints, imgpoints, images = asy_cir_objp_imjp(cols,rows,diagonal_spacing_mm,image_format)

    ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frame_size, None, None)

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