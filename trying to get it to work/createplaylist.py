#!/usr/bin/env python2.7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

url = "https://open.spotify.com/browse/featured"
driver = webdriver.Firefox()
driver.get(url)
# find this -> btn btn-black btn--no-margin btn--full-width P7Qjj40AVoE8Igi7Ji05m _1xNlj_ScH8hEMWzrkRt1A
# login_button = driver.find_element_by_class_name("P7Qjj40AVoE8Igi7Ji05m _1xNlj_ScH8hEMWzrkRt1A")
# login_button.click()
username = "jareddyreson@csu.fullerton.edu"
password = "passwordcause"
ids = driver.find_elements_by_xpath('//*[@class]')
for ii in ids:
    #print ii.tag_name
    if(ii.text == "LOG IN"):
        ii.click()
ids2 = driver.find_element_by_xpath('//*[@class]')
for i in ids2:
    print(i.text)
