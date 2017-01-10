from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import time
import argparse
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
    time.sleep(5)
    #driver.save_screenshot("out.png")

def login_google(driver, args):
    login_name = input("Enter your username: ")
    login_pass = getpass.getpass("Enter your password: ")
    driver.get(HACKERRANK_LOGIN_URL)
    driver.save_screenshot("out1.png")
    driver.find_element_by_xpath("//a[@data-analytics='SignupGoogle' and @data-attr2='Login']").click()
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = driver.current_window_handle
    signin_window_handle = None
    while not signin_window_handle:
        for handle in driver.window_handles:
            if handle != main_window_handle:
                signin_window_handle = handle
                break
    driver.switch_to.window(signin_window_handle)
    driver.find_element_by_id("Email").send_keys(login_name)
    driver.find_element_by_id("next").click()
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='Passwd']").send_keys(login_pass)
    driver.find_element_by_id("signIn").click()
    driver.switch_to.window(main_window_handle)
    scrape_hackerrank(driver, args)

def scrape_hackerrank(driver, args):
    if not args.fileinput:
        while True:
            url = input("Enter the problem url to scrape (type stop to stop): ")
            filename = input("Enter the file name you want to use: ")
            if url == "stop":
                break
            output_file(filename, get_problem_hackerrank(driver, url))
    else:
        f = open("input.file", "r")
        for line in f:
            try:
                l = line.split(" > ", 1)
                l[1] = l[1].rstrip("\r\n") # get rid of pesky newlines
                output_file(l[1], get_problem_hackerrank(driver, l[0]))
            except IndexError:
                print("Error: Incorrect input file formatting--check if input.file is correct.")
        f.close()
    #driver.save_screenshot("out1.png")

def get_problem_hackerrank(driver, url):
    driver.get(url)
    time.sleep(5)
    #driver.save_screenshot("out2.png")
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
    f = open(filename, "w")
    f.write(code)
    f.close()

parser = argparse.ArgumentParser(description="Save some submissions from "
                                 "HackerRank.")
parser.add_argument("-g", "--google", action="store_true", help="use google "
                    "account for login (default is username/password login)")
parser.add_argument("-f", "--fileinput", action="store_true", help="read from"
                    " input.file (see README.md)")
args = parser.parse_args()
driver = webdriver.PhantomJS()
if not args.google:
    login_hackerrank(driver)
    scrape_hackerrank(driver, args)
else:
    login_google(driver, args)

