import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import csv

def reprojection_error(objpoints, imgpoints, rvecs, tvecs, cameraMatrix, dist,name, images):
    """
    This function calculates the reprojection error for each image.
    It uses the camera matrix, distortion coefficients, rotation vectors, and translation vectors.
    """
    errors = []
    
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        errors.append(error)

    # Writing the error to a csv file

    filename = (f"Reprojection_error_{name}.csv")

    #Open the file in write mode
    with open(filename,mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Image_Name","Reprojection_error"])

        for image, error in zip(images, errors):
            writer.writerow([image,error])

    print(f"Reprojection errors have been saved in {filename}")

    # Calculate the total mean error (optional)
    mean_error = np.mean(errors)
    print(f"Total mean reprojection error: {mean_error:.4f} pixels")

    # Plot reprojection error for each image
    plt.figure(figsize=(10, 5))
    plt.bar(range(1, len(errors) + 1), errors, color='blue')
    plt.xlabel('Image Index')
    plt.ylabel('Reprojection Error (pixels)')
    plt.title(f'Reprojection Error for Each Image_{name}')
    plt.savefig(f"Reprojection Error for Each Image_{name}.pdf",format="pdf")
    plt.grid(True)
    plt.show()

def visualize_extrinsic_parameters(rvecs, tvecs, objpoints, name):
    """
    This function visualizes the extrinsic parameters of the camera.
    It uses the rotation vectors and translation vectors to plot the camera position and orientation.
    """
    objpoints_array = np.array(objpoints)
    # Initialize the plot
    rotation_matrices = [cv.Rodrigues(rvec)[0] for rvec in rvecs]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot camera at origin
    ax.scatter(0, 0, 0, c='r', marker='o', label='Camera')

    for rmat, tvec in zip(rotation_matrices, tvecs):
        # Define the corners of the checkerboard in the checkerboard's coordinate system
        corners = objpoints_array.reshape(-1, 3)

        # Rotate and translate the corners to the camera coordinate system
        transformed_corners = rmat.dot(corners.T).T + tvec.T

        # Draw the plane (just the corners)
        ax.plot_trisurf(transformed_corners[:, 0], transformed_corners[:, 1], transformed_corners[:, 2], alpha=0.5)

    ax.view_init(elev=-60, azim=180) 
    ax.set_box_aspect([1,1,1])
    # Set the labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Display the plot
    plt.title(f'Visualize_Extrinsic_camera_parameters_{name}')
    plt.savefig(f"Visualize_Extrinsic_camera_parameters_{name}.pdf",format="pdf")
    plt.legend()
    plt.show()

def select_analysis(objpoints, imgpoints, rvecs, tvecs, cameraMatrix, dist, images):
    """
    Main function to allow the user to select the type of analysis.
    """
    name = input("\nPlease enter a name for the result file: ")

    print("\nSelect the type of analysis:")
    print("1. Reprojection Error Analysis")
    print("2. Visualize Extrinsic Parameters")
    print("3. Perform All")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        reprojection_error(objpoints, imgpoints, rvecs, tvecs, cameraMatrix, dist, name, images)
    elif choice == '2':
        visualize_extrinsic_parameters(rvecs, tvecs, objpoints, name)
    elif choice == '3':
        reprojection_error(objpoints, imgpoints, rvecs, tvecs, cameraMatrix, dist, name, images)
        visualize_extrinsic_parameters(rvecs, tvecs, objpoints, name)
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
