# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:22:00 2020
version 1.0

@author: Pham Trung Viet
note:	Require user to setup the following environment variables
		userid --> your SUTD user id (e.g 100xxxx)
		pw     --> your SUTD password

		Remeber to setup your selenium browser driver too! 
"""

from selenium import webdriver
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
        
        # Path to your selenium browser driver here
        self.driver = webdriver.Chrome(r"C:\Users\Pham Trung Viet\Documents\chromedriver")
        
    
    def main(self):
        self.driver.get(self.sutd_declaration_url)
        if self.login() != self.login_page_url:
            print("login failed")
            exit()
            
        self.tempTaking()
        self.alertHandling()
        self.dailyDeclaration()
        self.alertHandling()
        self.driver.quit()
            
    def login(self):
        userID = self.driver.find_element_by_name(self.userID_elem_name)
        pw = self.driver.find_element_by_name(self.pw_elem_name)
        
        userID.clear()
        userID.send_keys(os.environ["userid"])
        pw.clear()
        pw.send_keys(os.environ["pw"])
        pw.send_keys(Keys.RETURN)
        time.sleep(1)
        return self.driver.current_url
    
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
    