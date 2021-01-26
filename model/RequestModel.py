#!/usr/bin/env python
# coding=utf-8
import random


class RequestModel(object):
    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"
    ]

    # 代理池？？
    Proxy_Pool = [
        'web-proxy.oa.com:8080',
        # '',
    ]

    # 获取不同的请求头
    @classmethod
    def getHeaders(cls):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache - Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.idyjy.com',
            'DNT': '1',
            'Pragma': 'no-cache',
            # 'Referer': 'http: //www.dytt8.net/html/gndy/dyzz/index.html',
            'Cookie': 'UM_distinctid=16dc0cffadc137-0831184c76eb09-67e1b3f-1fa400-16dc0cffadd1ea; safedog-flow-item=EDB5B438336D2E9A48D2FD085328122B; Hm_lvt_b12979e4e40bb5a6bba9824601810548=1580370178,1580472504,1580522352,1580539422; ASPSESSIONIDQQQSSCCR=KCHCEKNBKIMHNLJMKPGIBEFD; CNZZDATA1276470129=1619689626-1570892783-%7C1580546276; m=33367__%u7F8E%u5229%u575A%u5973%u58EB__http%3A//www.idyjy.com/sub/33367.html__%7C%7C32587__%u53F6%u95EE4%uFF1A%u5B8C%u7ED3%u7BC7__http%3A//www.idyjy.com/sub/32587.html__%7C%7C33362__%u8FDE%u73AF%u6740%u624B%u751F%u6D3B%u6307%u5357__http%3A//www.idyjy.com/sub/33362.html__%7C%7C26160__%u8FDD%u547D__http%3A//www.idyjy.com/sub/26160.html__%7C%7C23895__%u6D6E%u751F%u68A6__http%3A//www.idyjy.com/sub/23895.html__%7C%7C32530__%u71C3%u70E7%u5973%u5B50%u7684%u8096%u50CF__http%3A//www.idyjy.com/sub/32530.html__%7C%7C33222__1917__http%3A//www.idyjy.com/sub/33222.html__%7C%7C8931__%u9F99%u7EB9%u8EAB%u7684%u5973%u5B69__http%3A//www.idyjy.com/sub/8931.html__%7C%7C8626__%u8C1C%u4E00%u6837%u7684%u53CC%u773C__http%3A//www.idyjy.com/sub/8626.html__%7C%7C9503__%u6700%u4F73%u51FA%u4EF7__http%3A//www.idyjy.com/sub/9503.html__%7C%7C9857__%u767B%u5802%u5165%u5BA4__http%3A//www.idyjy.com/sub/9857.html__%7C%7C31068__%u54C8%u9A6C%u820D%u5C14%u5FB7%u60AC%u6848__http%3A//www.idyjy.com/sub/31068.html__; Hm_lpvt_b12979e4e40bb5a6bba9824601810548=1580547697',
            'User-Agent': random.choice(cls.UserAgent_List),
        }
        return headers

    # 获取代理
    @classmethod
    def getProxies(cls):
        proxies = {
            # 'http': random.choice(cls.Proxy_Pool),
            # 'http':'web-proxy.oa.com:8080',
            # 'https': random.choice(cls.Proxy_Pool)
        }
        return proxies
