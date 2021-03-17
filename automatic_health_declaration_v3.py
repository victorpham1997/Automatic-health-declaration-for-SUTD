# -*- coding: utf-8 -*-
"""
Created on 11/03/2021
Last edit on 11/03/2021
version 3

@author: T.Vic
note:	
This version can bypass the captcha by utilising cv2 filters, BFS and pytesseract OCR. The script will attempt to make a number of attempts to inference the captcha and log in with the provided username and password. The number of try depends on your luck, the average number of try I got is usually around 10. 

Chrome driver will be automatically downloaded

For SUTD account username and password, you can either hardcode inside the script or parse it as arguments to the script. Please ensure they are correct!

Telegram me @Vhektor if you have any question regards to the script!

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import argparse
import os
import time
import datetime
import cv2
import sys
import os
import numpy as np
import pytesseract
from PIL import Image
from matplotlib import cm
from webdriver_manager.chrome import ChromeDriverManager

class autoHealthDeclaration:
    def __init__ (self, args):
        if sys.platform == "win32":
            pytesseract.pytesseract.tesseract_cmd = args.tesseractpath

        self.abs_path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
        self.log_path = os.path.abspath(self.abs_path + "auto_health_log.txt")

        self.sutd_declaration_url = "https://tts.sutd.edu.sg/tt_login.aspx?formmode=expire"
        self.userID_elem_name = "ctl00$pgContent1$uiLoginid" 
        self.pw_elem_name =  "ctl00$pgContent1$uiPassword"
        self.captcha_field_name = "ctl00$pgContent1$txtVerificationCode"
        self.login_submit_btn_name = "ctl00$pgContent1$btnLogin"
        self.captcha_image_id = "pgContent1_Image2"

        self.login_page_url = "https://tts.sutd.edu.sg/tt_home_user.aspx"

        self.daily_declaration_url = "https://tts.sutd.edu.sg/tt_daily_dec_user.aspx"
        self.temperature_taking_url = "https://tts.sutd.edu.sg/tt_temperature_taking_user.aspx"
        
        chrome_options = Options()
        # You comment the next 3 lines to debug if there is any issue
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')

        chorme_driver_path = ChromeDriverManager().install()

        # Use the driver on the line below to prevent the script from creating a chrome window whenever the script run
        if args.sandbox:
            self.driver = webdriver.Chrome(chorme_driver_path)
        else:
            self.driver = webdriver.Chrome(chorme_driver_path, chrome_options=chrome_options)

        #------------------------------ Hardcode your username and pw here!!------------------------------------------
        self.userid = ""
        self.userpw = ""
        #--------------------------Else you have to manually pass it as arguement-------------------------------------
        if args.username != "":
            self.userid = args.username
        if args.pw != "":
            self.userpw = args.pw
        self.login = False
        self.captcha = ""

        self.filter_threshold = 195


    def main(self):
        #if condition returns False, AssertionError is raised:
        assert self.userid != "" and self.userpw != "", "Username and/or password cannot be empty, either provide it in the arguments or hardcode it in the script!"

        # This while loop is to keep trying to login, the average number of try is around 10
        i = 1
        while not self.login:
            self.driver.get(self.sutd_declaration_url)
            captcha = self.driver.find_element_by_id(self.captcha_image_id)
            captcha.screenshot(self.abs_path+"temp.png")
            img  = cv2.imread(self.abs_path+"temp.png")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img[3:,3:]

            self.captcha = self.bypassCaptcha(img).strip()
            # self.captcha = input("Enter captcha:")
            print(f"\ncaptcha is: {self.captcha}")
            # time.sleep()
            if self.captcha.isalnum() and (len(self.captcha)==4 or len(self.captcha)==5):
                current_url = self.Login()
                print(current_url)
                if current_url == self.login_page_url:
                    print(f"Login succeeded after {i} tries!\nMoving on to next step!")
                    try:
                        f = open(self.log_path, "a")
                        f.write(f"{datetime.datetime.now()}    Succeeded after {i} tries\n")
                        f.close()
                    except:
                        print(f"Cannot write to log file at {self.log_path}, please check if your path is valid")
                    self.login = True
                else:
                    print(f"Inferenced captcha {self.captcha} is incorrect, retrying for the {i} time...")
            else:
                print(f"Inferenced captcha {self.captcha} does not match the required condition, retrying for the {i} time...")
            i+=1
            if i > 100:
                print("Loop timeout, please check your username and password and make sure it is correct before trying again (or you are just very very very unlucky :(")
                try:
                    f = open(self.log_path, "a")
                    f.write(f"{datetime.datetime.now()}    Failed\n")
                    f.close()
                except:
                    print(f"Cannot write to log file at {self.log_path}, please check if your path is valid")
                exit()


        self.tempTaking()
        self.alertHandling()
        self.dailyDeclaration()
        self.alertHandling()
        print("All processes is completed! Exiting...")
        self.driver.quit()

    def Login(self):
        userID = self.driver.find_element_by_name(self.userID_elem_name)
        pw = self.driver.find_element_by_name(self.pw_elem_name)
        captcha_field = self.driver.find_element_by_name(self.captcha_field_name)
        submit_btn = self.driver.find_element_by_name(self.login_submit_btn_name)

        userID.clear()
        userID.send_keys(self.userid)
        pw.clear()
        pw.send_keys(self.userpw)
        captcha_field.clear()
        captcha_field.send_keys(self.captcha)
        # pw.send_keys(Keys.RETURN)
        submit_btn.click()

        time.sleep(1)
        return self.driver.current_url

    def bypassCaptcha(self, img):
        c_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        out = cv2.medianBlur(c_gray,3)

        a = np.where(out>self.filter_threshold, 1, out)
        out = np.where(a!=1, 0, a)

        out = self.removeIsland(out, 30)

        out = cv2.medianBlur(out,3)

        # plt.imshow(out,cmap='gray')

        im = Image.fromarray(out*255)
        out_captcha = pytesseract.image_to_string(im)
        # print(out_captcha)
        return out_captcha

    def bfs(self, visited, queue, array, node):
        # I make BFS itterative instead of recursive to accomodate my WINDOWS friends >:]
        def getNeighboor(array, node):
            neighboors = []
            if node[0]+1<array.shape[0]:
                if array[node[0]+1,node[1]] == 0:
                    neighboors.append((node[0]+1,node[1]))
            if node[0]-1>0:
                if array[node[0]-1,node[1]] == 0:
                    neighboors.append((node[0]-1,node[1]))
            if node[1]+1<array.shape[1]:
                if array[node[0],node[1]+1] == 0:
                    neighboors.append((node[0],node[1]+1))
            if node[0]-1>0:
                if array[node[0],node[1]-1] == 0:
                    neighboors.append((node[0],node[1]-1))
            return neighboors

        queue.append(node)
        visited.add(node)

        while queue:
            current_node = queue.pop(0)
            for neighboor in getNeighboor(array, current_node):
                if neighboor not in visited:
        #             print(neighboor)
                    visited.add(neighboor)
                    queue.append(neighboor)
            
    def removeIsland(self, img_arr, threshold):
        while 0 in img_arr:
            x,y = np.where(img_arr == 0)
            point = (x[0],y[0])

            visited = set()
            queue = []

            self.bfs(visited, queue, img_arr, point)

            if len(visited) <= threshold:
                for i in visited:
                    img_arr[i[0],i[1]] = 1
            else:
                for i in visited:
                    img_arr[i[0],i[1]] = 2

        img_arr = np.where(img_arr==2, 0, img_arr)
        return img_arr


    def tempTaking(self):
        self.driver.get(self.temperature_taking_url)
        self.driver.find_element_by_xpath("//select[@name='ctl00$pgContent1$uiTemperature']/option[text()='Less than or equal to 37.6°C']").click()

        submit_btn = self.driver.find_element_by_xpath(".//form//input[@type='submit']")
        submit_btn.click()
        
    
    def dailyDeclaration(self):
        time.sleep(1)
        self.driver.get(self.daily_declaration_url)
        buttons = self.driver.find_elements_by_xpath(".//form//input[@type='radio']")
        self.box_clicked = 0
        
        def check_box():
            self.box_clicked = 0
            for i in range(len(buttons)):
                btn_ls = self.driver.find_elements_by_xpath(".//form//input[@type='radio']")
                # print(len(btn_ls))
                if (btn_ls[i].get_attribute("value").endswith("No")):
                    btn_ls[i].click()
                    self.box_clicked += 1
            
        while(self.box_clicked < 4):
            try:
                check_box()
            except:
                print("Error occured, trying again.")
                
        submit_btn = self.driver.find_element_by_xpath(".//form//input[@type='submit']")
        submit_btn.click()

    def alertHandling(self):
        alert = self.driver.switch_to.alert
        alert.accept()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is automatic_health_declaration version 3, it can bypass captcha and help you log your temperature and health check automatically. Username and pw can be hardcoded in the script or passed as arguments!')
    parser.add_argument('-s', '--sandbox', type=bool, nargs='?', const=True, default=False , help='Will open chrome window if flag is set')
    parser.add_argument('-u', '--username', type=str, default="" , help='Input your username here or ignore it and hardcode in the script')
    parser.add_argument('-p', '--pw', type=str, default="" , help='Input your password here or ignore it and hardcode in the script')
    parser.add_argument('-tp', '--tesseractpath', type=str, default=r'C:\Program Files\Tesseract-OCR\tesseract.exe' , help='Manually set the path to Tesseract on your system. Only for Windows')

    args = parser.parse_args()
    ahd = autoHealthDeclaration(args)
    ahd.main()
    exit(10)
    # print(os.path.realpath(__file__)[-len(os.path.basename(__file__)):])
    # print(os.path.realpath(__file__)[:-len(os.path.basename(__file__))])
