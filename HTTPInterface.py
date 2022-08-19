import os
import urllib, urllib.request as urllib2
import urllib.parse as urlparse

import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.74 Safari/537.36'}

def http_get(url, headers=None, cook=None):
    try:
        r = requests.get(url, headers=headers, cookies=cook).content
        return r
    except urllib2.URLError as e:
        return ''

def http_post(url, cookie_file='', postData={}, data=''):
    try:
        if (data != ''):
            postData = dict(urlparse.parse_qsl(data))
        # net = net(cookie_file=cookie_file)
        # return net.http_POST(url,postData).content
        return requests.post(url, postData).content
    except urllib2.URLError as e:
        return ''
