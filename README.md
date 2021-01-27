# Spider_MovieHome
spider for www.dy1234.net

## 爬虫需要针对该网站的一些必要配置
### 域名
### RequestModel.Request Headers




## 问题所在
多线程操作的队列，无法获得准确的队列准确的元素个数

个人猜想：让每个线程进入队列的时候，报告自己当前的index号。而不是，用一个外部线程来监听，这是不准确的。