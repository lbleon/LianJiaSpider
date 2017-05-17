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

def chengjiao_spider(db_cj,url_page=u"https://bj.lianjia.com/chengjiao/pg1rs%E5%86%A0%E5%BA%AD%E5%9B%AD"):
    """
    爬取页面链接中的成交记录
    """
    print "chengjiao_spider " + url_page
    try:
#        req = urllib2.Request(url_page,headers=hds[random.randint(0,len(hds)-1)])
        req = urllib2.Request(url_page,headers=hds)
        source_code = urllib2.urlopen(req,timeout=10).read()
        plain_text=unicode(source_code)#,errors='ignore')   
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
    cj_list=soup.findAll('ul',{'class':'channelList'})    
    cj_list=cj_list.findAll('li')
    for cj in cj_list:
        info_dict={}
        href=cj.find('a')
        if not href:
            continue
        info_dict.update({u'链接':href.attrs['href']})
        content=cj.find('h2').text.split()
        if content:
            info_dict.update({u'小区名称':content[0]})
            info_dict.update({u'户型':content[1]})
            info_dict.update({u'面积':content[2]})
        content=unicode(cj.find('div',{'class':'con'}).renderContents().strip())
        content=content.split('/')
        if content:
            info_dict.update({u'朝向':content[0].strip()})
            info_dict.update({u'楼层':content[1].strip()})
            if len(content)>=3:
                content[2]=content[2].strip();
                info_dict.update({u'建造时间':content[2][:4]}) 
        content=cj.findAll('div',{'class':'div-cun'})
        if content:
            info_dict.update({u'签约时间':content[0].text})
            info_dict.update({u'签约单价':content[1].text})
            info_dict.update({u'签约总价':content[2].text})
        content=cj.find('div',{'class':'introduce'}).text.strip().split()
        if content:
            for c in content:
                if c.find(u'满')!=-1:
                    info_dict.update({u'房产类型':c})
                elif c.find(u'学')!=-1:
                    info_dict.update({u'学区':c})
                elif c.find(u'距')!=-1:
                    info_dict.update({u'地铁':c})
        
        command=gen_chengjiao_insert_command(info_dict)
        print command
        db_cj.execute(command,1)

if __name__=="__main__":
    print "start..."
    db_cj = "dump"
    chengjiao_spider(db_cj)

