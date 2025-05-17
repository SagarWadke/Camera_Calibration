# Camera Calibration Using Checkerboard Pattern

_This file will explain the steps necessary to successfully peform camera calibration using `Checker board pattern`._

---
## Test Setup

* For this test I have used a LMK 6-5 Color Camera with a 25mm objective to capture the images.
* The image size is 2464 x 2035 pixels
* The Checker board pattern is printed on a regular A4 sheet paper using a laser printer using black toner.
* The Checker board pattern has 10 rows and 15 columns with checker size of 18mm.
* The pattern is stuck to a acrylite plate using masking tape, which firmly holds it to the position.

## Steps to follow after selection of ChArUco pattern for calibration

* You will be prompted to enter the various parameters necessary for calibration:

```
 Enter frame size (width,height) in pixels: 2464,2035

 Enter chessboard size (row,col): 9,14

 Enter the size of chessboard square in mm: 18

 Enter the image format (e.g., 'png' or 'jpg'): png
```
* Camera calibration would be performed and the result will be saved to camera_matrix and distortion_coeffs to .yml file

* Next there will be a prompt for further analysis.

* Give a appropriate file name and select the desired analysis.