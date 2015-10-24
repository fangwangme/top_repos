#! /usr/bin/env python
#coding=utf-8

'''
@author : Fang Wang
@date : 2015.10.17
@desc : crawl repos of each programming language
'''

import requests
import lxml

def crawl_repos_by_language(language_tuple):
    '''
    crawl repos at trening page of given language
    includes:
    1. today repos
    2. this week repos
    3. this month repos
    '''

    hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'content-type': 'application/json',
    'Accept': '*/*',
    'Referer': 'https://github.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,es;q=0.2,fr;q=0.2,zh-TW;q=0.2,it;q=0.2'}

    language_name, language_url = language_tuple

    language_url_list = [language_url]
    language_url_list.append(language_url + '&since=weekly')
    language_url_list.append(language_url + '&since=monthly')

    for each_lanuange_url in language_url_list:
        try:
            r = requests.get(each_lanuange_url, headers = hd)
            trending_content = r.text
            with open('day.html', 'w') as f:
                f.write(trending_content.encode('utf-8'))
            return
        except Exception, e:
            print ' crawl %s failed , error : %s' % (each_lanuange_url, str(e))

    return


if __name__ == '__main__':
    l = ('Rust', 'https://github.com/trending?l=rust')
    crawl_repos_by_language(l)
