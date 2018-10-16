#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Project：      爬虫
-------------------------------------------------
   File Name：     hanshu.py
   Author：        Andy
   Site：          yaoling.ltd
   Eamil：         498330580@qq.com
   Time：          2018-09-14 16:22
-------------------------------------------------
"""

import requests as req
from bs4 import BeautifulSoup
import time
import pymongo
import random
import config
import re
import pymongo.errors as pe


# 重复抓取等待倒计时函数
def daojishi(H, M, S):
    print('现在进入等待时间，如需提前结束，请重新运行。')
    print('您设置的等待时间为 %d 小时 %d 分钟 %d 秒,现在开始倒计时。' % (H, M, S))
    while H >= 0 and M >= 0 and S >= 0:
        if H > 0:
            print('距离下一次抓取还有 %d 小时 %d 分钟 %d 秒' % (H, M, S))
            time.sleep(1)
            S = S - 1
            if S < 0:
                S = 59
                M = M - 1
                if M < 0:
                    M = 59
                    H = H - 1
        elif H == 0 and M > 0:
            print('距离下一次抓取还有 %d 分钟 %d 秒' % (M, S))
            time.sleep(1)
            S = S - 1
            if S < 0:
                S = 59
                M = M - 1
        elif H == 0 and M == 0:
            print('距离下一次抓取还有 %d 秒' % S)
            time.sleep(1)
            S = S - 1
            if S < 0:
                print('等待结束，重新开始抓取！！！')


# 等待倒计时函数
def jishi(sec):
    while sec >= 0:
        print('等待倒计时 %d 秒' % sec)
        time.sleep(1)
        sec = sec - 1


# 网页抓取函数
def HTML_DATA(url, start_time, end_time):
    header = {'user-agent': random.choice(config.USER_AGENTS)}
    daojishi_data = random.randint(start_time, end_time)
    jishi(daojishi_data)
    print('开始爬取： %s' % url)
    while True:
        try:
            data = req.get(url, headers=header).text
            break
        except req.exceptions.ConnectionError:
            print('连接失败，正在重试，请稍等......')
            jishi(daojishi_data)
    return data


# 数据库连接并保存函数
def mongoDB(biao, jihe, suju, dizhi, fabu_link):
    myclient = pymongo.MongoClient("mongodb://%s:27017/" % dizhi)  # 连接mongodb数据库
    mydb = myclient[biao]  # 创建数据表
    mycol = mydb[jihe]  # 创建数据集合
    myquery = {"发布链接": fabu_link}  # 验证数据链接是否存在的条件

    chaoshi = 0
    while True:
        try:
            mydoc = mycol.find_one(myquery, max_time_ms=50000)  # 查询所有符合条件的数据
            chaoshi = 4
            if mydoc is not None:
                print('%s 数据已存在' % fabu_link)
                return '数据已存在'
            else:
                mycol.insert_one(suju)
                print('%s储存成功。' % fabu_link)
                break
        except pe.NetworkTimeout:
            chaoshi += 1
            print('数据库查询超时！！！   正在重新尝试查询第%d次，请稍后······' % chaoshi)
        except pe.ServerSelectionTimeoutError:
            daojishi_tmp = random.randint(3, 6)
            print('数据库繁忙，暂停 %d 秒!!!' % daojishi_tmp)
            jishi(daojishi_tmp)
    myclient.close()


# 对已抓取网页内容进行分析并储存，传入内容为html_text,返回内容为下一页网址，如果是最后一页着返回“这是最后一页，抓取完毕。”，如果是已抓取过的函数着返回“数据已存在”
def list_data(html, quanzhan=None):
    global xiayiyelianjie
    jisu = 0
    soup = BeautifulSoup(html, 'lxml')
    fabu_time = soup.find_all('span', style='display: none;')
    fenlei = (soup.find_all('font'))[19:]
    zimuzu = soup.find_all('td', 'title')
    lianjie = soup.find_all(href=re.compile('view'))
    xiazailianjie = soup.find_all(href=re.compile('magnet'))
    faburen = soup.find_all(href=re.compile('user_id'))
    xiayiye_link = soup.find_all(href=re.compile('page'))

    if len(list(xiazailianjie)) is not 80:
        xiazailianjie = []
        for dow in lianjie:
            neiye_data = HTML_DATA(url='https://share.dmhy.org' + dow['href'], start_time=config.START_TIME,
                                   end_time=config.END_TIME)
            soup_neiye_data = BeautifulSoup(neiye_data, 'lxml')
            xiazailianjie_tmp = soup_neiye_data.find_all(href=re.compile('magnet'))
            if xiazailianjie_tmp is not []:
                xiazailianjie_tmp_one = xiazailianjie_tmp[0]
                xiazailianjie.append(xiazailianjie_tmp_one)
            else:
                xiazailianjie.append('None')

    for link in xiayiye_link:
        if link.text.strip() == '下一頁':
            xiayiyelianjie = 'https://share.dmhy.org' + (link['href'])
        else:
            xiayiyelianjie = '这是最后一页，抓取完毕。'

    for t, f, z, l, x, fb in zip(fabu_time, fenlei, zimuzu, lianjie, xiazailianjie, faburen):
        jisu += 1
        suju_dict = {'发布时间': t.text, '发布分类': f.text}
        zimuzu_biaoti_list = z.text.strip().split('\n\n\t\t\t\t', 1)
        if len(zimuzu_biaoti_list) == 2:
            suju_dict['发布字幕组'] = zimuzu_biaoti_list[0]
            suju_dict['发布标题'] = l.text.strip()
        else:
            suju_dict['发布字幕组'] = 'None'
            suju_dict['发布标题'] = l.text.strip()
        suju_dict['发布者'] = fb.text
        suju_dict['发布链接'] = 'https://share.dmhy.org' + l['href']
        suju_dict['下载链接'] = x['href']
        fabu_link = 'https://share.dmhy.org' + l['href']
        print('开始储存：%s' % l.text.strip())
        tmp = mongoDB(biao=config.DATA_BIAO, jihe=config.DATA_JIHE, suju=suju_dict, dizhi=config.DATA_LINK,
                      fabu_link=fabu_link)
        if tmp == '数据已存在' and quanzhan == 'OFF':
            xiayiyelianjie = tmp
            break

    if xiayiyelianjie == '数据已存在':
        link_xiayiye = xiayiyelianjie
        return link_xiayiye
    elif xiayiyelianjie == '这是最后一页，抓取完毕。':
        return xiayiyelianjie
    else:
        print('\n' + '下一页的地址为：' + xiayiyelianjie + '开始抓取下一页')
        return xiayiyelianjie


# 验证输入是否为整数的函数
def int_panduan(shuru):
    while True:
        try:
            x = input(shuru)
            y = int(x)
            break
        except ValueError:
            print('输入错误请输入整数！！！')
    return y


# 验证是否输入为空
def kong():
    pass


# 主函数
def run(start_url=config.START_URL,end_url=config.END_URL):
    # 这一段是设置了开始和结束页数的爬取
    if start_url is not '' and end_url is not '':
        start_url = int(start_url)
        end_url = int(end_url)
        print('现在开始爬取 %s 页到 %s 页。' % (start_url,end_url))
        url_open_list = [config.URL_DPEN + r'topics/list/page/%d' % i for i in
                         range(start_url, end_url + 1)]
        for url in url_open_list:
            html_text = HTML_DATA(url=url, start_time=config.START_TIME, end_time=config.END_TIME)
            url_tmp = list_data(html=html_text, quanzhan=config.DATA_CHUNZAI)
            if url_tmp == '这是最后一页，抓取完毕。':
                print('这是最后一页抓取完毕。')
                break
            elif url_tmp == '数据已存在':
                print('最新数据已更新完毕。')
                break
    # 这一段是只设置了开始页数的爬取
    elif start_url is not '' and end_url is '':
        start_url = int(start_url)
        print('现在开始爬取 %s 页之后的内容。' % start_url)
        url = config.URL_DPEN + r'topics/list/page/%d' % start_url
        while True:
            url = list_data(
                html=HTML_DATA(url=url, start_time=config.START_TIME, end_time=config.END_TIME),
                quanzhan=config.DATA_CHUNZAI)
            if url == '这是最后一页，抓取完毕。':
                print('这是最后一页抓取完毕。')
                break
            elif url == '数据已存在':
                print('最新数据已更新完毕。')
                break
    # 这一段是只设置结束页码的爬取
    elif start_url is '' and end_url is not '':
        end_url = int(end_url)
        print('现在开始爬取 %s 页之前的内容。' % end_url)
        url_open_list = [config.URL_DPEN + r'topics/list/page/%d' % i for i in range(1, end_url + 1)]
        for url in url_open_list:
            html_text = HTML_DATA(url=url, start_time=config.START_TIME, end_time=config.END_TIME)
            url_tmp = list_data(html=html_text, quanzhan=config.DATA_CHUNZAI)
            if url_tmp == '这是最后一页，抓取完毕。':
                print('这是最后一页抓取完毕。')
                break
            elif url_tmp == '数据已存在':
                print('最新数据已更新完毕。')
                break
    # 这一段是全站爬取
    else:
        print('用户未设置开始与结束页码，进行全站爬取。')
        url = config.URL_DPEN
        while True:
            url = list_data(
                html=HTML_DATA(url=url, start_time=config.START_TIME, end_time=config.END_TIME),
                quanzhan=config.DATA_CHUNZAI)
            if url == '这是最后一页，抓取完毕。':
                print('这是最后一页抓取完毕。')
                break
            elif url == '数据已存在':
                print('最新数据已更新完毕。')
                break
