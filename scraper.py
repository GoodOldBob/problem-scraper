from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import getpass
import time
"""
Before using, make sure the ChromeDriver executable is in your PATH.
"""

HACKERRANK_LOGIN_URL = "https://www.hackerrank.com/login?h_r=community_home&h_v=log_in&h_l=header_right"

def login_hackerrank(driver):
    login_name = input("Enter your username: ")
    login_pass = getpass.getpass("Enter your password: ")

    driver.get(HACKERRANK_LOGIN_URL)
    driver.find_element_by_xpath("//input[@data-attr1='UserName']").send_keys(login_name)
    #time.sleep(10)
    driver.find_element_by_xpath("//input[@data-attr1='UserName' and @id='password']").send_keys(login_pass)
    driver.find_element_by_xpath("//*[@id='legacy-login']/div[1]/p/button").click()
    driver.save_screenshot("out.png")


driver = webdriver.PhantomJS()
#driver.set_window_size(1024, 768)
login_hackerrank(driver)
url = input("Enter the problem url to scrape: ")
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")
print(soup.prettify())

"""
r = urllib.request.urlopen(url).read()
soup = BeautifulSoup(r)
print(soup.get_text())
"""
