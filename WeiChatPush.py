#!/usr/bin/env python

import re
import urllib2  
import sqlite3
import random
import threading
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


try: import json
except ImportError: import simplejson

url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxdd485458908a9d6a&secret=48a622f63324a9312e4cac52616488a7"       
url_sendtextmsg = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token="

def getToken():


    req = urllib2.Request(url)
#    req = urllib2.Request(url,hds)
#    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req)
#    response = urllib2.urlopen(req, json.dumps(data))
    data = json.load(response)   
    print data['access_token']
    return data['access_token']
    
def sendText(url, text):
    data = {
    "touser": "oD_MZxHm5e8uhg2apAbonEwuUGaY", 
    "msgtype": "text", 
    "text": {
        "content": "Hello World"
    }
    }
    data["text"]["content"] = text
    
    jsontext = json.dumps(data)
#    jsontext['msgtype'] = 'text'
    print jsontext 
    req = urllib2.Request(url)

    response = urllib2.urlopen(req, jsontext)
    data = json.load(response)
#    print data   
#    print data['errmsg']
#    return data['errmsg']

if __name__ == '__main__':

    accesstoken = getToken()
    url_sendtextmsg = url_sendtextmsg + accesstoken
#    print url_sendtextmsg
    text2send = "This is from My Test Client"
    sendText(url_sendtextmsg, text2send)