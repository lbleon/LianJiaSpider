import urllib2

def get_proxy():
    url_page = "http://127.0.0.1:5000/get/"
    req = urllib2.Request(url_page)
    source_code = urllib2.urlopen(req, timeout=10).read()
    return source_code

def delete_proxy(proxy):
#    requests.get("http://127.0.0.1:5000/delete/?proxy={}".format(proxy))
    url_page = "http://127.0.0.1:5000/delete/?proxy={}".format(proxy)
    req = urllib2.Request(url_page)
    source_code = urllib2.urlopen(req, timeout=10).read()
    return source_code

# your spider code

def spider():
    opener = urllib2.build_opener(
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.ProxyHandler({'http': 'http://'+ get_proxy()}))
    urllib2.install_opener(opener)
    print urllib2.urlopen('http://www.google.com').read()

if __name__=="__main__":
    print "start..."
    spider()