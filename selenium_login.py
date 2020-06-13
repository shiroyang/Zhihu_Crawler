"""
杨志朗 1700094803
这个程序用selenium来获取cookies以及模拟登录知乎
首先要在主程序内输入 my_account 以及 my_password , 来模拟登陆知乎一次，获取cookies
cookies 会保存为.json文件， 保存一次就不会再去跑get_cookies了
有时候登陆前要输入验证码或者是逆过来的文字，这里处理起来比较麻烦，直接手动处理，登陆一次
之后就会跑 login_simulation()就可以模拟登录知乎

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as ex
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json  # 用于保存cookies
from random import random  # 用于生成0-1的随机数


class Zhihu:

    def __init__(self):
        url = 'https://www.zhihu.com/'
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    # 检测是否登陆了知乎
    def is_login(self):
        try:
            return bool(
                self.browser.find_element_by_css_selector(".GlobalSideBar-navText")
            )
        except ex.NoSuchElementException:
            return False

    # 用于获取cookies
    def get_cookies(self):
        self.browser.get("https://www.zhihu.com/signin")
        # 这里首先要按账号密码登陆
        self.browser.find_element_by_xpath(
            "//*[@id=\"root\"]/div/main/div/div/div/div[1]/div/form/div[1]/div[2]").click()
        time.sleep(1 + random())
        self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(my_account)
        time.sleep(1 + random())
        self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(my_password)
        time.sleep(1 + random())
        self.browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()

        # 然后会出现验证码的问题，手动处理，登陆进去以后获取cookies
        cnt = 0
        while not self.is_login():
            time.sleep(random())
            cnt += 1
            print("第 %d 次尝试登录知乎" % cnt)

        # 退出上面循环说明已经登陆知乎了,开始获取cookies
        cookies = self.browser.get_cookies()  # Selenium为我们提供了get_cookies来获取登录cookies
        print("已经获取cookies!")
        self.browser.close()
        with open('ZhihuCookies.json', 'w') as f:
            f.write(json.dumps(cookies))

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
        print("成功使用cookies登陆知乎！ 10秒后自动关闭")
        time.sleep(10)
        self.browser.close()


if __name__ == "__main__":

    # 输入你的账号和密码用于获取cookies，还要知道chrome_driver的位置
    my_account = '这是你的账号'
    my_password = '这是你的密码'
    chromedriver_path = "D:/ChromePython/chromedriver.exe"  # 改成你的chromedriver的完整路径地址

    zhihu = Zhihu()  # Zhihu是定义的类

    # 看看当前地址里有没有知乎的cookies文件， 没有就获取cookies， 有就不用了
    file = 'ZhihuCookies.json'
    if file not in os.listdir():
        zhihu.get_cookies()
        zhihu = Zhihu()
    zhihu.login()
