import re

import pymysql

from model.Entity import Entity
from model.TaskQueue import TaskQueue


class EntityDao:

    NAME = ''

    def __init__(self, tableName):
        self.tableName = tableName
        NAME = tableName


    # 这个函数用来判断表是否存在
    def table_exists(self, conn, table_name):

        print("传入的tableName="+ str(table_name))

        sql = "show tables;"
        conn.execute(sql)
        tables = [conn.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]

        # 存在返回1 不存在返回0
        if table_name in table_list:
            return 1
        else:
            return 0



    def insertData(self):
        # DBName = 'dytt.db'
        # db = sqlite3.connect('./' + DBName, 10)
        db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='fish_movie', port=3306, charset='utf8')

        # 获取一个游标
        conn = db.cursor()



        # SelectSql = 'Select * from sqlite_master where type = "table" and name="lastest_moive";'

        SelectSql = 'select t.table_name from information_schema.TABLES t where t.TABLE_SCHEMA ="fish_movie" and t.TABLE_NAME ="'+ str(self.tableName) +'";'

        DropTableSql = 'DROP TABLE IF EXISTS `' + str(self.tableName) + '`;'

        CreateTableSql = '''
    CREATE TABLE `'''+ str(self.tableName) +'''`  (
                  `id` bigint(64) NOT NULL AUTO_INCREMENT COMMENT '电影主键',
              `m_name` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '电影名称',
              `trans_name` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '译名',
              `alt_name` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '又名，别名',
              `m_desc` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '电影简介',
              `m_type` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '电影类型',
              `decade` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '电影出品年份',
              `conutry` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '产地（国家）',
              `imdb_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT 'IMDB的电影ID',
              `douban_score` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '豆瓣分数',
              `director` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '导演',
              `actor` varchar(4096) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '演员',
              `placard` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '海报',
              `update_to` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '更新到多少集 或 已完结（电视剧专用）',
              `thunder_url` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '迅雷下载地址，字符串',
              `rcmd` tinyint(1) DEFAULT 0 COMMENT '首页是否推荐，1是，0非',
              `click_num` bigint(64) DEFAULT 0 COMMENT '影片点击量',
              `del` tinyint(1) DEFAULT 0 COMMENT '逻辑删除标志，1是，0非',
              PRIMARY KEY (`id`) USING BTREE
            ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
        '''

        InsertSql = '''
            INSERT INTO '''+ str(self.tableName) +''' (m_name, trans_name, alt_name, m_desc, m_type, decade, conutry, imdb_id, douban_score, 
             director, actor, placard, update_to, thunder_url) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        '''

        # %s,%s,%s,%s,%s
        # ?, ?, ?, ?, ?


        #----------------操作表-------可选-----开始---------------
        if (self.table_exists(conn, 'serial_home') == 0):
            conn.execute(CreateTableSql)
            print(str(self.tableName) + "创建成功！")
        else:
            conn.execute(DropTableSql)
            db.commit()
            conn.execute(CreateTableSql)
            print(str(self.tableName) + "删除旧表并且创建了新表！")
        db.commit()
        # ----------------操作表-------可选-----结束---------------


        # 初始化 叠加器
        count = 1

        while not TaskQueue.isContentQueueEmpty():
            item = TaskQueue.getContentQueue().get()
            conn.executemany(InsertSql, [Entity.dirToList(item), ])
            db.commit()
            print('插入第 ' + str(count) + ' 条数据成功')
            count = count + 1



        #----第二阶段测试使用-----开始---------
        # conn.executemany(InsertSql, [Entity.dirToList(temp), ])
        # db.commit()
        # print('插入第 ' + str(count) + ' 条数据成功')
        #----第二阶段测试使用-----结束--------



        print("当前的count:" + str(count))

        db.close()