# -*- coding: utf-8 -*-
"""
@author: 冰蓝
@site: https://lanbing510.info
"""

import re
import urllib2  
import sqlite3
import random
import threading
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding("utf-8")



if __name__=="__main__":
    print "start..."
#    html = "<div class=\"positionInfo\"> <span class=\"positionIcon\"></span> <a href=\"https://bj.lianjia.com/xiaoqu/chaoyang/\" class=\"district\" title=\"朝阳小区\">朝阳</a>  &nbsp;<a href=\"https://bj.lianjia.com/xiaoqu/ganluyuan/\" class=\"bizcircle\" title=\"甘露园小区\">甘露园</a>&nbsp; /塔楼/板楼/塔板结合     /&nbsp;2001年建成 </div>"
    with open('test', 'r') as f:
        html = f.read()
        f.close()
#    print html
    info_list=[u'链接',u'小区名称',u'户型',u'面积',u'朝向',u'楼层',u'建造时间',u'签约时间',u'签约单价',u'签约总价',u'房产类型',u'学区',u'地铁']

    soup =  BeautifulSoup(html,"html.parser")
    cj_list=soup.find('ul',{'class':'listContent'})   
    cj_list=cj_list.findAll('li')
    cj = cj_list[0]
    info_dict={}
    cjtitle = cj.find('div',{'class':'title'})
    href=cjtitle.find('a')
    cjname = cjtitle.text.split(" ")
#    cjsize = re.sub("^[0-9]", "", cjname[2])
#    print cjsize
#    cjsize = int(cjsize)
#    print href.attrs['href']
#    print cjname
#    print cjsize
#    if not href:
#        continue
    info_dict.update({info_list[0]:href.attrs['href']})
    cjhouseInfo = cj.find('div',{'class':'houseInfo'})
    info_dict.update({info_list[1]:cjname[0]})
    info_dict.update({info_list[2]:cjname[1]})
    info_dict.update({info_list[3]:cjname[2]})

    print cjhouseInfo.text
    cjhouseInfoDetails = cjhouseInfo.text.replace(" ","").split("|")
    print cjhouseInfoDetails
    info_dict.update({info_list[4]:cjhouseInfoDetails[0]})

    cjpositionInfo = cj.find('div',{'class':'positionInfo'})
    print cjpositionInfo.text
    cjpositionInfo = cjpositionInfo.text.split(" ")
    info_dict.update({info_list[5]:cjpositionInfo[0]})
    info_dict.update({info_list[6]:cjpositionInfo[1]})

    cjdealDate = cj.find('div',{'class':'dealDate'})
    info_dict.update({info_list[7]:cjhouseInfo.text})
    print cjdealDate.text
    cjunitPrice = cj.find('div',{'class':'unitPrice'})
    cjunitPriceNum = re.sub("[^0-9]", "", cjunitPrice.text)
    cjunitPriceNum = int(cjunitPriceNum)
    print cjunitPrice.text
    info_dict.update({info_list[8]:cjunitPrice.text})
    cjtotalPrice = cj.find('div',{'class':'totalPrice'})
    cjtotalPriceNum = re.sub("[^0-9]", "", cjtotalPrice.text)
    cjtotalPriceNum = int(cjtotalPriceNum)
    print cjtotalPriceNum
    info_dict.update({info_list[9]:cjtotalPrice.text})
    print cjtotalPrice.text

    cjdealCycleeInfo = cj.find('div',{'class':'dealCycleeInfo'})
    cjdealCycleeInfo = cjdealCycleeInfo.find('span',{'class':'dealCycleTxt'})
    cjdealCycleeInfo = cjdealCycleeInfo.findAll('span')
    cjdealCycleeInfoOriginalPriceNum = re.sub("[^0-9]", "", cjdealCycleeInfo[0].text)
    cjdealCycleeInfoOriginalPriceNum = int(cjdealCycleeInfoOriginalPriceNum)
    cjdealCycleeInfoOriginalDayNum = re.sub("[^0-9]", "", cjdealCycleeInfo[1].text)
    cjdealCycleeInfoOriginalDayNum = int(cjdealCycleeInfoOriginalDayNum)
#    print cjdealCycleeInfo
    print cjdealCycleeInfoOriginalPriceNum
    print cjdealCycleeInfoOriginalDayNum
    info_dict.update({info_list[10]:cjtotalPrice.text})
    info_dict.update({info_list[11]:cjtotalPrice.text})
    info_dict.update({info_list[12]:cjtotalPrice.text})
    print info_dict

