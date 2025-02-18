"""
@Desc   : 对接阿里云的接口，查询是否空号
@Time   : 2024-12-23 15:45
@Author : tank boy
@File   : PhoneTest.py
@coding : utf-8
"""
import json
import urllib, sys, ssl, openpyxl
import pandas as pd
from openpyxl.reader.excel import load_workbook

excel_path = "C:\\Users\\Administrator\\Desktop\\Temp.xlsx"
The_excel = load_workbook(excel_path)
The_excel_active = The_excel.active

# 已经查询并获得结果的 电话及其相关信息
result_tel = []
# 用于存放单个电话与信息的容器
item_tel = []



# def write_excel(excel, excel_active, row, col, result):
#     excel_active.cell(row, col, result)
#     excel.save(excel_path)


def read_excel():
    df = pd.read_excel(excel_path, usecols=['Tel', 'Area', 'Channel', 'Result'])
    phone_array = []

    for single_array in df.values:
        print(single_array)
        phone_array.append(single_array[0])

    # print(phone_array)
    # 返回一个数组
    return phone_array


def get_request(mobile, p_index):
    host = 'https://mobileempty.shumaidata.com'
    path = '/mobileempty'
    method = 'GET'
    appcode = 'd1a3b58ab4ba4affa77f8c34d8612163'
    bodys = {}

    # 重新格式化座机
    if ("825" == str(mobile)[:3]):
        mobile = "0" + str(mobile)


    # 因为待查询的数据里有重复的电话号码，没有必要再一次去查询。
    # 请求前，先去已查询过的数组里，查找结果


    print(mobile)
    url = host + path + '?mobile=' + str(mobile)
    print(url)

    my_request = urllib.request.Request(url)
    my_request.add_header('Authorization', 'APPCODE ' + appcode)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    response = urllib.request.urlopen(my_request, context=ctx)
    pre_content = response.read().decode('utf-8')
    print(pre_content)
    print("当前任务进度：" + str(p_index+2) + "/4335")

    content = json.loads(pre_content)

    if content['code'] == 200:
        area = (content['data'])['area']
        channel = (content['data'])['channel']
        status = (content['data'])['status']
        if status == 0:
            status = '空号'
        elif status == 1:
            status = '实号'
        elif status == 2:
            status = '停机'
        elif status == 3:
            status = '查无此号'
        elif status == 4:
            status = '沉默号'
        elif status == 5:
            status = '风险号'

        # 1. 以备用来让后来的待查电话来 先查询

        # 2. 之间容器没有内容，再将结果存入一个数组保存起来
        item_tel = [str(mobile), area, channel, status]
        result_tel.append(item_tel)

        # 写入excel
        The_excel_active.cell(p_index+2, 13, area)
        The_excel_active.cell(p_index+2, 14, channel)
        The_excel_active.cell(p_index+2, 15, status)




    else:
        The_excel_active.cell(p_index + 2, 15, 'None')

    # 本质是每10个保存一次
    # 修改为在快要结束的时候，改为查询一个，保存一个
    # if p_index % 10 == 0:
    The_excel.save(excel_path)





if __name__ == '__main__':

    phone_array = read_excel()

    message = input("Input 'Y' for testing.\n")
    print(message)

    # for index in range(len(phone_array)):
    #     get_request(phone_array[index], index)
    #
    # The_excel.close()
