# 抓qunaer数据并生成热力图
# 原帖：http://www.51testing.com/html/82/n-3721082.html
import re

from click._compat import raw_input
from lxml import etree
from numpy import place


def getlist():
    plasce = raw_input("请输入想要搜索的区域，类型（如北京，热门景点等）：")
    url = 'http://piao.qunar.com/ticket/list.htm?keyword='+ str(place) +'&region=&from=mpl_search_suggest&page={}'
    i = 1
    sightlist = []
    while i:
        page = getPage(url.format(i))
        selector = etree.HTML(page)
        print('正在抓取第' + str(i) + '页景点信息')
        i += 1
        information = selector.xpath('//div[@class="result=list"]/div')
        for inf in information: # 获取必要信息
            sight_name = inf.xpath('./div/div/h3/a/text()')[0]
            sight_level = inf.xpath('.//span[@class="level"]/text()')
            if len(sight_level):
                sight_level = sight_level[0].replace('景区', '')
            else:
                sight_level = 0
            sight_area = inf.xpath('.//span[@class="area"]/a/text()')[0]
            sight_hot = inf.xpath('.//span[@class="product_star_level"]//span/text()')[0].replace('热度 ', '')
            sight_add = inf.xpath('.//p[@class="address color999"]/span/text()')[0]
            sight_add = re.sub('地址： | (.*?) |\(.*?\)|, .*?$|\/.*?$','',str(sight_add))