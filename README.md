# Camera Calibration Using Open-CV
This project provides a Python-based camera calibration tool using OpenCV.

---

## Features of the project

- It supports camera calibration using three different patterns (Checker Board, Asymmetric Circles, Charuco Board)
- It allows user to estimate intrinsic parameters and distortion coefficients
- It allows user to also peform extended analysis (Reprojection error analysis, Extrinsic visualisation)
- Modular code structure for with reusable utility functions 
- High flexibility to use user defined board and pattern size
---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SagarWadke/Camera_Calibration.git
   cd Camera_Calibration

2. Save the images of the calibration board taken from your camera in the same directory where the camera_calibration.py file is located.

3. Run the camera_calibration.py

4. Select the calibration pattern you have used for your camera calibration.

4. The further steps are discussed in the individual test folders for each pattern

---

## Notes

- For calibration, the patterns can be printed online eg. calib.io
- Print the pattern using a high quality laser printer.
- Make sure to turn off scaling and print pattern to their actual size
- Glue/tape the pattern to a flat surface for better calibration
