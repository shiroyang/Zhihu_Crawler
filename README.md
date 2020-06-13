# 知乎热榜爬虫+可视化 **使用说明**



## 1.Requirements:

打开文件夹， 在地址栏输入 %comspec% 并按回车

![image-20200613122022518](https://user-images.githubusercontent.com/60550888/84560905-9bd0f700-ad7a-11ea-97df-b1fdab857edc.png)



这样可以在当前目录下打开cmd

![image-20200613122113348](https://user-images.githubusercontent.com/60550888/84560912-b99e5c00-ad7a-11ea-81a1-ceb35c124324.png)



命令行输入`pip install -r requirements.txt`  并回车，安装所需要的库

![image-20200613123008622](https://user-images.githubusercontent.com/60550888/84560929-ed798180-ad7a-11ea-89c5-ab60efcf118f.png)




之后打开 **zhihu_crawler.py**, 将webdriver设置成自己的绝对地址，并保存

![image-20200613123234436](https://user-images.githubusercontent.com/60550888/84560942-113cc780-ad7b-11ea-9b67-11e76e6f3331.png)




然后打开**selenium_login.py**, 进行同样的操作，并输入你的知乎的账号和密码，并保存

![image-20200613123427592](https://user-images.githubusercontent.com/60550888/84560954-26b1f180-ad7b-11ea-9f7c-5d1afffe7890.png)




最后打开 **main.py** , 进行同样的操作，并保存


![image-20200613123719542](https://user-images.githubusercontent.com/60550888/84560970-3f220c00-ad7b-11ea-9957-ebdafafaabc6.png)





接下来开始运行程序，如果已经在目录下有 **ZhihuCookies.json** 的 cookies文件，请跳到第三步， 若没有则从第二步开始





## 2. 获得cookies并用cookies模拟登录知乎



在命令行输入`python selenium_login.py`并回车

![image-20200613124123684](https://user-images.githubusercontent.com/60550888/84560992-64af1580-ad7b-11ea-8406-ff3a77a51cc7.png)


由于这里没有处理验证码的情况，所以出现验证码时请手动输入

![image-20200613124624904](https://user-images.githubusercontent.com/60550888/84561000-7db7c680-ad7b-11ea-9fa8-6b01a0d07a4d.png)


这个时候程序会自动挂起，所以不需要担心超时问题

![image-20200613124701462](https://user-images.githubusercontent.com/60550888/84561011-9627e100-ad7b-11ea-9127-7230c170f055.png)




登陆成功以后，程序会保存cookies并自动退出，然后就用cookies实现模拟登陆知乎，开启网页10秒钟

![image-20200613125227404](https://user-images.githubusercontent.com/60550888/84561022-a770ed80-ad7b-11ea-8526-50d35d6b693d.png)






## 3. 爬虫及可视化

继续在命令行输入 `python main.py` 并回车

![image-20200613125540208](https://user-images.githubusercontent.com/60550888/84561038-c40d2580-ad7b-11ea-92ed-8016b2800cb1.png)


该文件会首先打开知乎网站并从热搜里面爬取前五十名的信息

![image-20200613125752185](https://user-images.githubusercontent.com/60550888/84561050-dbe4a980-ad7b-11ea-862a-9eb294b52b57.png)




爬取的内容会放在当前目录下的 **ZhihuRanking.txt** 当中

只后会进行两次可视化，第一次是普通的可视化

![image-20200613130302507](https://user-images.githubusercontent.com/60550888/84561064-f61e8780-ad7b-11ea-88f5-28f9a6d2a117.png)




之后程序会根据自定义的关键词对热搜榜中进行匹配，将含有关键词的热搜内容提出来
![image-20200613131342921](https://user-images.githubusercontent.com/60550888/84561088-0d5d7500-ad7c-11ea-8b82-857a5b4abea7.png)




并重新进行可视化，并用推特的推送声进行系统提示
![image-20200613130235800](https://user-images.githubusercontent.com/60550888/84561100-26662600-ad7c-11ea-9297-fc4a95f20ca9.png)




这两个可视化的结果都放在当前目录下的 **知乎热搜实时排名.html** 里面



## 4.自定义部分

当前目录下 **./csv_data/config.csv** 和 **./csv_data/keywords.csv**是可以自定义的部分

**config.csv** 中可以自己定义热搜榜的刷新时间，并重新进行可视化操作，修改后保存

![image-20200613131022344](https://user-images.githubusercontent.com/60550888/84561104-37af3280-ad7c-11ea-9c35-adb585b1d7c6.png)


**keywords.csv** 中可以定义热搜榜的关键词

![image-20200613131218579](https://user-images.githubusercontent.com/60550888/84561106-41389a80-ad7c-11ea-963e-c7542ea62771.png)


