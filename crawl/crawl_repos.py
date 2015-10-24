#! /usr/bin/env python
#coding=utf-8

'''
@author : Fang Wang
@date : 2015.10.17
@desc : crawl repos of each programming language
'''

import requests
from lxml import html
import pickle
import time
import random


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

    language_repos = []

    for each_lanuange_url in language_url_list:
        try:
            time.sleep(random.randint(1,5))
            r = requests.get(each_lanuange_url, headers = hd)
            trending_content = r.text
            each_page_repos = parse_repos(trending_content)
            language_repos += each_page_repos
        except Exception, e:
            print ' crawl %s failed , error : %s' % (each_lanuange_url, str(e))

    return language_repos


def parse_repos(content):
    '''
    parse repo infos at content
    infos should be a list which contains all repos at current page
    each repo tuple like (repo_name, author, real_name)
    '''

    repos_list = []
    try:
        root = html.fromstring(content)
        repos_ele_list = root.find_class('repo-list-item')
        if not repos_ele_list:
            print 'parse repo ele failed. please try again.'
    except Exception, e:
        print 'parse repo ele failed. error : %s.' % str(e)
        return

    for each_repo_ele in repos_ele_list:
        try:
            repo_info_ele = each_repo_ele.xpath('h3')[0]
            repo_real_name = repo_info_ele.xpath('a/@href')[0][1:]
            author, repo_name = repo_real_name.split('/')
            repos_list.append((repo_name, author, repo_real_name))
        except Exception, e:
            print 'parse this repo failed, error : %s. ' % str(e)
            continue

    return repos_list


def crawl_all_language_repos():
    '''
    according to language list crawled, crawl all repos
    '''

    language_list = []
    try:
        with open('../data/language_list.pickle') as f:
            language_list = pickle.load(f)
    except Exception, e:
        print 'load language list failed, error : %s ' % str(e)

    if not language_list:
        return

    for each_lanuange_info in language_list:
        try:
            language_name, language_url = each_lanuange_info
            language_repos = crawl_repos_by_language(each_lanuange_info)
            save_each_language_repos(language_name, language_repos)
        except Exception, e:
            print 'crawl %s failed, error : %s. ' % (language_name, str(e))
            continue

    return


def save_each_language_repos(language_name, new_language_repos):
    '''
    save repos data to pickle file
    before save, it should drop duplicated data
    '''

    try:
        with open('../data/%s.pickle' % language_name) as f:
            language_repos = pickle.load(f)
            language_repos += new_language_repos
            language_repos = list(set(language_repos))
    except:
        language_repos = new_language_repos

    with open('../data/%s.pickle' % language_name, 'wb') as f:
        pickle.dump(language_repos, f)

    return


if __name__ == '__main__':
    #l = ('Rust', 'https://github.com/trending?l=rust')
    #crawl_repos_by_language(l)
    crawl_all_language_repos()
    '''
    with open('day.html') as f:
        content = f.read()
        print parse_repos(content)
    '''
