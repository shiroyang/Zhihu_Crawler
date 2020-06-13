"""
杨志朗 1700094803
这个程序用selenium来爬取知乎热榜，保存相关文件到目录下的ZhihuRanking.txt文件里面

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as ex
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import os
import json  # 用于保存cookies
from random import random  # 用于生成0-1的随机数


class Zhihu:

    def __init__(self):
        url = 'https://www.zhihu.com/'
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path="D:/ChromePython/chromedriver.exe", options=options)  # 这里请自行设置chromedriver的位置
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    def login(self):
        print("开始用已获取的cookies模拟登录")

        # 从文件中获取保存的cookies
        with open('ZhihuCookies.json', 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())  # 获取cookies
        # 把获取的cookies处理成dict类型
        cookies_dict = dict()
        for cookie in listcookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']

        self.browser.get("https://www.zhihu.com")
        for item in cookies_dict:
            self.browser.add_cookie({
                "domain": ".zhihu.com",
                "name": item,
                "value": cookies_dict[item],
                "path": '/',
                "expires": None
            })
        self.browser.get("https://www.zhihu.com")
        print("成功使用cookies登陆知乎")

    def crawl(self):
        print("开始爬取知乎热搜榜~\n\n")
        ranking_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div/div['
                                                      '1]/nav/a[3]')))
        ranking_button.click()
        # 等待知乎加载完毕
        time.sleep(1 + random())
        html = self.browser.page_source
        bs = BeautifulSoup(html, 'html.parser')
        ranking_topics = bs.find_all(['h2'], {'class': 'HotItem-title'})  # 这里找出来的topics还有html标签，想办法去除掉
        print(" ------------------------------------------- 分割线 -------------------------------------------------\n\n")
        cnt = 1
        with open('ZhihuRanking.txt', 'w', encoding='utf-8') as f:
            for item in ranking_topics:
                print(str(cnt) + '. ' + item.get_text())
                print(str(cnt) + '. ' + item.get_text(), file=f)
                cnt += 1
        self.browser.close()


if __name__ == "__main__":

    zhihu = Zhihu()  # Zhihu是定义的类

    # 看看当前地址里有没有知乎的cookies文件， 没有就获取cookies， 有就不用了
    zhihu.login()
    zhihu.crawl()
