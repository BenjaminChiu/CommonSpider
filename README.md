

# CommonSpider

> 🍰 a template Spider for the most website

test changing project name for git

<p align="center">
<img src="https://s1.ax1x.com/2020/07/22/UbKCpq.png" alt="StreamerHelper" width="100px">
</p>

## 爬虫需要针对该网站的一些必要配置

### 域名

### RequestModel.Request Headers

## 问题所在

多线程操作的队列，无法获得准确的队列准确的元素个数

个人猜想：让每个线程进入队列的时候，报告自己当前的index号。而不是，用一个外部线程来监听，这是不准确的。






[![MIT](https://img.shields.io/github/license/ZhangMingZhao1/StreamerHelper?color=red)](https://github.com/ZhangMingZhao1/StreamerHelper/blob/master/LICENSE)
[![npm version](https://img.shields.io/npm/v/npm)](https://github.com/ZhangMingZhao1/StreamerHelper/blob/master/package.json)
[![nodejs version](https://img.shields.io/npm/v/node?color=23&label=node&logoColor=white)](https://github.com/ZhangMingZhao1/StreamerHelper/blob/master/package.json)

## Introduction

通用爬虫框架，为节省时间而生！

## Run

直接运行vmess_main.py等几个文件即可。
因为使用了通用的运行框架，每个.py文件适配一个网站


## TodoList

- [x] 支持斗鱼，虎牙，b站直播，afreeca，抖音直播，快手直播，西瓜直播，花椒直播，YY 直播，战旗直播，酷狗繁星，NOW 直播，CC 直播，企鹅电竞直播
- [x] 自动监测主播在线
- [x] 自动上传b站
- [x] 多p下载多p上传
- [x] 支持多个主播
- [x] tag可配置，对应在info.json的每个主播
- [x] 支持access_token验证，防验证码
- [ ] 支持twitch
- [ ] 支持docker部署
- [ ] 爬虫定时区间，节省服务器流量...
- [ ] 重启后同时检测本地是否有上传失败的视频文件，并上传。
- [ ] 增加一个独立脚本遍历download文件夹下的视频文件重新上传(重启上传的折中解决办法，还有解决第一次账号密码配置错误失败上传的问题)

## Special Thanks

Special Thanks [JetBrains](https://www.jetbrains.com/?from=real-url) offering free JetBrains Open Source license

[![JetBrains-logo](https://i.loli.net/2020/10/03/E4h5FZmSfnGIgap.png)](https://www.jetbrains.com/?from=real-url)