#! /usr/bin/env python
#coding=utf-8

import requests
from lxml import html
import pickle

def crawl_language_list():
    '''
    crawl all programming languages at github
    '''
    trending_url = 'https://github.com/trending'

    hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'content-type': 'application/json',
    'Accept': '*/*',
    'Referer': 'https://github.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,es;q=0.2,fr;q=0.2,zh-TW;q=0.2,it;q=0.2'}

    r = requests.get(trending_url, headers = hd)
    trending_content = r.text

    language_list = parse_languages(trending_content)
    if language_list:
        with open ('../data/language_list.pickle', 'wb') as ll:
            pickle.dump(language_list, ll)
    else:
        print 'No language parsed at this page, please execute script again.'

    return


def parse_languages(trending_content):
    '''
    parse trending content to language list,
    which format should be [(language_name, language_url)]
    '''

    try:
        root = html.fromstring(trending_content)
    except Exception, e:
        print 'convert to lxml element failed. error : %s ' % str(e)
        return

    languages_ele_list = root.find_class('select-menu-item-text js-select-button-text js-navigation-open')

    language_list = []
    for each_lanuange_ele in languages_ele_list:
        try:
            each_lanuange_url = each_lanuange_ele.xpath('@href')[0].strip()
            each_lanuange_name = each_lanuange_ele.text.strip()
            language_list.append((each_lanuange_name, each_lanuange_url))
        except Exception, e:
            print 'parse this language element failed, error %s ' % str(e)
            continue

    return language_list


if __name__ == '__main__':
    crawl_language_list()
