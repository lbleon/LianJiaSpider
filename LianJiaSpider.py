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
from time import ctime,sleep

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#登录，不登录不能爬取三个月之内的数据
#import LianJiaLogIn


#Some User Agents

hdsUserAgent=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

hds= {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Encoding':'identity',
	    'Accept-Language':'en-US,en;q=0.8',
	    'Connection':'keep-alive',
#        'Cookie':'select_city=110000; select_nation=1; lianjia_uuid=00fc8dbf-e6cf-4f94-887c-6874dd53deb4; UM_distinctid=15bf1f90973507-09bdbeecc8a3f1-871133d-e1000-15bf1f9097463b; all-lj=78917a1433741fe7067e3641b5c01569; _jzqckmp=1; _jzqx=1.1494417610.1494417610.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _ga=GA1.2.1563199523.1494413281; _gid=GA1.2.1979628260.1494417756; _smt_uid=5912f0e9.b3fb644; _qzja=1.176937353.1494413546114.1494413546114.1494417610092.1494417754116.1494418150594.0.0.0.6.2; _qzjb=1.1494417610092.4.0.0.0; _qzjc=1; _qzjto=6.2.0; _jzqa=1.1421860933554737700.1494413546.1494413546.1494417610.2; _jzqc=1; _jzqb=1.4.10.1494417610.1; CNZZDATA1253477573=628000428-1494413391-%7C1494418097; CNZZDATA1254525948=341047088-1494410628-%7C1494415011; CNZZDATA1255633284=1010315704-1494409642-%7C1494413722; CNZZDATA1255604082=64476216-1494410064-%7C1494416139; lianjia_ssid=9973b5dc-d5de-4b31-a55f-ebbac6356617',
#'Cookie':'lianjia_uuid=5fde4b43-8c71-4bed-ad0d-ec339612fbeb; sample_traffic_test=controlled_66; select_city=110000; UM_distinctid=15c16e72e0a890-06b0fd49251c29-396a7807-fa000-15c16e72e0b806; _jzqckmp=1; lianjia_token=2.0031e03c78489820db204d15497f1ca53e; _smt_uid=591c6424.1d895acc; _jzqa=1.1332347072049126100.1495032870.1495032870.1495040251.2; _jzqc=1; _jzqx=1.1495032870.1495040251.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _jzqb=1.1.10.1495040251.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1048061317.1495032873; _gid=GA1.2.1297077282.1495040262; _gat_dianpu_agent=1; lianjia_ssid=f05dc78b-ea9f-243b-54a9-19eda074ee57'
#'Cookie':'lianjia_uuid=1190da6e-ddb9-4948-bfd1-d3f43076e167; all-lj=c28812af28ef34a41ba2474a2b5c52c2; UM_distinctid=15c1c3d4f0d24f-0b01c204a83f7a-396a7807-fa000-15c1c3d4f0e490; lianjia_token=2.000b4dbc267235a0851ae0951738c04327; _jzqx=1.1495122399.1495208680.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; sample_traffic_test=controlled_66; select_city=110000; _smt_uid=591dc1de.35aac84e; CNZZDATA1253477573=63672075-1495117236-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495203742; CNZZDATA1254525948=974177894-1495119036-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495204660; CNZZDATA1255633284=1733980612-1495117333-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495203744; CNZZDATA1255604082=2114464222-1495117758-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495205371; _qzja=1.1445448234.1495122398983.1495205140239.1495208679759.1495208679759.1495209058969.0.0.0.13.3; _qzjb=1.1495208679758.2.0.0.0; _qzjc=1; _qzjto=10.2.0; _jzqa=1.1440563072283717400.1495122399.1495205140.1495208680.3; _jzqc=1; _jzqckmp=1; _jzqb=1.2.10.1495208680.1; _ga=GA1.2.1522449273.1495122402; _gid=GA1.2.1164158679.1495209060; lianjia_ssid=a7f0df7a-e6b0-d3d8-ac44-7951b7c3fc4e',
#'Cookie':'select_city=110000; all-lj=78917a1433741fe7067e3641b5c01569; lianjia_uuid=72679f27-46c1-412d-9914-1610ee00032e; _jzqckmp=1; UM_distinctid=15c2184055abb2-03f4dd4a19304b-396a7807-fa000-15c2184055ba69; sample_traffic_test=test_66; lianjia_token=2.00414d206a38353cc950e0095b7ec35b67; ljref=pc_sem_baidu_ppzq_x; _jzqy=1.1495212736.1495212736.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E5%9C%A8%E7%BA%BF%E5%8C%97%E4%BA%AC%E4%BA%8C%E6%89%8B%E6%88%BF.-; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; CNZZDATA1253477573=754948759-1495208082-%7C1495208082; _smt_uid=591f1bea.443c5b41; CNZZDATA1254525948=919312602-1495210061-%7C1495210061; CNZZDATA1255633284=1354815648-1495209144-%7C1495209144; CNZZDATA1255604082=1936524490-1495210771-%7C1495210771; _qzja=1.713165405.1495210919245.1495210919245.1495210919246.1495212736464.1495212740365.0.0.0.11.1; _qzjb=1.1495210919246.11.0.0.0; _qzjc=1; _qzjto=11.1.0; _jzqa=1.1870246450224896500.1495210919.1495210919.1495210919.1; _jzqc=1; _jzqb=1.11.10.1495210919.1; _ga=GA1.2.1428545721.1495210930; _gid=GA1.2.1720298040.1495212742; lianjia_ssid=ec6b2eff-7a99-4387-8cf7-5df8a2d36322',
#'Cookie':'lianjia_uuid=e3221e01-932c-a5d8-2c0f-36c735161ae0; sample_traffic_test=test_66; select_city=110000; all-lj=0f6b18681ea67d53fa44b1df18064287; UM_distinctid=15c21ef3aea35e-02bd1c9ce87-396a7807-fa000-15c21ef3aeb24e; _jzqx=1.1495217946.1495217946.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _jzqckmp=1; _smt_uid=591f3719.46ac5291; CNZZDATA1253477573=250100245-1495213482-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495213482; CNZZDATA1254525948=1693761593-1495215463-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495215463; CNZZDATA1255633284=1553597661-1495214544-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495214544; CNZZDATA1255604082=1440683019-1495214969-http%253A%252F%252Fcaptcha.lianjia.com%252F%7C1495214969; _qzja=1.885061892.1495217946141.1495217946141.1495217946142.1495218315886.1495218327111.0.0.0.4.1; _qzjb=1.1495217946142.4.0.0.0; _qzjc=1; _qzjto=4.1.0; _jzqa=1.3480395563082862000.1495217946.1495217946.1495217946.1; _jzqc=1; _jzqb=1.4.10.1495217946.1; _ga=GA1.2.1313234124.1495217956; _gid=GA1.2.565635435.1495218338; lianjia_ssid=0f0e70ea-3ac1-21fb-1bfb-ad0ef27288c1',
'Cookie':'lianjia_uuid=6bbd3f81-f011-4c8a-9bfd-533cf7c4cd88; sample_traffic_test=test_66; select_city=110000; all-lj=5ce010dbdb86da2c0bba3b0cda32eb3e; UM_distinctid=15c35f3eb44ce-0191f42b05153e-396a7807-fa000-15c35f3eb45a01; _jzqx=1.1495553797.1495553797.1.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.-; _jzqckmp=1; lianjia_token=2.00225a99c95b22856a33f7b0f8261c0900; _smt_uid=59245704.58360300; CNZZDATA1253477573=990217172-1495550274-null%7C1495550274; CNZZDATA1254525948=1227878780-1495552094-null%7C1495552094; CNZZDATA1255633284=1361466855-1495550874-null%7C1495550874; CNZZDATA1255604082=94780685-1495553637-null%7C1495553637; _qzja=1.980551795.1495553798484.1495553798484.1495553798484.1495553798484.1495553812767.0.0.0.2.1; _qzjb=1.1495553798484.2.0.0.0; _qzjc=1; _qzjto=2.1.0; _jzqa=1.2924051980438953000.1495553797.1495553797.1495553797.1; _jzqc=1; _jzqb=1.2.10.1495553797.1; _ga=GA1.2.821737569.1495553802; _gid=GA1.2.1735411872.1495553816; lianjia_ssid=136bce21-fdf4-4136-95ba-d30f681cb08d',
#'Host':'bj.lianjia.com',
#'Upgrade Insecure-Requests':'1',
#'Cache-Control':'max-age=0',
#'User Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

#北京区域列表
#regions=[u"东城",u"西城",u"朝阳",u"海淀",u"丰台",u"石景山","通州",u"昌平",u"大兴",u"亦庄开发区",u"顺义",u"房山",u"门头沟",u"平谷",u"怀柔",u"密云",u"延庆",u"燕郊"]
regions=[u"朝阳",u"东城",u"西城",u"海淀",u"昌平"]


lock = threading.Lock()


class SQLiteWraper(object):
    """
    数据库的一个小封装，更好的处理多线程写入
    """
    def __init__(self,path,command='',*args,**kwargs):  
        self.lock = threading.RLock() #锁  
        self.path = path #数据库连接参数  
        
        if command!='':
            conn=self.get_conn()
            cu=conn.cursor()
            cu.execute(command)
    
    def get_conn(self):  
        conn = sqlite3.connect(self.path)#,check_same_thread=False)  
        conn.text_factory=str
        return conn   
      
    def conn_close(self,conn=None):  
        conn.close()  
    
    def conn_trans(func):  
        def connection(self,*args,**kwargs):  
            self.lock.acquire()  
            conn = self.get_conn()  
            kwargs['conn'] = conn  
            rs = func(self,*args,**kwargs)  
            self.conn_close(conn)  
            self.lock.release()  
            return rs  
        return connection  
    
    @conn_trans    
    def execute(self,command,method_flag=0,conn=None):  
        cu = conn.cursor()
        try:
            if not method_flag:
                cu.execute(command)
            else:
                cu.execute(command[0],command[1])
            conn.commit()
        except sqlite3.IntegrityError,e:
            print e
            return -1
        except Exception, e:
            print e
            return -2
        return 0
    
    @conn_trans
    def fetchall(self,command="select name from xiaoqu",conn=None):
        cu=conn.cursor()
        lists=[]
        try:
            cu.execute(command)
            lists=cu.fetchall()
        except Exception,e:
            print e
            pass
        return lists


def gen_xiaoqu_insert_command(info_dict):
    """
    生成小区数据库插入命令
    """
    info_list=[u'小区名称',u'大区域',u'小区域',u'小区户型',u'建造时间']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
    command=(r"insert into xiaoqu values(?,?,?,?,?)",t)
    return command


def gen_chengjiao_insert_command(info_dict):
    """
    生成成交记录数据库插入命令
    """
    info_list=[u'链接',u'小区名称',u'户型',u'面积',u'朝向',u'楼层',u'建造时间',u'签约时间',u'签约单价',u'签约总价',u'房产类型',u'学区',u'地铁']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
    command=(r"insert into chengjiao values(?,?,?,?,?,?,?,?,?,?,?,?,?)",t)
    return command


def xiaoqu_spider(db_xq,url_page=u"https://bj.lianjia.com/xiaoqu/pg1rs%E6%98%8C%E5%B9%B3/"):
    """
    爬取页面链接中的小区信息
    """
    info_list=[u'小区名称',u'大区域',u'小区域',u'小区户型',u'建造时间']
    print "xiaoqu_spider start..."
    print url_page
    try:
#        req = urllib2.Request(url_page,headers=hds[random.randint(0,len(hds)-1)])
        req = urllib2.Request(url_page,headers=hds)
        source_code = urllib2.urlopen(req,timeout=10).read()
#        print source_code
        plain_text=unicode(source_code)#,errors='ignore')
#        print plain_text  
        soup = BeautifulSoup(plain_text,'html.parser')
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e.code
        exit(-1)
    except Exception,e:
        print e.message
        exit(-1)
    
    xiaoqu_list=soup.findAll('li',{'class':'clear xiaoquListItem'})
    for xq in xiaoqu_list:
        info_dict={}
        xqinfo = xq.find('div',{'class':'info'})
        xqinfotitle = xqinfo.find('div',{'class':'title'})
        info_dict.update({info_list[0]:xqinfotitle.find('a').text})
        xqinfopositionInfo = xqinfo.find('div',{'class':'positionInfo'})
#        print xqinfopositionInfo
        info_dict.update({info_list[1]:xqinfopositionInfo.find('a',{'class':'district'}).text})
        info_dict.update({info_list[2]:xqinfopositionInfo.find('a',{'class':'bizcircle'}).text})
        content = unicode(xqinfopositionInfo)
        content = content.replace('\r', '').replace('\n', '')
        content = content.replace(' ','')
#        with open('test', 'w') as f:
#            f.write(xqinfopositionInfo.prettify())
#            f.close()
#        content = unicode(xqinfopositionInfo.renderContents().strip())
#        content = unicode(xqinfopositionInfo)
#        print content
        info = re.findall(r"</a>.*?</a>(.*?)</div>",content)
#        print "info is "
#        print info
        info_dict.update({info_list[3]:info[0]})
        infoBuildDate = re.sub("[^0-9]", "", info[0])
#        print infoBuildDate
        if infoBuildDate.isdigit() == True:
            infoBuildDateNum = int(infoBuildDate)
#            print infoBuildDateNum
        else:
            continue
#        skip the xj < 2000
        if infoBuildDateNum < 2000:
            continue
        info_dict.update({info_list[4]:infoBuildDate})
#        print info_dict	
        """
        info_dict.update({u'小区名称':xq.find('a').text})
        
        content=unicode(xq.find('div',{'class':'con'}).renderContents().strip())
        info=re.match(r".+>(.+)</a>.+>(.+)</a>.+</span>(.+)<span>.+</span>(.+)",content)
        if info:
            info=info.groups()
            info_dict.update({u'大区域':info[0]})
            info_dict.update({u'小区域':info[1]})
            info_dict.update({u'小区户型':info[2]})
            info_dict.update({u'建造时间':info[3][:4]})
        """
        command=gen_xiaoqu_insert_command(info_dict)
#        print command
        db_xq.execute(command,1)
    print "xiaoqu_spider end..."
    
def do_xiaoqu_spider(db_xq,region=u"昌平"):
    """
    爬取大区域中的所有小区信息
    """
    print "%s is ready to spider" % region
    url=u"https://bj.lianjia.com/xiaoqu/rs"+region+"/"
    try:
#        req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
        req = urllib2.Request(url,headers=hds)
        source_code = urllib2.urlopen(req,timeout=5).read()
        plain_text=unicode(source_code)#,errors='ignore')
#        print plain_text
        soup = BeautifulSoup(plain_text,'html.parser')
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        return
    except Exception,e:
        print e
        return
    d="d="+soup.find('div',{'class':'page-box house-lst-page-box'}).get('page-data')
    exec(d)
    total_pages=d['totalPage']
#    print total_pages
    threads=[]
#    """
    for i in range(total_pages):
        url_page=u"https://bj.lianjia.com/xiaoqu/pg%drs%s/" % (i+1,region)
        t=threading.Thread(target=xiaoqu_spider,args=(db_xq,url_page))
        threads.append(t)
#   Test for the region Page 1 First
#    url_page=u"https://bj.lianjia.com/xiaoqu/pg%drs%s/" % (1,region)

#    t=threading.Thread(target=xiaoqu_spider,args=(db_xq,url_page))
#    threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
#   """
    print "%s is finished to spider" % region


def chengjiao_spider(db_cj,url_page=u"https://bj.lianjia.com/chengjiao/pg1rs%E5%86%A0%E5%BA%AD%E5%9B%AD"):
    """
    爬取页面链接中的成交记录
    """
    info_list=[u'链接',u'小区名称',u'户型',u'面积',u'朝向',u'楼层',u'建造时间',u'签约时间',u'签约单价',u'签约总价',u'房产类型',u'学区',u'地铁']
    print "chengjiao_spider page " + url_page
    try:
#        req = urllib2.Request(url_page,headers=hds[random.randint(0,len(hds)-1)])
#        req = urllib2.Request(url_page,headers=hdsUserAgent[random.randint(0,len(hds)-1)])
#
#simulate the broswer with rodam User Agent
        hds['User-Agent'] = hdsUserAgent[random.randint(0,len(hdsUserAgent)-1)]['User-Agent']
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
    if cj_list :
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
            info_dict.update({info_list[7]:cjdealDate.text})
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
    #        print cjdealCycleeInfo[0].text
            info_dict.update({info_list[10]:cjdealCycleeInfo[0].text})
            info_dict.update({info_list[11]:cjtotalPrice.text})
            info_dict.update({info_list[12]:cjtotalPrice.text})
    #        print info_dict
            command=gen_chengjiao_insert_command(info_dict)
    #        print command
            db_cj.execute(command,1)
    else:
        print "could not find listContent"
        exception_write('chengjiao_spider', url_page)
#        exception_write('xiaoqu_chengjiao_spider', xq_name)
#        print plain_text



def xiaoqu_chengjiao_spider(db_cj,xq_name=u"澳洲康都"):
    """
    爬取小区成交记录
    """
    url = u"http://bj.lianjia.com/chengjiao/rs"+urllib2.quote(xq_name)+"/"
    print "xiaoqu_chengjiao_spider" + url
    try:
#        req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
#        req = urllib2.Request(url,headers=hdsUserAgent[random.randint(0,len(hds)-1)])
#        hds['User Agent'] = hdsUserAgent[random.randint(0,len(hdsUserAgent) - 1)]
#        print hds
#simulate the broswer with rodam User Agent
        hds['User-Agent'] = hdsUserAgent[random.randint(0,len(hdsUserAgent)-1)]['User-Agent']
        req = urllib2.Request(url,headers=hds)
        source_code = urllib2.urlopen(req,timeout=10).read()
        plain_text=unicode(source_code)#,errors='ignore')   
        soup = BeautifulSoup(plain_text,'html.parser')
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        exception_write('xiaoqu_chengjiao_spider',xq_name)
        return
    except Exception,e:
        print e
        exception_write('xiaoqu_chengjiao_spider',xq_name)
        return

    #find how many the cj is
    totalnumofcjhouse=soup.find('div',{'class':'total fl'})
    if totalnumofcjhouse:
        totalnumofcjhouse=totalnumofcjhouse.find('span')
        totalnumofcjhouse=int(totalnumofcjhouse.text)
#       print totalnumofcjhouse
        if totalnumofcjhouse == 0:
            return
    else:
        print "page does not contains the total fl"
        exception_write('xiaoqu_chengjiao_spider', xq_name)
        return

    content=soup.find('div',{'class':'page-box house-lst-page-box'})
    total_pages=0
    if content:
        d="d="+content.get('page-data')
        exec(d)
        total_pages=d['totalPage']
        print "xiaoqu chengjiao spider pages total num %d" %(total_pages)

    else:
        print "page is not get due to the constent missing"
#        print plain_text
#       debug the cannot fond pages html
        #home page without the login info is coming
#        with open('test', 'w') as f:
#            f.write(plain_text)
#            f.close()
        exception_write('xiaoqu_chengjiao_spider', xq_name)
        return
    threads=[]
    for i in range(total_pages):
        url_page=u"http://bj.lianjia.com/chengjiao/pg%drs%s/" % (i+1,urllib2.quote(xq_name))
#        print "input page to spide" + url_page
        t=threading.Thread(target=chengjiao_spider,args=(db_cj,url_page))
        threads.append(t)
#        sleep(random.randint(0,1))
#        t.start()

#        t.join()

#Spider for the 1st Page of ChenJiao
#    threads=[]
#    url_page=u"https://bj.lianjia.com/chengjiao/pg%drs%s/" % (1,urllib2.quote(xq_name))
#    t=threading.Thread(target=chengjiao_spider,args=(db_cj,url_page))
#    threads.append(t)
# check the spider one by one

    for t in threads:
        t.start()
    for t in threads:
        t.join()

def get_last_failed_xq():
    excep_list = exception_read()
    for excep in excep_list:
        excep = excep.strip()
        if excep == "":
            continue
        excep_name, url = excep.split(" ", 1)
        if excep_name == "xiaoqu_chengjiao_spider" :
            return url
        else:
            continue

def do_xiaoqu_chengjiao_spider(db_xq,db_cj):
    """
    批量爬取小区成交记录
    """
    count=0
    xq_list=db_xq.fetchall()
#Test for one SingleXiaoqu First
#    xiaoqu_chengjiao_spider(db_cj,xq_list[0][0])
#    """
#   read from the log of the lastname
    last_failed_xq_name = get_last_failed_xq()
    notfoundlastfailedxq = True

    for xq in xq_list:
        count += 1
        print xq[0],last_failed_xq_name
        print notfoundlastfailedxq
        #skip the success ones
        #1346 ~ 1370 is easy to have traffice issue of ip
        #if para thread, almost 30 xq will make the traffic strang and blocked
        #the cookie is the most important one for getting the data, could think of login again and again
        if xq[0] != last_failed_xq_name and notfoundlastfailedxq:
            pre_xq_name = xq[0]
            continue
        else:
            if notfoundlastfailedxq :
                xiaoqu_chengjiao_spider(db_cj, pre_xq_name)
            notfoundlastfailedxq = False
            xiaoqu_chengjiao_spider(db_cj,xq[0])
            print 'have spidered %d %s xiaoqu' % (count,xq[0])
#        sleep(random.randint(0, 5))
#            exception_write('last_chenjiao_spider', count)
#    """
    print 'done'


def exception_write(fun_name,url):
    """
    写入异常信息到日志
    """
    lock.acquire()
    f = open('log.txt','a')
    line="%s %s\n" % (fun_name,url)
    f.write(line)
    f.close()
    lock.release()

    #exit the spider when the first exception meet
    exit(0)


def exception_read():
    """
    从日志中读取异常信息
    """
    lock.acquire()
    f=open('log.txt','r')
    lines=f.readlines()
    f.close()
    f=open('log.txt','w')
    f.truncate()
    f.close()
    lock.release()
    return lines


def exception_spider(db_cj):
    """
    重新爬取爬取异常的链接
    """
    count=0
    excep_list=exception_read()
    while excep_list:
        for excep in excep_list:
            excep=excep.strip()
            if excep=="":
                continue
            excep_name,url=excep.split(" ",1)
            if excep_name=="chengjiao_spider":
                chengjiao_spider(db_cj,url)
                count+=1
            elif excep_name=="xiaoqu_chengjiao_spider":
                xiaoqu_chengjiao_spider(db_cj,url)
                count+=1
            else:
                print "wrong format"
            print "have spidered %d exception url" % count
        excep_list=exception_read()
    print 'all done ^_^'
    


if __name__=="__main__":
    print "start..."
    command="create table if not exists xiaoqu (name TEXT primary key UNIQUE, regionb TEXT, regions TEXT, style TEXT, year TEXT)"
    db_xq=SQLiteWraper('lianjia-xq.db',command)
    
    command="create table if not exists chengjiao (href TEXT primary key UNIQUE, name TEXT, style TEXT, area TEXT, orientation TEXT, floor TEXT, year TEXT, sign_time TEXT, unit_price TEXT, total_price TEXT,fangchan_class TEXT, school TEXT, subway TEXT)"
    db_cj=SQLiteWraper('lianjia-cj.db',command)
    
    print "DB created"
#    xiaoqu_chengjiao_spider(db_cj)
#    do_xiaoqu_spider(db_xq,regions[0])
#    do_xiaoqu_chengjiao_spider(db_xq,db_cj)

#   爬下所有的小区信息
 #   for region in regions:
 #       do_xiaoqu_spider(db_xq,region)
    
    #爬下所有小区里的成交信息
    do_xiaoqu_chengjiao_spider(db_xq,db_cj)
    
    #重新爬取爬取异常的链接
#    exception_spider(db_cj)

