from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import xlwt  # 电子表格操作模块

browser = webdriver.Chrome(r'C:\Users\guo\Desktop\renshe\chromedriver.exe')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

browser.get('https://网址/register/#/login?_k=ax56bx')
browser.find_element_by_xpath(
    '/html/body/div/div/div/div[2]/div/div[2]/div[1]/div[2]/form/div[3]/span[2]/input').send_keys('用户名')
browser.find_element_by_xpath(
    '/html/body/div/div/div/div[2]/div/div[2]/div[1]/div[2]/form/div[4]/span[2]/input').send_keys('，密码')
time.sleep(1)
browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[1]/div[2]/form/div[6]/button[1]').click()
time.sleep(1)


def getData():  # 获取数据函数
    datalist = []  # 总的数据列表
    for i in range(1, 65):
        url = 'https://网址/ApplyCollegeNew?page=' + str(i)
        page_text = requests.get(url=url, headers=headers, timeout=10).text
        # 实例化bs对象，加载页面源码
        soup = BeautifulSoup(page_text, 'lxml')
        # 数据解析，返回列表[]
        li_list = soup.select('#collegesLists > li')
        # 循环列表
        for li in li_list:
            data = []  # 定义列表，用于保存每一行的数据
            title = li.select('.collegeFeature >h3>a')[0].string
            data.append(title)
            detail = li.select('.collegeFeature')[0].text
            data.append(detail)
            datalist.append(data)  # 将每行列表添加到总列表

    return datalist


def saveData(datalist, savepath):
    print('save....')
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('大学列表', cell_overwrite_ok=True)
    col = ('学校名称', '其他说明')
    # 表头字段名的写入
    for i in range(0, len(col)):  # 元组是不可变的，len取长度
        sheet.write(0, i, col[i])  # 列名
    # 数据记录的写入
    for i in range(0, len(datalist)):  # 使用len(列表）获得长度
        data = datalist[i]
        for j in range(0, len(data)):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)
    print('save ok....')


if __name__ == "__main__":
    savepath = '大学数据.xls'
    datalist = getData()
    saveData(datalist, savepath)

