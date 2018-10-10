#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Project：      爬虫
-------------------------------------------------
   File Name：     dmhy-1.0.py
   Author：        Andy
   Site：          yaoling.ltd
   Eamil：         498330580@qq.com
   Time：          2018-09-14 16:24
-------------------------------------------------
"""
print('''
---------------------------- 瑶玲 ----------------------------
作者：Andy
网址：yaoling.ltd
Eamil：498330580@qq.com
版本：动漫花园-爬虫 1.0
说明：本版本为一个初始版本，主要为爬取动漫花园全站资源所写，
      主要配置为本目录下config.py文件，只简单的配置了一下界
      面，还未提供更多的选项与界面，数据库为MongoDB
计划：1.增加其他数据储存方式（比如：文本导出、其他数据库）
      2.config文件验证，增加用户第一次启动图形输入配置
      3.增加更多反扒措施（代理）
      4.可对爬取的分类进行选择
      5.API功能
      6.P2P共享
      7.增加用户功能
      8.增加异步爬取功能
      9.增加多线程爬取功能
后言：本人是经历了当初极影关闭事件的一名老动漫爱好者，写这个
      爬虫的初衷也是担心某天花园也无法访问，所以有了这个想法
      写一个爬虫将数据储存起来，方便以后使用，如果有字幕组的
      大佬觉得不合适我立刻删除自己的资料。说一下想法吧，我希
      望之后能把这个代码发展成一个P2P的网络，各个动漫爱好者的
      电脑都是一个小服务器，分担一点，以免网站无法访问时还可用
      后期准备加入用户功能。如果有其他建议请发邮箱，谢谢！
---------------------------- 瑶玲 ----------------------------      
''')

import config
import hanshu

while True:
    config_data = input('是否启用默认配置（Y/N）：')
    # 这一段为启用配置文件config的情况
    while config_data == 'Y' or config_data == 'y':
        hanshu.run()
        print('数据抓取完毕！！！')
        hanshu.daojishi(H=config.H, M=config.M, S=config.S)

    while config_data == 'N' or config_data == 'n':
        start_url = input('请输入开始页码（如不需要设置开始页码请直接回车）：')
        end_url = input('请输入结束页码（如不需要设置结束页码请直接回车）：')
        hanshu.run(start_url=start_url, end_url=end_url)
        print('数据抓取完毕！！！')
        hanshu.daojishi(H=config.H, M=config.M, S=config.S)

    else:
        print('您输入的内容为 %s ,启用默认配置文件输入“Y”，否则请输入“N”。' % config_data)
