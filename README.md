# **Automatic health declaration script for SUTD**

This is an automated python script using selenium, cv2 and Pytesseract to automatically fill in the compulsory health declaration by SUTD.

## Update

- Version 3 is out, it can **bypass the captcha** :) Due to the updated captcha system **only version 3 is working.**

## Dependencies

1. Chrome webdriver: https://chromedriver.chromium.org/downloads (please download according to your **current chrome version**)

2. Pip install the required module in the script (check the script and pip install any module you are missing)


## Usage

1. Make sure the script itself can run manually first 

   - Open python IDE to test the script manually. 

   - Open the script and edit the path for the webdriver

   - For username and password, you can either hardcode inside the script or parse it as arguments to the script. -h tag is available for the script.

     ```bash
     python3 automatic_health_declaration_v3.py -h
     ```

     Please ensure username and pw are correct!

   - Ensure --sandbox tag is set to be able to manually test the process

   - Run the script manually and make sure it works before automating it.

2. Automate it

   a. For Window:

   - You can use the .bat file in the executable_file folder as the execution program, remember to edit the path to your python environment and python file respectively in your .bat file.
   - Use Window Task scheduler to run the bat file at the scheduled time

   b. For Linux:

   - You can use the .sh file in the executable_file folder as the execution program, remember to edit the path to your python environment  and file python respectively in your .sh file.
   - Use Startup Application to run it whenever you log in your machine. Or use crontab to schedule it.

Enjoy never having to worry about the school sending you reminder to fill in the temperature taking. 
## Credit

The chrome pw fetching was done with the help of this repo: https://github.com/priyankchheda/chrome_password_grabber

OCR engine was done by Pytesseract: https://github.com/madmaze/pytesseract

Image filter was done using OpenCV library: https://github.com/opencv/opencv-python