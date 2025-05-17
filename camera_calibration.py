from  calibration import checkerboard_calibration,asymmetric_circles_calibration,charucoboard_calibration

def main():
    print("Select the type of calibration:")
    print("1. Checkerboard Calibration")
    print("2. Asymmetric Circles Board Calibration")
    print("3. Charuco Board Calibration")
    print("4. Exit")
    choice = input("Enter your choice (Number): ")

    if choice == '1':
        print("Running Checkerboard Calibration...")
        checkerboard_calibration.main()  # Call the main function of the checkerboard calibration script
    elif choice == '2':
        asymmetric_circles_calibration.main()
    elif choice == '3':
        charucoboard_calibration.main()
    elif choice == '4':
        print("Exiting...")
    else:
        print("Invalid choice. Please select between 1 and 4.")

if __name__ == "__main__":
    main()