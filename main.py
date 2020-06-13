"""
杨志朗 1700094803
这里是主程序， 我在前面写了zhihu_crawler.py 和 visualization.py,
zhihu_crawler.py 实现了用cookies登陆知乎，并爬取热搜榜，将其保存在当前目录下的ZhihuRanking.txt中
visualization.py 实现了利用ZhihuRanking.txt 来进行可视化，将结果保存在当前目录下的知乎热榜实时排名.txt中
在这段程序里面把前面两个程序import进来

-----------------------------------------分割线-----------------------------------------------------

在这段程序里面我们要做的就是剩余的事情， 即每n秒跑一次 zhihu_crawler.py(), 获得最新的热搜， 这个n的系数保存在'./csv_data/config.csv' 当中， 可以自行修改；
我们爬虫完就会更新ZhihuRanking.txt的数据，我们立刻进行普通的渲染，把效果展示出来，
然后我们再从'./csv_data/keywords.csv' 当中读入重点观测的关键词，并对ZhihuRanking.txt 中进行匹配，
若有相应的词时，我们重新进行一次自定义的渲染，即出现关键词那行会到最上面一行来，再让电脑发出推特的声音，最后进行页面刷新


"""

from zhihu_crawler import Zhihu  # 导入已经定义的类
from visualization import visualization, customized_visualization  # 导入已经写好的函数
from selenium import webdriver
from playsound import playsound
import numpy as np
import pandas as pd
import time
import os

#  这个网页一定要设置成全局变量，好让所有的函数都可以控制网页
global pic_browser  # 这是可视化的网页


#  这个函数就是让电脑发出声音的, 请先pip install playsound
def buzz():
    playsound('./mp3/twitter.mp3')


#  这个函数就是把渲染好的网页打开来
def open_local_html():
    print("正在打开可视化的网页\n\n")
    # 这里是个大坑，打开本地网页的时候是一定要"file:///" + 本地网页的绝对地址的
    local_url = 'file:///' + os.path.abspath('知乎热榜实时排名.html')
    pic_browser.maximize_window()
    pic_browser.get(local_url)


def refresh_local_html():
    print("重新渲染了该网页，为您刷新中\n\n")
    pic_browser.refresh()


if __name__ == "__main__":
    #  webdriver请自行更改成自己的路径
    pic_browser = webdriver.Chrome(executable_path="D:/ChromePython/chromedriver.exe")
    pic_browser.minimize_window()

    #  先把两个csv文件读出来
    df1 = pd.read_csv('./csv_data/config.csv', header=0)
    refresh_time = df1['refresh_time'].item()  # 读取要刷新的时间
    df2 = pd.read_csv("./csv_data/keywords.csv", header=0, encoding='utf-8-sig')
    keywords_list = []
    for item in df2['keywords']:
        keywords_list.append(item)

    is_open = False  # 这个flag是用来判断有没有打开网页的，如果没有就打开，如果已经打开了就刷新网页

    while True:
        zhihu = Zhihu()  # Zhihu是定义的类
        zhihu.login()
        zhihu.crawl()
        print("\n\n爬虫完毕\n\n")
        visualization()
        print("\n\n可视化完毕")
        # 如果可视化的网页已经开起来了，就刷新； 还没有打开就开起来
        if not is_open:
            open_local_html()
            is_open = True
        else:
            refresh_local_html()
        t = refresh_time
        #  检查有没有出现keywords!
        with open("ZhihuRanking.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            cnt = 0  # 用来记录正在读第几条line
            cnt_list = []  # 用来记录哪几条line出现了关键词， 等下要作为参数传给customized_visualization()
            for line in lines:
                cnt += 1
                for keyword in keywords_list:
                    if keyword in line:
                        print("第  %d  条热搜里面出现了关键词  %s !!！" % (cnt, keyword))
                        cnt_list.append(cnt)
                        buzz()
                        break
        # 下面我们要用cnt_list 来进行定制化的可视化过程, 如果cnt_list为空则不用再重新渲染了
        if len(cnt_list) != 0:
            customized_visualization(cnt_list)
            refresh_local_html()

        for i in range(refresh_time):
            print("我们将在 %d  秒后重新爬取数据并进行可视化，我们会自动为您刷新可视化的页面" % t)
            t -= 1
            time.sleep(1)
        print('\n' * 100)
        print("重新开始爬虫并可视化")
