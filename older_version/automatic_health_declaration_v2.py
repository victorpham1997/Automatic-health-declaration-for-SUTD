# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 2021
Last edit on Sat Feb 20 2021
version 2

@author: T.Vic
note:	this script can automatic log health information provided active session id. It should go hand in hand with automatic_health_ping script
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time



class autoHealthDeclaration:
    def __init__ (self):
        self.sutd_declaration_url = "https://tts.sutd.edu.sg/tt_login.aspx?formmode=expire"
        self.userID_elem_name = "ctl00$pgContent1$uiLoginid" 
        self.pw_elem_name =  "ctl00$pgContent1$uiPassword"
        self.login_page_url = "https://tts.sutd.edu.sg/tt_home_user.aspx"
        
        self.daily_declaration_url = "https://tts.sutd.edu.sg/tt_daily_dec_user.aspx"
        self.temperature_taking_url = "https://tts.sutd.edu.sg/tt_temperature_taking_user.aspx"
        
        chrome_options = Options()
        # You comment the next 3 lines to debug if there is any issue
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # Path to your selenium browser driver here
        self.session_id = "f55ybszozzanjbnnk2oqfaej"
        # self.driver = webdriver.Chrome("/home/victorpham1997/Documents/chromedriver", chrome_options=chrome_options)
        self.driver = webdriver.Chrome("/path/to/Documents/chromedriver")
        # self.driver.add_cookie({'name':"ASP.NET_SessionId", 
        # 	"value" : self.session_id,
        # 	"domain": "tts.sutd.edu.sg",
        # 	"path": "/"
        # 	})


    def main(self):
        self.driver.get(self.sutd_declaration_url)
        self.driver.delete_cookie("ASP.NET_SessionId")
        self.driver.add_cookie({'name':"ASP.NET_SessionId", 
        	"value" : self.session_id,
        	"domain": "tts.sutd.edu.sg",
        	"path": "/"
        	})
        # if self.login() != self.login_page_url:
        #     print("login failed")
        #     exit()

        self.tempTaking()
        self.alertHandling()
        self.dailyDeclaration()
        self.alertHandling()
        self.driver.quit()


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
                print(len(btn_ls))
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
    ahd = autoHealthDeclaration()
    ahd.main()
    exit(10)
