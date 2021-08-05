"""
@Desc   : 分体爬虫总是报重定向错误，尝试使用类中 集中爬
@Time   : 2021-08-05 21:53
@Author : tank boy
@File   : fb.1.py
@coding : utf-8
"""

import requests
import time
import random
import re
import pandas
import os
from selenium import webdriver
from bs4 import BeautifulSoup

from model.my_request import MySession


class CrawlFb:
    def __init__(self, account, password, driver_location):
        self.account = account
        self.password = password
        self.driver_location = driver_location
        self.cookies = []
        self.data = []

    # 透過selenium登入獲得cookies
    def login(self):
        # driver設定
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
    def crawl(self, url, number):
        # selenium登入
        self.login()

        # requests session
        s = MySession()

        # 將cookies放入session中
        for cookie in self.cookies:
            s.cookies.set(cookie['name'], cookie['value'])

        # headers
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        }

        p = 0
        len = int(number / 10)
        for tt in range(0, len):
            # 更改網址參數
            r_url = url + '&p=' + str(p)

            # 送出請求
            response = s.get('https://mbasic.facebook.com/search/places/?q=mattress+uk&source=filter&isTrending=0', headers=headers, proxies={
                'http': 'http://127.0.0.1:10809',
                'https': 'http://127.0.0.1:10809'
            })

            print("我带你们打!")
            print("%s" % response)
            print("%s" % response)
            print("%s" % response)

            # 獲得每則留言html id
            cmid = re.findall('id="\d{15,16}', response.text)
            cmid_list = []
            for i in cmid:
                ii = i.split('"')
                cmid_list.append(ii[1])

            # 分析留言內容
            soup = BeautifulSoup(response.text, 'html.parser')

            comments = []  # 根據 id存每則留言
            for id in cmid_list:
                comments.append(soup.find('div', id=id))

            for comment in comments:  # 分析留言內容
                name = comment.find('h3').text
                # print(name, end=' ')
                msgs = comment.select('div')
                msgs_s = ''
                for msg in msgs:
                    if not re.findall('讚 · 傳達心情', msg.text) and not re.findall('已回覆 · \d+ 則回覆', msg.text):
                        # print(msg.text)
                        msgs_s += msg.text
                dic = {}
                dic['name'] = name
                dic['msg'] = msgs_s
                self.data.append(dic)

            # 更新留言參數
            p += 10
            print('已爬取', p, '則留言')
            time.sleep(random.uniform(0.2, 1.2))

    # 輸出至目錄底下資料夾
    def to_csv(self, dir_name):
        out_dir = './' + dir_name
        out_name = '留言內容.csv'
        df = pandas.DataFrame(data=self.data)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        fullname = os.path.join(out_dir, out_name)
        df.to_csv(fullname, encoding='utf_8_sig', index=False)
        print('輸出至', dir_name, '資料夾')
        print('輸出完成')


if __name__ == '__main__':
    # 個人資料
    account = "626640968@qq.com"
    password = "qiupeng..6772000"
    driver_location = 'C:\\Develop.Tool\\chromedriver.exe'

    # 爬取目標 (要使用mbasic的網址)
    url = 'https://mbasic.facebook.com/story.php?story_fbid=583752185671245&id=326366841409782&__tn__=%2AW'

    # crawl
    crawlFB = Crawl_fb(account=account, password=password, driver_location=driver_location)
    crawlFB.crawl(url=url, number=100)
    crawlFB.to_csv(dir_name='data')
