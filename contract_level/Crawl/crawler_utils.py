# -*- coding:utf-8 -*-

import urllib
import urllib2
import random

USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"                
]


# 使用代理访问网站 - GET方式实现
def crawl_url_by_get(url, proxy=None, enable_proxy=False):
    
    # make a string with 'GET'  
    method = 'GET'
    
    # create a handler 
    proxy_handler = urllib2.ProxyHandler(proxy)
    null_proxy_handler = urllib2.ProxyHandler({}) 
    
    # create an openerdirector instance according to enable_proxy
    if enable_proxy:
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies, proxy_handler, urllib2.HTTPHandler)
        # print 'using proxy to crawl pages', url
    else :
        opener = urllib2.build_opener(null_proxy_handler)
        # print 'without using proxy to crawl pages', url
    
    # install opener 
    urllib2.install_opener(opener)
    
    # buidl a request 
    request = urllib2.Request(url)
    
    # Umcomment the below line for ramdom choose the user_agent 
    # user_agent = random.choice(USER_AGENT_LSIT)
    user_agent = USER_AGENT_LIST[1] 
    request.add_header('User-Agent', user_agent)
    request.get_method = lambda:method
    
    try :
        connection = opener.open(request, timeout=5)
        if connection.code == 200:
            html = connection.read()
            return html
        else :
            return None
    except urllib2.HTTPError, ex:
        # print e.code, e.reason
        print 'spider_url_by_get（） -------- ', str(ex) 
        connection = ex
        return None
    except urllib2.URLError, ex:
        # print e.reason
        # print e.code, e.reason
        print 'spider_url_by_get（） -------- ', str(ex) 
        # remove_proxy(proxy)
        return None
    except Exception, ex:
        print 'spider_url_by_get（） -------- ', str(ex) 
        # remove_proxy(proxy)
        return None

def main():
	url = 'https://etherscan.io/address/0xda65eed883a48301d0ecf37465f135a7a0c9d978#code'
	html = crawl_url_by_get(url, proxy=None, enable_proxy=True)
	with open('./test_html', 'w') as f:
		f.write(html)

if __name__ == '__main__':
    main()
