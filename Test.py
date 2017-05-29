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

    hdsUserAgent = [
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}, \
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'}, \
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}, \
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}, \
        {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}, \
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'}, \
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}, \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}, \
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}, \
        {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'}, \
        {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

    hds = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'identity',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           #        'Cookie':'select_city=110000; select_nation=1; lianjia_uuid=00fc8dbf-e6cf-4f94-887c-6874dd53deb4; UM_distinctid=15bf1f90973507-09bdbeecc8a3f1-871133d-e1000-15bf1f9097463b; all-lj=78917a1433741fe7067e3641b5c01569; _jzqckmp=1; _jzqx=1.1494417610.1494417610.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _ga=GA1.2.1563199523.1494413281; _gid=GA1.2.1979628260.1494417756; _smt_uid=5912f0e9.b3fb644; _qzja=1.176937353.1494413546114.1494413546114.1494417610092.1494417754116.1494418150594.0.0.0.6.2; _qzjb=1.1494417610092.4.0.0.0; _qzjc=1; _qzjto=6.2.0; _jzqa=1.1421860933554737700.1494413546.1494413546.1494417610.2; _jzqc=1; _jzqb=1.4.10.1494417610.1; CNZZDATA1253477573=628000428-1494413391-%7C1494418097; CNZZDATA1254525948=341047088-1494410628-%7C1494415011; CNZZDATA1255633284=1010315704-1494409642-%7C1494413722; CNZZDATA1255604082=64476216-1494410064-%7C1494416139; lianjia_ssid=9973b5dc-d5de-4b31-a55f-ebbac6356617',
           # 'Cookie':'lianjia_uuid=5fde4b43-8c71-4bed-ad0d-ec339612fbeb; sample_traffic_test=controlled_66; select_city=110000; UM_distinctid=15c16e72e0a890-06b0fd49251c29-396a7807-fa000-15c16e72e0b806; _jzqckmp=1; lianjia_token=2.0031e03c78489820db204d15497f1ca53e; _smt_uid=591c6424.1d895acc; _jzqa=1.1332347072049126100.1495032870.1495032870.1495040251.2; _jzqc=1; _jzqx=1.1495032870.1495040251.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _jzqb=1.1.10.1495040251.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1048061317.1495032873; _gid=GA1.2.1297077282.1495040262; _gat_dianpu_agent=1; lianjia_ssid=f05dc78b-ea9f-243b-54a9-19eda074ee57'
           # 'Cookie':'lianjia_uuid=1190da6e-ddb9-4948-bfd1-d3f43076e167; all-lj=c28812af28ef34a41ba2474a2b5c52c2; UM_distinctid=15c1c3d4f0d24f-0b01c204a83f7a-396a7807-fa000-15c1c3d4f0e490; lianjia_token=2.000b4dbc267235a0851ae0951738c04327; _jzqx=1.1495122399.1495208680.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; sample_traffic_test=controlled_66; select_city=110000; _smt_uid=591dc1de.35aac84e; CNZZDATA1253477573=63672075-1495117236-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495203742; CNZZDATA1254525948=974177894-1495119036-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495204660; CNZZDATA1255633284=1733980612-1495117333-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495203744; CNZZDATA1255604082=2114464222-1495117758-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495205371; _qzja=1.1445448234.1495122398983.1495205140239.1495208679759.1495208679759.1495209058969.0.0.0.13.3; _qzjb=1.1495208679758.2.0.0.0; _qzjc=1; _qzjto=10.2.0; _jzqa=1.1440563072283717400.1495122399.1495205140.1495208680.3; _jzqc=1; _jzqckmp=1; _jzqb=1.2.10.1495208680.1; _ga=GA1.2.1522449273.1495122402; _gid=GA1.2.1164158679.1495209060; lianjia_ssid=a7f0df7a-e6b0-d3d8-ac44-7951b7c3fc4e',
           # 'Cookie':'select_city=110000; all-lj=78917a1433741fe7067e3641b5c01569; lianjia_uuid=72679f27-46c1-412d-9914-1610ee00032e; _jzqckmp=1; UM_distinctid=15c2184055abb2-03f4dd4a19304b-396a7807-fa000-15c2184055ba69; sample_traffic_test=test_66; lianjia_token=2.00414d206a38353cc950e0095b7ec35b67; ljref=pc_sem_baidu_ppzq_x; _jzqy=1.1495212736.1495212736.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E5%9C%A8%E7%BA%BF%E5%8C%97%E4%BA%AC%E4%BA%8C%E6%89%8B%E6%88%BF.-; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; CNZZDATA1253477573=754948759-1495208082-%7C1495208082; _smt_uid=591f1bea.443c5b41; CNZZDATA1254525948=919312602-1495210061-%7C1495210061; CNZZDATA1255633284=1354815648-1495209144-%7C1495209144; CNZZDATA1255604082=1936524490-1495210771-%7C1495210771; _qzja=1.713165405.1495210919245.1495210919245.1495210919246.1495212736464.1495212740365.0.0.0.11.1; _qzjb=1.1495210919246.11.0.0.0; _qzjc=1; _qzjto=11.1.0; _jzqa=1.1870246450224896500.1495210919.1495210919.1495210919.1; _jzqc=1; _jzqb=1.11.10.1495210919.1; _ga=GA1.2.1428545721.1495210930; _gid=GA1.2.1720298040.1495212742; lianjia_ssid=ec6b2eff-7a99-4387-8cf7-5df8a2d36322',
           # 'Cookie':'lianjia_uuid=e3221e01-932c-a5d8-2c0f-36c735161ae0; sample_traffic_test=test_66; select_city=110000; all-lj=0f6b18681ea67d53fa44b1df18064287; UM_distinctid=15c21ef3aea35e-02bd1c9ce87-396a7807-fa000-15c21ef3aeb24e; _jzqx=1.1495217946.1495217946.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _jzqckmp=1; _smt_uid=591f3719.46ac5291; CNZZDATA1253477573=250100245-1495213482-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495213482; CNZZDATA1254525948=1693761593-1495215463-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495215463; CNZZDATA1255633284=1553597661-1495214544-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495214544; CNZZDATA1255604082=1440683019-1495214969-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495214969; _qzja=1.885061892.1495217946141.1495217946141.1495217946142.1495218315886.1495218327111.0.0.0.4.1; _qzjb=1.1495217946142.4.0.0.0; _qzjc=1; _qzjto=4.1.0; _jzqa=1.3480395563082862000.1495217946.1495217946.1495217946.1; _jzqc=1; _jzqb=1.4.10.1495217946.1; _ga=GA1.2.1313234124.1495217956; _gid=GA1.2.565635435.1495218338; lianjia_ssid=0f0e70ea-3ac1-21fb-1bfb-ad0ef27288c1',
           'Cookie': 'lianjia_uuid=e3221e01-932c-a5d8-2c0f-36c735161ae0; sample_traffic_test=test_66; select_city=110000; all-lj=0f6b18681ea67d53fa44b1df18064287; UM_distinctid=15c21ef3aea35e-02bd1c9ce87-396a7807-fa000-15c21ef3aeb24e; _jzqx=1.1495217946.1495217946.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _jzqckmp=1; lianjia_token=2.002f9fe3d356e7ff703e32cae229addec4; _smt_uid=591f3719.46ac5291; _qzja=1.885061892.1495217946141.1495217946141.1495217946142.1495218813312.1495219330104.0.0.0.8.1; _qzjb=1.1495217946142.8.0.0.0; _qzjc=1; _qzjto=8.1.0; _jzqa=1.3480395563082862000.1495217946.1495217946.1495217946.1; _jzqc=1; CNZZDATA1253477573=250100245-1495213482-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495214574; CNZZDATA1254525948=1693761593-1495215463-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495215463; CNZZDATA1255633284=1553597661-1495214544-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495214544; CNZZDATA1255604082=1440683019-1495214969-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495214969; _jzqb=1.8.10.1495217946.1; _ga=GA1.2.1313234124.1495217956; _gid=GA1.2.1777610980.1495219332; lianjia_ssid=0f0e70ea-3ac1-21fb-1bfb-ad0ef27288c1',
           # 'Host':'bj.lianjia.com',
           # 'Upgrade Insecure-Requests':'1',
           # 'Cache-Control':'max-age=0',
           # 'User Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
           }
    hds['User-Agent'] = hdsUserAgent[random.randint(0,len(hdsUserAgent)-1)]['User-Agent']
    print hds
"""
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
"""
