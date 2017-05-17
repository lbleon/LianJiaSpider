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

hds= {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Encoding':'identity',
	    'Accept-Language':'en-US,en;q=0.8',
	    'Connection':'keep-alive',
        'Cookie':'select_city=110000; select_nation=1; lianjia_uuid=00fc8dbf-e6cf-4f94-887c-6874dd53deb4; UM_distinctid=15bf1f90973507-09bdbeecc8a3f1-871133d-e1000-15bf1f9097463b; all-lj=78917a1433741fe7067e3641b5c01569; _jzqckmp=1; _jzqx=1.1494417610.1494417610.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _ga=GA1.2.1563199523.1494413281; _gid=GA1.2.1979628260.1494417756; _smt_uid=5912f0e9.b3fb644; _qzja=1.176937353.1494413546114.1494413546114.1494417610092.1494417754116.1494418150594.0.0.0.6.2; _qzjb=1.1494417610092.4.0.0.0; _qzjc=1; _qzjto=6.2.0; _jzqa=1.1421860933554737700.1494413546.1494413546.1494417610.2; _jzqc=1; _jzqb=1.4.10.1494417610.1; CNZZDATA1253477573=628000428-1494413391-%7C1494418097; CNZZDATA1254525948=341047088-1494410628-%7C1494415011; CNZZDATA1255633284=1010315704-1494409642-%7C1494413722; CNZZDATA1255604082=64476216-1494410064-%7C1494416139; lianjia_ssid=9973b5dc-d5de-4b31-a55f-ebbac6356617',
	   }
def chengjiao_spider(db_cj,url_page=u"https://bj.lianjia.com/chengjiao/pg1rs%E5%86%A0%E5%BA%AD%E5%9B%AD"):
    """
    爬取页面链接中的成交记录
    """
    info_list=[u'链接',u'小区名称',u'户型',u'面积',u'朝向',u'楼层',u'建造时间',u'签约时间',u'签约单价',u'签约总价',u'房产类型',u'学区',u'地铁']
    print "chengjiao_spider " + url_page
    try:
#        req = urllib2.Request(url_page,headers=hds[random.randint(0,len(hds)-1)])
        req = urllib2.Request(url_page,headers=hds)
        source_code = urllib2.urlopen(req,timeout=10).read()
        plain_text=unicode(source_code)#,errors='ignore')
#        with open('test', 'w') as f:
#            f.write(plain_text)
#            f.close()   
        soup = BeautifulSoup(plain_text,'html.parser')
#        print plain_text
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        exception_write('chengjiao_spider',url_page)
        return
    except Exception,e:
        print e
        exception_write('chengjiao_spider',url_page)
        return

    cj_list=soup.find('ul',{'class':'listContent'})    
    cj_list=cj_list.findAll('li')
#    print cj_list
    for cj in cj_list:
        info_dict={}
        cjtitle = cj.find('div',{'class':'title'})
        href=cjtitle.find('a')
        cjname = cjtitle.text.split(" ")

        info_dict.update({info_list[0]:href.attrs['href']})
        cjhouseInfo = cj.find('div',{'class':'houseInfo'})
        info_dict.update({info_list[1]:cjname[0]})
        info_dict.update({info_list[2]:cjname[1]})
        info_dict.update({info_list[3]:cjname[2]})
    
#        print cjhouseInfo.text
        cjhouseInfoDetails = cjhouseInfo.text.replace(" ","").split("|")
#        print cjhouseInfoDetails
        info_dict.update({info_list[4]:cjhouseInfoDetails[0]})
    
        cjpositionInfo = cj.find('div',{'class':'positionInfo'})
#        print cjpositionInfo.text
        cjpositionInfo = cjpositionInfo.text.split(" ")
        info_dict.update({info_list[5]:cjpositionInfo[0]})
        info_dict.update({info_list[6]:cjpositionInfo[1]})
    
        cjdealDate = cj.find('div',{'class':'dealDate'})
        info_dict.update({info_list[7]:cjhouseInfo.text})
#        print cjdealDate.text
        cjunitPrice = cj.find('div',{'class':'unitPrice'})
#        print cjunitPrice
        cjunitPriceNum = re.sub("[^0-9]", "", cjunitPrice.text)
#        print cjunitPriceNum
        if cjunitPriceNum.isdigit() == True:
            cjunitPriceNum = int(cjunitPriceNum)
        else:
            continue
#       print cjunitPrice.text
        info_dict.update({info_list[8]:cjunitPrice.text})
        cjtotalPrice = cj.find('div',{'class':'totalPrice'})
        cjtotalPriceNum = re.sub("[^0-9]", "", cjtotalPrice.text)
        cjtotalPriceNum = int(cjtotalPriceNum)
#        print cjtotalPriceNum
        info_dict.update({info_list[9]:cjtotalPrice.text})
#        print cjtotalPrice.text
    
        cjdealCycleeInfo = cj.find('div',{'class':'dealCycleeInfo'})
        cjdealCycleeInfo = cjdealCycleeInfo.find('span',{'class':'dealCycleTxt'})
        cjdealCycleeInfo = cjdealCycleeInfo.findAll('span')
#        print cjdealCycleeInfo
        cjdealCycleeInfoOriginalPriceNum = re.sub("[^0-9]", "", cjdealCycleeInfo[0].text)
        cjdealCycleeInfoOriginalPriceNum = int(cjdealCycleeInfoOriginalPriceNum)
#        cjdealCycleeInfoOriginalDayNum = re.sub("[^0-9]", "", cjdealCycleeInfo[1].text)
#        cjdealCycleeInfoOriginalDayNum = int(cjdealCycleeInfoOriginalDayNum)
    #    print cjdealCycleeInfo
#        print cjdealCycleeInfoOriginalPriceNum
#        print cjdealCycleeInfoOriginalDayNum
        info_dict.update({info_list[10]:cjtotalPrice.text})
        info_dict.update({info_list[11]:cjtotalPrice.text})
        info_dict.update({info_list[12]:cjtotalPrice.text})
#        print info_dict
#        command=gen_chengjiao_insert_command(info_dict)
#        print command
#        db_cj.execute(command,1)

if __name__=="__main__":
    print "start..."
    db_cj = "dump"
    chengjiao_spider(db_cj)

