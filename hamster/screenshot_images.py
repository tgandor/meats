#!/usr/bin/env python

import sys
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

browser = Chrome()
browser.get(sys.argv[1])
time.sleep(5)

def shoot():
    for idx, el in enumerate(browser.find_elements(By.TAG_NAME, 'img')):
        print(f"{idx:04d}.jpg:", el.get_attribute('src'))
        el.screenshot(f"{idx:04d}.jpg")

shoot()

while input("Retry?"):
    shoot()
