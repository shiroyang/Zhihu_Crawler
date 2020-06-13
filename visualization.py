"""
杨志朗 1700094803
用pyecharts 实现可视化
存在一个问题就是热榜的话太长了，无法正常显示，我决定先用jieba库把关键词图取出来再进行可视化
但是我最后还是决定用漏斗图微调一下，勉强把热搜的字都放到了漏斗图里面，也就不用关键词了
存在的问题是50个热搜实在是太多了，勉强放上来字就很小了，有一个老花镜就没事了（逃

为了加大出现关键词的排面我又设计了一个 customized_visualization(), 大致都和visualization()功能是一样的，
该函数相比visualization()多了一个参数，是一个列表，列表里面是出现了含有关键词的那句话在50句话里面的具体位置
然后把出现关键字的那行的权值都设成最大， 这样含有关键词的那些数据都会到最上面一行中。
"""

from pyecharts.charts import Funnel
from pyecharts import options as opts
from pyecharts.globals import ThemeType
# from jieba.analyse import *
import os
import time


def visualization():
    latest_time = os.path.getmtime("ZhihuRanking.txt")  # 这个是Unix时间，需要转换为人类的时间
    latest_time = time.localtime(latest_time)
    latest_time = time.strftime("%Y-%m-%d %H:%M:%S", latest_time)
    latest_time = str(latest_time)
    #  print(latest_time)
    size_list = []  # 这个用来决定每个热度的大小
    ranking_list = []  # 这个是把话题写进去
    ranking_key_list = []  # 这里是对热榜中的每一条热搜中抽取4个关键词，构成新的热搜
    ini = 200
    for i in range(50):
        ini = int(ini * 0.9) + 2
        size_list.append(ini)
    #  print(size_list)
    with open("ZhihuRanking.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[4:].strip('\n')  # 这里要注意把空格吃掉
            ranking_list.append(line)
            # new_word = ''
            # for keyword, weight in extract_tags(line, topK=4, withWeight=True):
            #     new_word += keyword + ' '
            # ranking_key_list.append(new_word)

    #  print(ranking_list)
    #  print(ranking_key_list)
    #  下面开始制作图表
    c = (
        Funnel(init_opts=opts.InitOpts(width="2048px", height="1080px"))
        .add("热搜关键词", [list(z) for z in zip(ranking_list, size_list)], label_opts=opts.LabelOpts(position="top"),
             gap=1, tooltip_opts=opts.TooltipOpts(), sort_='none')
        .set_global_opts(title_opts=opts.TitleOpts(title="知乎热榜实时排名  更新于 " + latest_time),
                         legend_opts=opts.LegendOpts(type_='scroll', orient='vertical', pos_left='0%', pos_top='20%'),
                         tooltip_opts=opts.TooltipOpts(is_show=True))
        .render("知乎热榜实时排名.html")
    )


def customized_visualization(key_list):
    latest_time = os.path.getmtime("ZhihuRanking.txt")  # 这个是Unix时间，需要转换为人类的时间
    latest_time = time.localtime(latest_time)
    latest_time = time.strftime("%Y-%m-%d %H:%M:%S", latest_time)
    latest_time = str(latest_time)
    size_list = []  # 这个用来决定每个热度的大小
    ranking_list = []  # 这个是把话题写进去
    ini = 200
    for i in range(50):
        ini = int(ini * 0.9) + 2
        size_list.append(ini)

    list_len = len(key_list)
    for i in range(list_len):
        size_list[key_list[i] - 1] = 350

    with open("ZhihuRanking.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[4:].strip('\n')  # 这里要注意把空格吃掉
            ranking_list.append(line)

    c = (
        Funnel(init_opts=opts.InitOpts(width="2048px", height="1080px"))
        .add("热搜关键词", [list(z) for z in zip(ranking_list, size_list)], label_opts=opts.LabelOpts(position="top"),
             gap=1, tooltip_opts=opts.TooltipOpts())
        .set_global_opts(title_opts=opts.TitleOpts(title="知乎热榜+关键词自定义排名  更新于 " + latest_time),
                         legend_opts=opts.LegendOpts(type_='scroll', orient='vertical', pos_left='0%', pos_top='20%'),
                         tooltip_opts=opts.TooltipOpts(is_show=True))
        .render("知乎热榜实时排名.html")
    )


if __name__ == "__main__":
    visualization()
