"""
@Desc   : 分体爬虫总是报重定向错误，尝试使用类中 集中爬
@Time   : 2021-08-05 21:53
@Author : tank boy
@File   : fb.py
@coding : utf-8
"""

import time
import random
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup

from util.my_request import MySession, MyRequest


class CrawlFb:
    def __init__(self, account, password, driver_location):
        self.account = account
        self.password = password
        self.driver_location = driver_location
        self.cookies = []

    # 透過selenium登入獲得cookies
    def login(self):
        # driver设定
        driver = webdriver.Chrome(self.driver_location)

        # 登入動作
        driver.get('https://www.facebook.com/')
        input_1 = driver.find_element_by_css_selector('#email')
        input_2 = driver.find_element_by_css_selector("input[type='password']")

        input_1.send_keys(self.account)
        input_2.send_keys(self.password)
        driver.find_element_by_css_selector("button[name='login']").click()
        time.sleep(1)

        # 獲得登入cookies
        cookies = driver.get_cookies()
        self.cookies = cookies
        driver.close()

    # 爬取內容
    def crawl(self, url_in):
        # selenium登入
        # self.login()

        # requests session
        s = MySession()

        # 將cookies放入session中
        # for cookie in self.cookies:
        #     s.cookies.set(cookie['name'], cookie['value'])

        count = 0
        # 送出請求
        while True:
            print("当前请求次数：%s" % count)
            print("当前链接为：%s" % url_in)
            response = MyRequest(s, url_in, True).get()
            print("%s" % response)

            if response.status_code == 302:
                url_in = response.headers['location']
                count = count + 1
            elif response.status_code == 200:
                break
        # response.encoding = 'br'
        # print("%s" % response.text)
        selector = etree.HTML(response.text)
        link = selector.xpath("//td[@class='t cd']/a/@href")
        print("% s" % link)


if __name__ == '__main__':
    # 個人資料
    account = "626640968@qq.com"
    password = "qiupeng..6772000"
    driver_location = 'C:\\Develop.Tool\\chromedriver.exe'

    # 爬取目標 (要使用mbasic的網址)
    # url = 'https://mbasic.facebook.com/search/places/?q=mattress+uk&source=filter&isTrending=0'
    url = 'https://mbasic.facebook.com/story.php?story_fbid=583752185671245&id=326366841409782&__tn__=%2AW'
    # url = 'https://www.facebook.com/The-Mattress-Man-North-West-UK-Ltd-381355255365257/'
    # crawl
    crawlFB = CrawlFb(account=account, password=password, driver_location=driver_location)
    crawlFB.crawl(url)
