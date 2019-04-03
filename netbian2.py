#coding=utf-8
import urllib.request
import re
import os
import urllib
import time
#根据给定的网址来获取网页详细信息，得到的html就是网页的源代码
headers = ("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
opener = urllib.request.build_opener()
opener.addheaders = [headers]

def getHtml(url):
    page = opener.open(url)
    html = page.read()
    return html.decode('GBK')


def getImg(html,count):
    reg = r'/desk/.+?\.htm'
    pagezz = re.compile(reg) #转换成一个正则对象
    imgpagelist = pagezz.findall(html) #表示在整个网页中过滤出所有图片的地址，放在imglist中
    path = 'F:\\jpg\\花卉' #设置保存地址
    x=0
    if not os.path.isdir(path):
        os.makedirs(path) # 将图片保存到H:..\\test文件夹中，如果没有test文件夹则创建
    paths = path+'\\' #保存在test路径下
    #print(html)
    for pageurl in imgpagelist:
        a=r'class=\"pic\"[\d\D]+?class=\"pic\-down\"'
        reg = r'http://img\.netbian\.com/file/.+?\.jpg'
        imgzz = re.compile(reg)  # 转换成一个正则对象
        imghtml=getHtml("http://www.netbian.com"+pageurl)
        lizz=re.compile(a)
        li=lizz.findall(imghtml)
        #print(imghtml)
        for l in li:
            imglist = imgzz.findall(l)  # 表示在整个网页中过滤出所有图片的地址，放在imglist中
            #print(l)
            for imgurl in imglist:
                #print(imgurl)
                #urllib.request.urlretrieve(imgurl,'{0}{1}-{2}.jpg'.format(paths,count,x)) #会被反爬虫
                while(True):
                    tempcount=0
                    try:
                        data = opener.open(imgurl, timeout=2)
                        with open('{0}{1}-{2}.jpg'.format(paths, count, x), 'wb') as f:
                            # print('{0}{1}-{2}.jpg'.format(paths,count,x))
                            print('第' + str(x) + '张下载完成')
                            f.write(data.read())
                            f.close()
                        break
                    except:
                        tempcount+=1
                        if tempcount>5 :
                            break
                        continue;
                x = x + 1
    print('第'+str(count)+'页下载完成')


html = getHtml("http://www.netbian.com/huahui/index.htm")  # 获取该网址网页详细信息，html就是网页的源代码
getImg(html,1) #从网页源代码中分析并下载保存图片
for i in range(10,55):
    html = getHtml("http://www.netbian.com/huahui/index_" + str(i) + ".htm")  # 获取该网址网页详细信息，html就是网页的源代码
    getImg(html,i) #从网页源代码中分析并下载保存图片
