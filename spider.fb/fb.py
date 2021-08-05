"""
@Desc   : 用于Facebook的信息爬取
@Time   : 2021-08-04 18:35
@Author : tank boy
@File   : fb.py
@coding : utf-8
"""
import random
import time

# 透過selenium登入獲得cookies
import requests
from lxml import etree
from selenium import webdriver

from util.my_request import MySession, MyRequest
from util.request_util import UserAgent_List


def login():
    account = "626640968@qq.com"
    password = "qiupeng..6772000"
    # driver設定
    driver_location = 'C:\\Develop.Tool\\chromedriver.exe'
    driver = webdriver.Chrome(driver_location)

    # 登入動作
    driver.get('https://www.facebook.com/')
    input_1 = driver.find_element_by_css_selector('#email')
    input_2 = driver.find_element_by_css_selector("input[type='password']")

    input_1.send_keys(account)
    input_2.send_keys(password)
    driver.find_element_by_css_selector("button[name='login']").click()
    time.sleep(1)

    # 獲得登入cookies
    cookies = driver.get_cookies()

    driver.close()
    return cookies


def step_1(cookies):
    s = requests.Session()

    # 將cookies放入session中
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

        response = s.get('https://mbasic.facebook.com/search/places/?q=mattress+uk&source=filter&isTrending=0', headers={'user-agent': random.choice(UserAgent_List)}, proxies={
            'http': 'http://127.0.0.1:10809',
            'https': 'http://127.0.0.1:10809'
        }, allow_redirects=False)
    # print("%s" % response.text)
    print("%s" % response)


def init():
    s = MySession()
    response = MyRequest(s, 'https://mbasic.facebook.com/search/places/?q=mattress+uk&source=filter&isTrending=0', True).my_get()
    # print("%s" % response.text)
    # with open('C:/Users/Administrator/Desktop/fb.json', 'w') as f:
    #     print(response.text, file=f)
    #     f.close()
    print("%s" % response)
    selector = etree.HTML(response.text)
    store_link = selector.xpath("//a[@tabindex='0']/@href")
    print(store_link)


if __name__ == '__main__':
    c = login()
    step_1(c)
    # init()
