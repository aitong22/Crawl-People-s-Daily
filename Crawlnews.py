
import requests
import bs4
import os
import datetime
import time

def fetchUrl(url):

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    r = requests.get(url,headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def getPageList(year, month, day):

    url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000renmrb_01.htm'
    html = fetchUrl(url)
    bsobj = bs4.BeautifulSoup(html,'html.parser')
    temp = bsobj.find('div', attrs = {'id': 'pageList'})
    if temp:
        pageList = temp.ul.find_all('div', attrs = {'class': 'right_title-name'})
    else:
        pageList = bsobj.find('div', attrs = {'class': 'swiper-container'}).find_all('div', attrs = {'class': 'swiper-slide'})
    linkList = []

    for page in pageList:
        link = page.a["href"]
        url = 'http://paper.people.com.cn/rmrb/html/'  + year + '-' + month + '/' + day + '/' + link
        linkList.append(url)

    return linkList
def getTitleList(year, month, day, pageUrl):

    html = fetchUrl(pageUrl)
    bsobj = bs4.BeautifulSoup(html,'html.parser')
    temp = bsobj.find('div', attrs = {'id': 'titleList'})
    if temp:
        titleList = temp.ul.find_all('li')
    else:
        titleList = bsobj.find('ul', attrs = {'class': 'news-list'}).find_all('li')
    linkList = []

    for title in titleList:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp["href"]
            if 'nw.D110000renmrb' in link:
                url = 'http://paper.people.com.cn/rmrb/html/'  + year + '-' + month + '/' + day + '/' + link
                linkList.append(url)
    return linkList

def getContent(html):

    bsobj = bs4.BeautifulSoup(html,'html.parser')

    # 获取文章 标题
    title = bsobj.h3.text + '\n' + bsobj.h1.text + '\n' + bsobj.h2.text + '\n'
    #print(title)

    # 获取文章 内容
    pList = bsobj.find('div', attrs = {'id': 'ozoom'}).find_all('p')
    content = ''
    for p in pList:
        content += p.text + '\n'
    #print(content)

    # 返回结果 标题+内容
    resp = title + content
    return resp

def saveFile(content, path, filename):
    '''
    功能：将文章内容 content 保存到本地文件中
    参数：要保存的内容，路径，文件名
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)

def download_rmrb(year, month, day, destdir):
    '''
    功能：爬取《人民日报》网站 某年 某月 某日 的新闻内容，并保存在 指定目录下
    参数：年，月，日，文件保存的根目录
    '''
    pageList = getPageList(year, month, day)
    for page in pageList:
        titleList = getTitleList(year, month, day, page)
        for url in titleList:

            # 获取新闻文章内容
            html = fetchUrl(url)
            content = getContent(html)
            # 生成保存的文件路径及文件名
            temp = url.split('_')[2].split('.')[0].split('-')
            pageNo = temp[1]
            titleNo = temp[0] if int(temp[0]) >= 10 else '0' + temp[0]
            path = destdir + '/' + year + month + day + '/'
            fileName = year + month + day + '-' + pageNo + '-' + titleNo + '.txt'

            # 保存文件
            saveFile(content, path, fileName)

def gen_dates(b_date, days):
    day = datetime.timedelta(days = 1)
    for i in range(days):
        yield b_date + day * i

def get_date_list(beginDate, endDate):
    """
    获取日期列表
    :param start: 开始日期
    :param end: 结束日期
    :return: 开始日期和结束日期之间的日期列表
    """

    start = datetime.datetime.strptime(beginDate, "%Y%m%d")
    end = datetime.datetime.strptime(endDate, "%Y%m%d")

    data = []
    for d in gen_dates(start, (end-start).days):
        data.append(d)
    return data
if __name__ == '__main__':
    '''
    主函数：程序入口
    '''
    # 输入起止日期，爬取之间的新闻
    beginDate = input('请输入开始日期:') # 日期格式20200101
    endDate = input('请输入结束日期:')
    data = get_date_list(beginDate, endDate)

    for d in data:
        year = str(d.year)
        month = str(d.month) if d.month >=10 else '0' + str(d.month)
        day = str(d.day) if d.day >=10 else '0' + str(d.day)
        destdir = "E:/date"

        download_rmrb(year, month, day, destdir)
        print("爬取完成：" + year + month + day)
#         time.sleep(3)




import os
rootdir = r'E:\date'
newfile = r'E:\date\合并后文档.txt'
paths = []


for root, dirs, files in os.walk(rootdir):
    for file in files:
        paths.append(os.path.join(root, file).encode('utf-8'))


f = open(newfile,'w',encoding='utf-8')

for i in paths:
    for line in open(i,encoding='utf-8'):
        f.writelines(line)
f.close()   # 保存并关闭新建的文件


import jieba
import csv




with open(file=r"E:\人民日报关键词\人民日报热词.txt",encoding='UTF-8') as f:
    nameList = f.read().split('\n')

with open(file=r"E:\date\合并后文档.txt",encoding='UTF-8') as f:
    txt = f.read()

for name in nameList:
    jieba.add_word(name)
Excel = open("E:/date/本月中国政要出现次数.csv", 'w', newline='')
writ = csv.writer(Excel)
writ.writerow(['名称', '出现次数'])
# 分词
txt = jieba.lcut(txt)

counts = {}
for item in txt:
    for name in nameList:
        if item == name:
            counts[name] = counts.get(name, 0) + 1

count = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
for item in count[:20]:
    print(item)
item = list(counts.items())
item.sort(key=lambda x: x[1], reverse=True)
for i in range(8):
    writ.writerow(item[i])  ，
print('统计结果输出成功')

