#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Project：      爬虫
-------------------------------------------------
   File Name：     数据可视化导出.py
   Author：        Andy
   Site：          www.yaoling.ltd
   Eamil：         498330580@qq.com
   Time：          2018-09-14 20:12
-------------------------------------------------
"""

import pymongo
import time
import pandas as pd


def chazhao(data_chaxun, biao):
    myclient_chaxun = pymongo.MongoClient("mongodb://192.168.74.128:27017/")  # 连接mongodb数据库
    mydb_chaxun = myclient_chaxun['爬虫']  # 创建数据表
    mycol_chaxun = mydb_chaxun[biao]  # 创建数据集合

    count = mycol_chaxun.find(data_chaxun)
    myclient_chaxun.close()
    return count


def chucun(data, biao):
    myclient_chaxun = pymongo.MongoClient("mongodb://192.168.74.128:27017/")  # 连接mongodb数据库
    mydb_chaxun = myclient_chaxun['爬虫']  # 创建数据表
    mycol_chaxun = mydb_chaxun[biao]  # 创建数据集合
    mycol_chaxun.insert_one(data)
    myclient_chaxun.close()


if __name__ == "__main__":
    '''
    list_data = chazhao(data_chaxun={}, biao='动漫花园')

    list_time = []
    list_name = []
    list_zimuzu = []
    list_fenlei = []
    list_suju = []
    for i in list_data:
        list_suju.append(i)
        #list_time.append(i['发布时间'][:10])
        #list_name.append(i['发布者'])
        #list_zimuzu.append(i['发布字幕组'])
        #list_fenlei.append(i['发布分类'])
    #list_time_tmp = sorted(list(set(list_time)))
    #list_name_tmp = sorted(list(set(list_name)))
    '''
    df = pd.read_excel('动漫花园.xlsx')
    # xx = df.pivot_table(index='发布者',columns='发布时间',margins=True)
    fbz_time = df.groupby(['发布时间', '发布者']).size()
    x = fbz_time.groupby(['发布者']).cumsum()
    x.to_csv('字幕组.csv', encoding='utf-8')

    '''
    f = open('字幕组.csv',encoding='UTF-8')
    de = pd.read_csv(f)
    xx = de.pivot_table(['data'],index='time', columns='name')
    xx.to_csv('字幕组1.csv',encoding='utf-8')
    '''
    print(x)
    '''
    #list_zimuzu_tmp = sorted(list(set(list_zimuzu)))
    #list_fenlei_tmp = sorted(list(set(list_fenlei)))
    for n in list_name_tmp:
        jisu = 0
        print('获取到发布者：%s' % n)
        for t in list_time_tmp:
            print('获取到时间 %s' % t)
            for tj in list_suju:
                if (n in tj['发布者']) and (t in tj['发布时间']):
                    print()
                    jisu = jisu + 1
                    print(jisu)
                    if n == None:
                        n = '无用户名'
                    name_tmp = ('%s （%s）' % (n,tj['发布字幕组']))
                    print(name_tmp)
        print(jisu)

            #tongji_data = {'data':t, 'value':jisu, 'name':n}
            #print(tongji_data)
            #chucun(data=tongji_data,biao='发布者统计')


    #print(list_name)
    #print(list_name_tmp)
    #print(list_zimuzu)
    #print(list_zimuzu_tmp)
    #print(list_fenlei)
    #print(list_fenlei_tmp)

    #tongji(list_tongji=list_name_tmp,list_time_data=list_time_tmp,key='发布者',biao_name='发布者统计')
    #tongji(list_tongji=list_zimuzu_tmp, list_time_data=list_time_tmp, key='发布字幕组', biao_name='发布字幕组统计')
    #tongji(list_tongji=list_fenlei_tmp, list_time_data=list_time_tmp, key='发布分类', biao_name='发布分类统计')
    '''
