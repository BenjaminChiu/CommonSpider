#!/usr/bin/env python
#coding=utf-8


#import sqlite3
import pymysql
import re

from movieHome.dytt8Moive import dytt_Lastest
from model.TaskQueue import TaskQueue
from thread.FloorWorkThread import FloorWorkThread
from thread.TopWorkThread import TopWorkThread
from utils.Utils import Utils

'''
    程序主入口
@Author monkey
@Date 2017-08-08
'''

# 截止到2017-08-08, 最新电影一共才有 164 个页面
#LASTEST_MOIVE_TOTAL_SUM = 6 #164

# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 6


def startSpider():
    # 实例化对象

    # 获取【最新电影】有多少个页面
    #在这里 我们为了测试时避免浪费过多的爬取时间，将最多电影页面写死
    LASTEST_MOIVE_TOTAL_SUM = dytt_Lastest.getMaxsize()
    print('【最新电影】一共  ' + str(LASTEST_MOIVE_TOTAL_SUM) + '  有个页面')
    dyttlastest = dytt_Lastest(LASTEST_MOIVE_TOTAL_SUM)
    floorlist = dyttlastest.getPageUrlList()

    floorQueue = TaskQueue.getFloorQueue()
    for item in floorlist:
        floorQueue.put(item, 3)

    # print(floorQueue.qsize())

    for i in range(THREAD_SUM):
        workthread = FloorWorkThread(floorQueue, i)
        workthread.start()

    while True:
        if TaskQueue.isFloorQueueEmpty():
            break
        else:
            pass

    for i in range(THREAD_SUM):
        workthread = TopWorkThread(TaskQueue.getMiddleQueue(), i)
        workthread.start()


    while True:
        if TaskQueue.isMiddleQueueEmpty():
            break
        else:
            pass

    insertData()


def insertData():
    # DBName = 'dytt.db'
    # db = sqlite3.connect('./' + DBName, 10)
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='fish_movie', port=3306, charset='utf8')

    #获取一个游标
    conn = db.cursor()

    #SelectSql = 'Select * from sqlite_master where type = "table" and name="lastest_moive";'

    SelectSql = 'select t.table_name from information_schema.TABLES t where t.TABLE_SCHEMA ="fish_movie" and t.TABLE_NAME ="moive_home";'

    DropTableSql = '''DROP TABLE IF EXISTS `moive_home`;'''


    CreateTableSql = '''
CREATE TABLE `moive_home`  (
  `m_id` bigint(64) NOT NULL AUTO_INCREMENT COMMENT '电影主键',
  `m_name` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '电影名称',
  `m_transName` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '译名',
  `m_desc` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '电影简介',
  `m_type` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '电影类型',
  `m_decade` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '电影出品年份',
  `m_conutry` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '产地（国家）',
  `m_IMDB_id` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT 'IMDB的电影ID',
  `m_douban_score` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '豆瓣分数',
  `m_director` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '导演',
  `m_actor` varchar(4096) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '演员',
  `m_placard` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '海报',
  `m_ftp_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT 'ftp地址（冗余）',
  `m_thunder_url` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '迅雷下载地址，字符串',
  `rcmd` tinyint(1) DEFAULT 0 COMMENT '首页是否推荐，1是，0非',
  `del` tinyint(1) DEFAULT 0 COMMENT '逻辑删除标志，1是，0非',
  PRIMARY KEY (`m_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
    '''

    InsertSql = '''
        INSERT INTO moive_home (m_name, m_transName, m_desc, m_type, m_decade, m_conutry, m_IMDB_id, m_douban_score, 
         m_director, m_actor, m_placard, m_ftp_url, m_thunder_url) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''


    #%s,%s,%s,%s,%s
    #?, ?, ?, ?, ?


    if (table_exists(conn, "moive_home") == 0):
        conn.execute(CreateTableSql)
        print("moive_home 创建成功！")
    else:
        conn.execute(DropTableSql)
        db.commit()
        conn.execute(CreateTableSql)
        print("moive_home，删除旧表并且创建了新表！")


    #初始化 叠加器
    count = 1

    while not TaskQueue.isContentQueueEmpty():
        item = TaskQueue.getContentQueue().get()
        conn.executemany(InsertSql, [Utils.dirToList(item),])
        db.commit()
        print('插入第 ' + str(count) + ' 条数据成功')
        count = count + 1

    # conn.executemany(InsertSql, [Utils.dirToList(temp), ])
    # db.commit()
    # # print('插入第 ' + str(count) + ' 条数据成功')




    print("当前的count:"+str(count))
    db.commit()
    db.close()





#这个函数用来判断表是否存在
def table_exists(conn,table_name):
    sql = "show tables;"
    conn.execute(sql)
    tables = [conn.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]

    # 存在返回1 不存在返回0
    if table_name in table_list:
        return 1
    else:
        return 0





#主函数 入口？什么几把原理？
if __name__ == '__main__':
    startSpider()