import re

from dao.EntityDao import EntityDao
from model.TaskQueue import TaskQueue


class EntityService:

    def __init__(self, tableName):
        self.__tableName = tableName
        self.__entitydao = EntityDao(tableName)
        self.__firstRun = True

    # 关闭数据库连接
    def shutDownDB(self):
        self.__entitydao.DB.close()

    # 判断表是否存在业务
    def table_exists(self):
        tables = self.__entitydao.showAllTables()
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]

        # 存在返回True 不存在返回False
        if self.__tableName in table_list:
            return True
        else:
            return False

    # 操作表-------可选-----
    def doTable(self):
        if self.__firstRun:
            self.__firstRun = False
            if self.table_exists():
                self.__entitydao.dropTable()
                self.__entitydao.createTable()
                print("删除旧表成功！并且创建了新表！")
            else:
                self.__entitydao.createTable()
                print("新创建表成功！")

    # 添加到数据库业务
    def finalSpider(self):
        # 操作表
        # self.doTable()

        # 初始化 叠加器
        count = 1
        while not TaskQueue.isQueue_3Empty():
            item = TaskQueue.getQueue_3().get()
            # 去重添加（有相同的电影名和导演），如果相同，判断链接是否多于数据库中，是就更新
            # 导演字段可能为空的处理
            parm = ''
            if str(item['director']).strip():
                parm = item['director']

            dataList = self.__entitydao.findModelByName(item['mName'], parm)

            # 返回值为空 新电影 可以插入
            if not len(dataList):
                self.__entitydao.insertManyEntity(item)
                print('插入第 ' + str(count) + ' 条数据成功')
                count = count + 1
            else:
                urlInDB = dataList[0][1]
                urlInPage = item['thunderUrl']
                # 新爬到的链接更多，更新
                if len(urlInPage) > len(urlInDB):
                    self.__entitydao.updateModel(urlInPage, item['mName'], parm)
                    print("更新" + str(item['mName']) + "成功!")

        # --第二阶段--页面信息集合抓取测试使用-----开始---------
        # self.__entitydao.insertManyEntity(temp)
        # print("插入成功！")
        # ----第二阶段测试使用-----结束--------
