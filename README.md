# CommonSpider

a template Spider for the most website

test changing project name for git

## 爬虫需要针对该网站的一些必要配置

### 域名

### RequestModel.Request Headers

## 问题所在

多线程操作的队列，无法获得准确的队列准确的元素个数

个人猜想：让每个线程进入队列的时候，报告自己当前的index号。而不是，用一个外部线程来监听，这是不准确的。


<p align="center">
<img src="https://s1.ax1x.com/2020/07/22/UbKCpq.png" alt="StreamerHelper" width="100px">
</p>

> 🍰 Never miss your Streamer again

[![MIT](https://img.shields.io/github/license/ZhangMingZhao1/StreamerHelper?color=red)](https://github.com/ZhangMingZhao1/StreamerHelper/blob/master/LICENSE)
[![npm version](https://img.shields.io/npm/v/npm)](https://github.com/ZhangMingZhao1/StreamerHelper/blob/master/package.json)
[![nodejs version](https://img.shields.io/npm/v/node?color=23&label=node&logoColor=white)](https://github.com/ZhangMingZhao1/StreamerHelper/blob/master/package.json)

## Introduction

主播直播助手，部署后，后台批量监测各个平台主播是否在线，并实时录制直播保存为视频文件，停播后投稿到b站。（关于版权问题，投稿的参数默认一律设置的转载，简介处默认放的有主播房间号）

## Installation

修改templates/info.json文件：
- personInfo为你的要上传的b站账号和密码，
- access_token 支持access_token验证,避免频繁登录造成出现验证码登录(已知bug:错误的token验证错误后无法触发登录的流程)
- streamerInfo为你要批量录制的主播，key为标题信息，value为包含主播直播地址和标签数组的对象。像移动端的直播地址，可进入APP点分享按钮，复制分享链接中的URL，如抖音的https://v.douyin.com/J2Nw8YM/
- tags为投稿标签，不能为空，总数量不能超过12个， 并且单个不能超过20个字，否则稿件投稿失败
- tid为投稿分区，详见表：[tid表](https://github.com/FortuneDayssss/BilibiliUploader/wiki/Bilibili%E5%88%86%E5%8C%BA%E5%88%97%E8%A1%A8)
- uploadLocalFile为是否投稿，填false表示仅下载，不上传，不填写该字段则默认上传
- deleteLocalFile为是否在投稿后删除本地文件，该选项仅在uploadLocalFile设置为true时启用，不填写该字段则默认删除

```json
{
  "personInfo": {
    "username": "",
    "password": ""
  },
  "streamerInfo": [
    {
      "iGNing直播第一视角": {
        "roomUrl": "https://www.huya.com/980312",
        "tid": 21,
        "uploadLocalFile": true,
        "deleteLocalFile": false,
        "tags": [
          "英雄联盟",
          "电子竞技",
          "iG"
        ]
      }
    },
    {
      "罗永浩抖音直播": {
        "roomUrl": "https://v.douyin.com/J2Nw8YM/",
        "tid": 21,
        "uploadLocalFile": true,
        "tags": [
          "网络红人",
          "罗老师"
        ]
      }
    }
  ]
}
```

#### Docker

配置文件: `/app/templates/info.json`

视频目录: `/app/download`

容器的保活使用docker提供的`restart`参数，不再使用PM2。

DNS参数可以根据地区以及实际情况进行配置。

```shell
docker run --name stream -itd -v /path/to/config/info.json:/app/templates/info.json -v /path/to/download/:/app/download --dns 114.114.114.114 --restart always zsnmwy/streamerhelper
```

#### 安装ffmpeg

mac:
```bash
brew update
brew install ffmpeg
```
linux:
```
sudo add-apt-repository ppa:djcj/hybrid
sudo apt-get update
sudo apt-get install ffmpeg
```

部署：
```bash
npm i -g pm2
git clone https://github.com/ZhangMingZhao1/StreamerHelper.git && cd StreamerHelper
npm i
npm run serve
```

## Environment

我们的机器在下面环境下完美运行:

阿里云轻量应用服务器，内存2g，CPU 1核，Ubuntu 18.04，同时检测两个主播。

| Node.js | npm | TypeScript|
| ---- | ---- | ---- |
| 12.18.2 | 6.14.5 |3.9.6 |



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


