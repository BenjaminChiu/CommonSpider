#!/usr/bin/env python
# coding=utf-8

from requests import Session
from requests.adapters import HTTPAdapter

import cfg
# request是一个库，不是类，无法继承
# 继承request，在request基础上进行二次开发
from model.request_util import get_proxies, header


class MySession(Session):

    def __init__(self):
        super().__init__()
        self.mount('http://', HTTPAdapter(max_retries=3))  # 重写父类，增加重连次数
        self.mount('https://', HTTPAdapter(max_retries=3))


class MyRequest(object):

    def __init__(self, session, url, *proxy_flag):
        super().__init__()
        self.session = session
        self.url = url
        self.header = header
        self.proxy_flag = proxy_flag
        if self.proxy_flag:
            self.proxy = get_proxies()

    def my_get(self):
        if self.proxy_flag:
            # get是一个动作，这个动作的值是response。外面需要接受到response，就需要return get
            return self.session.get(self.url, headers=self.header, timeout=cfg.TIMEOUT, proxies=self.proxy)
        else:
            return self.session.get(self.url, headers=self.header, timeout=cfg.TIMEOUT)
