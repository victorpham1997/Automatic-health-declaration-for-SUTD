# **Automatic health declaration script for SUTD**

This is an automated python script using selenium, cv2 and Pytesseract to automatically fill in the compulsory health declaration by SUTD.

The script has been tested on Linux(Ubuntu) and Windows 10

## Update

- Version 3 is out, it can **bypass the captcha** :) Due to the updated captcha system **only version 3 is working.**
- Tested v3 on both Linux and Windows 10

## Dependencies

1. Pip install the required module in the script by:

   ```
   pip install -r requirements.txt
   ```

2. **(For Window users only) ** Install Tesseract.exe:

   - Download the Tesseract installer from here https://github.com/UB-Mannheim/tesseract/wiki

   - Install it and take note at the path in which it was installed, by default it will be at 

     ``` bash
     C:\Program Files\Tesseract-OCR\
     ```

     If the path is different from above, you have to manually input the path using the argument tag `-tp` or` --tesseractpath` to pass as argument to the script.	


## Usage

1. Make sure the script itself can run manually first 

   - Open python IDE to test the script manually. 

   - Chrome webdriver will be downloaded automatically so no need to worry about that

   - For username and password, you have 2 options:

     1.  Hardcoding them inside the script: You can hardcode your username and password into the script in the highlighted section 

     2. Pass them as arguments: You can pass them as argument to the script by using `-u` and `-p` tag for username and password respectively. 
        For example: `python3 automatic_health_declaration_v3.py -u 1009999 -p helloworld`
        
        Please ensure username and password are correct!
     
   - Ensure `-s` or `--sandbox`  tag is set to be able to manually test the process
   
   - Run the script manually and make sure it works before automating it.
   
2. Output for ```python3 automatic_health_declaration_v3.py -h```

   ```
   usage: automatic_health_declaration_v3.py [-h] [-s [SANDBOX]] [-u USERNAME]
                                             [-p PW] [-tp TESSERACTPATH]
   
   This is automatic_health_declaration version 3, it can bypass captcha and
   help you log your temperature and health check automatically. Username and
   pw can be hardcoded in the script or passed as arguments!
   
   optional arguments:
     -h, --help            show this help message and exit
     -s [SANDBOX], --sandbox [SANDBOX]
                           Will open chrome window if flag is set
     -u USERNAME, --username USERNAME
                           Input your username here or ignore it and hardcode
                           in the script
     -p PW, --pw PW        Input your password here or ignore it and hardcode
                           in the script
     -tp TESSERACTPATH, --tesseractpath TESSERACTPATH
                           Manually set the path to Tesseract on your system.
                           Only for Windows
   ```

3. Automate it

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

