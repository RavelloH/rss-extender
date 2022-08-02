# -*- coding: utf-8 -*-
## Author: RavelloH
### RSS Maker

from xml.dom.minidom import parse
from urllib.request import urlopen
from wget import download
from bs4 import BeautifulSoup as bs
import xml.dom.minidom
import re,os
import linecache

# 替换函数
def alter(file,old_str,new_str):
    lines = ''
    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            lines = lines + line
        if old_str in lines:
            lines = lines.replace(old_str, new_str , 1)
        f2.write(lines)
    os.remove(file)
    os.rename("%s.bak" % file, file)

# 下载原始rss
print('[进程0/6]正在初始化...')
try:
    rsslink = 'https://fetchrss.com/rss/62e7476cbc64503f4d1c8c3262e748042496e12e1401c6e3.xml'
    rsscontext = urlopen(rsslink)
    print('[进程1/6]RSS拉取成功')   
except:
    print('[Error]RSS拉取失败')
    exit()

# 打开原始及本地rss
try:
    OriginRss = xml.dom.minidom.parse(rsscontext)
    getresult = OriginRss.documentElement
    LocalRss = xml.dom.minidom.parse('./rss.xml')
    Localresult = LocalRss.documentElement
    print('[进程2/6]RSS打开成功')
except:
    print('[Error]RSS打开失败')
    exit()
    
# 判断RSS是否有更新
items = getresult.getElementsByTagName("item")
local = Localresult.getElementsByTagName("item")
newpost = items[0]
newtitle = newpost.getElementsByTagName('title')[0]
# 解析本地
localpost = local[0]
localtitle = localpost.getElementsByTagName('title')[0]
newtitlestring = newtitle.childNodes[0].data
localtitlestring = localtitle.childNodes[0].data
if newtitlestring == localtitlestring:
    print('[进程3/6]RSS比对完成:当前已同步，无需继续合并')
    newtimes = getresult.getElementsByTagName('pubDate')[0]
    oldtimes = Localresult.getElementsByTagName('pubDate')[0]
    newtime = newtimes.childNodes[0].data
    oldtime = oldtimes.childNodes[0].data
    alter('rss.xml',str(oldtime),str(newtime))
    print('[进程4已跳过]')
    print('[进程5已跳过]')
    print('[进程6/6]RSS时间更新完成:%s=>%s' %(oldtime,newtime))
    print('[RSS更新完成]')
    exit()
else:
    print('[进程3/6]RSS比对完成:有新项目待更新')
    
# 合并新项目(目前只设计了合并一个)
print('[进程4/6]正在合并新项目...')
filltext = '''
</image>
<item>
'''
filename = download('https://fetchrss.com/rss/62e7476cbc64503f4d1c8c3262e748042496e12e1401c6e3.xml','./originRss.xml')
# 查找对应行
with open(filename, 'r') as file:
    line = file.readline()
    counts = 1
    while line:
        if newtitlestring in line:
            break
        line = file.readline()
        counts += 1
# 创建插入新内容
tofiletext = linecache.getline(filename, counts-1)+linecache.getline(filename, counts)+linecache.getline(filename, counts+1)+linecache.getline(filename, counts+2)+linecache.getline(filename, counts+3)+linecache.getline(filename, counts+4)+linecache.getline(filename, counts+5)
file_name = "./rss.xml"
with open(file_name, 'r') as f:
    lines = f.readlines()
    lines.insert(15,tofiletext)
    s = ''.join(lines)
with open(file_name, 'w') as f:
    f.write(s)
print('\n[进程4/6]新项目已合并')

# 爬取博客内描述 去广告
keyword = '<![CDATA[<br/><br/><span style="font-size:12px; color: gray;">(Feed generated with <a href="https://fetchrss.com" target="_blank">FetchRSS</a>)</span>]]>'
totalline = len(open(file_name,'r').readlines())
needs = []
with open(file_name, 'r') as file:
    line = file.readline()
    counts = 1
    while line:
        if keyword in line:
            needs.append(counts)
        if counts == totalline:
            break
        line = file.readline()
        counts += 1

for j in needs:
    originurl = linecache.getline(file_name, j-1)
    pattern = re.compile(r'[a-zA-z]+://[^\s<]*')
    obj = bs(urlopen(pattern.search(originurl).group()).read(),'html.parser')
    description_info = obj.find_all('p')
    totallen = 0
    nowlen = 0
    for k in description_info:
        totallen += 1
    while True:
        if len(str(description_info[nowlen])) > 70:
            break
        if nowlen > totallen-1:
            break  
        nowlen += 1
    summary = str(description_info[nowlen].get_text(strip=True))
    print('[进程5/6]已获取一篇摘要:%s...' %(summary[:10]))
    alter(file_name,keyword,summary)

# 时间整理
newtimes = getresult.getElementsByTagName('pubDate')[0]
oldtimes = Localresult.getElementsByTagName('pubDate')[0]
newtime = newtimes.childNodes[0].data
oldtime = oldtimes.childNodes[0].data
alter('rss.xml',str(oldtime),str(newtime))
print('[进程6/6]RSS时间更新完成:%s=>%s' %(oldtime,newtime))
print('[RSS更新完成]')
