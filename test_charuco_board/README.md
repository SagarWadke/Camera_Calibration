# Camera Calibration Using ChArUco Pattern

_This file will explain the steps necessary to successfully peform camera calibration using `ChArUco pattern`._

---
## Test Setup

* For this test I have used a LMK 6-5 Color Camera with a 25mm objective to capture the images
* The image size is 2464 x 2035 pixels
* The ChArUco pattern is printed on a regular A4 sheet paper using a laser printer using black toner.
* The ChArUco pattern has total 9 rows and 15 columns with quare size as 18 mm and marker size as 13 mm.
* The dictionary used is Aruco DICT 4X4
* The pattern is stuck to a acrylite plate using masking tape, which firmly holds it to the position.

## Steps to follow after selection of ChArUco pattern for calibration

* You will be prompted to enter the various parameters necessary for calibration:

```
 Enter frame size (width,height) in pixels: 2464,2035

 Enter charuco board size (total_row,total_col): 9,15

 Enter the square_size in m: 0.018

 Enter the marker_size in m: 0.013

 Enter the image format (e.g., 'png' or 'jpg'): png 
```
* Camera calibration would be performed and the result will be saved to camera_matrix and distortion_coeffs to .yml file

* Next there will be a prompt for further analysis.

* Give a appropriate file name and select the desired analysis.