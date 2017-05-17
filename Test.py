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
#    content =  str(BeautifulSoup(html,"html.parser"))
    content =  unicode(BeautifulSoup(html,"html.parser"))
    content = content.replace('\r', '').replace('\n', '')
    content = content.replace(' ','')
    print content
#<\s*?$tagname\b[^>]*>(.*?)</$tagname\b[^>]*>
    
    info = re.findall(r"</a>.*?</a>(.*?)</div>",content)
    info = info[0].split(" ");
#    print info
    print info

