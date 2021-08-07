#!/usr/bin/env python
# coding=utf-8

from requests import Session
from requests.adapters import HTTPAdapter

from my_proxy.io_proxy import proxy_out, cold_proxy_out
from my_proxy.util_proxy import proxy_false
from util import cfg

UserAgent_List = [
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",

    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",

    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",

    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",

    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51",

    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
]

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-Encoding': 'gzip, deflate, br',
    'accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'no-cache',
    # 'Connection': 'keep-alive',
    'cookie': 'sb=W2sKYdn3R81XJbvtr7JW3Bw5; datr=W2sKYakT_MTAVexu2_Gg-xyF; locale=zh_CN; wd=1490x799; c_user=100005381614728; spin=r.1004209596_b.trunk_t.1628169793_s.1_v.2_; xs=39:fpqmh5ToiKrt0A:2:1628077194:-1:6774::AcXJmdkvPJtaa8Z6bHb69zxvI8EBMWmg4ZXWGzIJrw; fr=1IEbuTrfVO4nWx39I.AWW6sQZVO4enxPl0_i8GxVyC7iA.BhDAMV.Zf.AAA.0.0.BhDAMV.AWUApRI8Ypg',
    'dnt': '1',
    'pragma': 'no-cache',
    'user-agent': 'facebookexternalhit/1.1'
    # 'user-agent': random.choice(UserAgent_List)
}


class MySession(Session):
    """
    通过继承Session，来进行自定义的Session
    """

    def __init__(self):
        super().__init__()
        self.mount('http://', HTTPAdapter(max_retries=3))  # 重写父类，增加重连次数
        self.mount('https://', HTTPAdapter(max_retries=3))
        # 数据由冷备份 到 热更新的代理池
        # 每请求一次就应该刷新一次代理池（防止代理池枯竭，应该不断地验证 添加代理到代理池）
        # 当使用代理失败后，应该向代理模块反馈代理信息
        cold_proxy_out()


# 继承request，在request基础上进行二次开发
# request是一个库，不是类，无法继承
class MyRequest(object):

    def __init__(self, session, url, *proxy_flag):
        super().__init__()
        self.session = session
        self.url = url
        self.header = header
        self.proxy_flag = proxy_flag
        if self.proxy_flag:
            self.proxy = proxy_out()

    def get(self):
        """
        没有将url移到本函数中，是为了更好捆绑url与proxy。方便追踪修改proxy
        # get是一个动作，这个动作的值是response。外面需要接受到response，就需要return get
        @return:
        """
        response = None
        try:
            if self.proxy_flag:
                response = self.session.get(self.url, headers=self.header, timeout=cfg.TIMEOUT, allow_redirects=False, proxies=self.proxy)
            else:
                response = self.session.get(self.url, headers=self.header, timeout=cfg.TIMEOUT, allow_redirects=False)
        except Exception as e:
            print("链接请求异常：%s" % self.url)

        # 将代理进行反馈，单独and response 是为了提前判断是否None，避免后面取status code出错
        if self.proxy_flag and (not response or response.status_code != 200):
            print("触发了代理反馈！")
            proxy_false(self.proxy)

        return response
