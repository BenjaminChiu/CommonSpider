"""
@Desc   : 对接阿里云的接口，查询是否空号
@Time   : 2024-12-23 15:45
@Author : tank boy
@File   : PhoneTest.py
@coding : utf-8
"""

import urllib, sys
import ssl


if __name__ == '__main__':
    host = 'https://mobileempty.shumaidata.com'
    path = '/mobileempty'
    method = 'GET'
    appcode = '你自己的AppCode'
    querys = 'mobile=mobile'
    bodys = {}
    url = host + path + '?' + querys

    request = urllib.request.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = urllib.urlopen(request, context=ctx)
    content = response.read()
    if (content):
        print(content)