from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import time
"""
Before using, make sure PhantomJS is in your PATH.
"""

HACKERRANK_LOGIN_URL = "https://www.hackerrank.com/login?h_r=community_home&h_v=log_in&h_l=header_right"

def login_hackerrank(driver):
    login_name = input("Enter your username: ")
    login_pass = getpass.getpass("Enter your password: ")

    driver.get(HACKERRANK_LOGIN_URL)
    driver.find_element_by_xpath("//input[@data-attr1='UserName']").send_keys(login_name)
    driver.find_element_by_xpath("//input[@data-attr1='UserName' and @id='password']").send_keys(login_pass)
    driver.find_element_by_xpath("//*[@id='legacy-login']/div[1]/p/button").click()
    #driver.save_screenshot("out.png")

def scrape_hackerrank(driver):
    login_hackerrank(driver)
    time.sleep(5)
    #driver.save_screenshot("out1.png")
    url = input("Enter the problem url to scrape: ")
    driver.get(url)
    time.sleep(5)
    driver.save_screenshot("out2.png")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    #codemirror_start = soup.find_all(class_="CodeMirror-code")
    code_lines = soup.find_all("pre")
    #print(codemirror_start)
    #for string in codemirror_start[0].strings:
    code = ""
    for line in code_lines:
        for string in line.strings:
            code = code + repr(string)
        code = code + "\n"
    return clean_hackerrank(code)
    #print(codemirror_start.contents)
    #print(soup.prettify())

def clean_hackerrank(code):
    code = code.replace("'", "")
    code = code.replace("\\u200b", "\n")
    code = code.replace("\\xa0", " ")
    return code

def output_file(filename, code):
    f = open(filename, 'w')
    f.write(code)

driver = webdriver.PhantomJS()
output_file("testerino.java", scrape_hackerrank(driver))

#driver.set_window_size(1024, 768)


