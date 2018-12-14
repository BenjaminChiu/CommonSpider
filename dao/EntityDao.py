import re

import pymysql

from model.Entity import Entity
from model.TaskQueue import TaskQueue


class EntityDao:
    # 确定数据库连接，并获取连接游标   #在实际使用中，用对象去访问 类中公有的静态属性CONN
    DB = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='fish_movie', port=3306,charset='utf8')
    CONN = DB.cursor()
    DBNAME = 'fish_movie'

    def __init__(self, tableName):
        self.__tableName = tableName



    # 这个函数用来判断表是否存在当前数据库
    def showAllTables(self):
        sql = "show tables;"
        self.CONN.execute(sql)
        tables = [self.CONN.fetchall()]
        return tables


    def selectSql(self):
        selectSql = 'select t.table_name from information_schema.TABLES t where t.TABLE_SCHEMA ="' + str(self.DBNAME) + '" and t.TABLE_NAME ="' + str(self.__tableName) + '";'
        self.CONN.execute(selectSql)


    def createTable(self):
        createTableSql = '''
        CREATE TABLE `''' + str(self.__tableName) + '''`  (
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
                  `thunder_url` longtext CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '迅雷下载地址，字符串',
                  `rcmd` tinyint(1) DEFAULT 0 COMMENT '首页是否推荐，1是，0非',
                  `click_num` bigint(64) DEFAULT 0 COMMENT '影片点击量',
                  `mold` tinyint(1) DEFAULT 1 COMMENT '影片类型',
                  `del` tinyint(1) DEFAULT 0 COMMENT '逻辑删除标志，1是，0非',
                  PRIMARY KEY (`id`) USING BTREE
                ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
            '''
        self.CONN.execute(createTableSql)
        self.DB.commit()


    def dropTable(self):
        dropTableSql = 'DROP TABLE IF EXISTS `' + str(self.__tableName) + '`;'
        self.CONN.execute(dropTableSql)
        self.DB.commit()


    # 单个插入
    def insertEntity(self):
        insertSql = '''
            INSERT INTO ''' + str(self.__tableName) + ''' (m_name, trans_name, alt_name, m_desc, m_type, decade, conutry, imdb_id, douban_score, 
             director, actor, placard, update_to, thunder_url) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        '''
        self.CONN.execute(insertSql)
        self.DB.commit()



    #批量插入
    def insertManyEntity(self, item):
        insertSql = '''
            INSERT INTO ''' + str(self.__tableName) + ''' (m_name, trans_name, alt_name, m_desc, m_type, decade, conutry, imdb_id, douban_score, 
             director, actor, placard, update_to, thunder_url) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        '''
        self.CONN.executemany(insertSql, [Entity.dirToList(item), ])
        self.DB.commit()


    def findModelByName(self, name, director):
        sql = 'SELECT m_name,thunder_url FROM '+str(self.__tableName)+' WHERE m_name =\''+str(name)+'\' AND director=\''+str(director)+'\''
        self.CONN.execute(sql)
        return self.CONN.fetchall()

    # 更新
    def updateModel(self, url, name, director):
        sql = 'UPDATE '+str(self.__tableName)+' SET thunder_url = \''+str(url)+'\' WHERE m_name = \''+str(name)+'\' AND director=\''+str(director)+'\''
        self.CONN.execute(sql)
        self.DB.commit()

