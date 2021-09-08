"""
@Desc   : 分体爬虫总是报重定向错误，尝试使用类中 集中爬
@Time   : 2021-08-05 21:53
@Author : tank boy
@File   : fb.py
@coding : utf-8
"""
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from util.my_request import MySession, MyRequest


class CrawlFb:
    def __init__(self, t_url, account, password, driver_location):
        self.t_url = t_url
        self.account = account
        self.password = password
        self.driver_location = driver_location
        self.session = MySession()
        self.store_info_url = []

    def my_run(self):
        # self.login()
        self.get_store_url()
        self.get_store_info()

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

        # 將cookies放入session中
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        driver.close()

    # 爬取內容
    def get_store_url(self):

        response = MyRequest(self.session, self.t_url, True).get()
        print("目标url请求状态：%s" % response)

        soup = BeautifulSoup(response.text, 'html.parser')
        td_s = soup.find_all('td', 's cc')  # td 的类型是一个集合(ResultSet)

        url_s = []
        for td in td_s:
            store_info_url = 'https://mbasic.facebook.com' + td.a['href'].split('/?')[0] + '/about'
            url_s.append(store_info_url)
        self.store_info_url = url_s

    def get_store_info(self):
        # email_re = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')

        tt = 'https://mbasic.facebook.com/The-Mattress-Man-North-West-UK-Ltd-381355255365257/about'

        store_s = []
        # 遍历每一个店铺的url
        for url in self.store_info_url:
            response = MyRequest(self.session, url, True).get()
            print("各个店铺info_url请求状态：%s" % response)
            soup = BeautifulSoup(response.text, 'html.parser')
            store_info = []

            img_phone = soup.find('img', src='https://static.xx.fbcdn.net/rsrc.php/v3/yj/r/zBXQrqqny9i.png')
            phone = ''
            if img_phone:
                phone = img_phone.parent.next_sibling.div.text

            img_email = soup.find('img', src='https://static.xx.fbcdn.net/rsrc.php/v3/yy/r/vKDzW_MdhyP.png')
            email = ''
            if img_email:
                email = img_email.parent.next_sibling.div.text

            img_website = soup.find('img', src='https://static.xx.fbcdn.net/rsrc.php/v3/yV/r/EaDvTjOwxIV.png')
            website = url
            if img_website:
                website = img_website.parent.next_sibling.div.text

            store_info.append(email)
            store_info.append(website)
            store_info.append(phone)

            print('%s' % phone)
            print('%s' % email)
            print('%s' % website)
            store_s.append(store_info)

        with open('C:/Users/Administrator/Desktop/store_s.json', 'w') as f:
            for store in store_s:
                write_flag = False

                if store[0] or store[1] or store[2]:
                    print(store[0] + ' ' * 3 + store[1] + ' ' * 3 + store[2], file=f)
                    write_flag = True

                if write_flag:
                    print('', file=f)
            f.close()
        print("共爬取到店铺数量：%s" % len(store_s))
        print("信息写入完毕")


if __name__ == '__main__':
    # 個人資料
    account = "626640968@qq.com"
    password = "qiupeng..6772000"
    driver_location = 'C:/Develop.Tool/chromedriver.exe'

    # 爬取目標 (要使用mbasic的網址)
    url = 'https://mbasic.facebook.com/search/places/?q=mattress+uk&source=filter&isTrending=0'
    # url = 'https://mbasic.facebook.com/story.php?story_fbid=583752185671245&id=326366841409782&__tn__=%2AW'
    # url = 'https://www.facebook.com/The-Mattress-Man-North-West-UK-Ltd-381355255365257/'

    crawlFB = CrawlFb(t_url=url, account=account, password=password, driver_location=driver_location)
    crawlFB.my_run()
