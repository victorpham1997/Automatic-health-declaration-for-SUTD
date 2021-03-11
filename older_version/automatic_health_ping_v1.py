# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 2021
Last edit on Sat Feb 20 2021
version 1

@author: T.Vic
note:	this script will ping the tty site with the given session_id, make sure it is run periodically to make sure the cookies is not expired.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time

session_id = "f55ybszozzanjbnnk2oqfaej"

chrome_options = Options()
# You comment the next 3 lines to debug if there is any issue
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome("/home/victorpham1997/Documents/chromedriver")

driver.get("https://tts.sutd.edu.sg/tt_daily_dec_user.aspx")
driver.delete_cookie("ASP.NET_SessionId")
driver.add_cookie({'name':"ASP.NET_SessionId", 
	"value" : session_id,
	"domain": "tts.sutd.edu.sg",
	"path": "/"
	})


driver.get("https://tts.sutd.edu.sg/tt_home_user.aspx")
time.sleep(5)
driver.quit()