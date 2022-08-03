# RSS
[![update](https://github.com/RavelloH/RSS/actions/workflows/main.yml/badge.svg)](https://github.com/RavelloH/RSS/actions/workflows/main.yml)  
基于fetchrss.com的RSS爬虫，可实现深度爬取文章摘要、突破fetchrss只生成最近五篇文章、去除原来存在于原始RSS中的广告等功能

## 功能
- [x] 将fetchrss中原有的广告替换为文章内摘要  
- [x] 自动同步RSS并更新日期  
- [x] 自动构筑github page以生成以github.io为域名的RSS  

## 使用
1.前往fetchrss.com，为你的博客创建一个免费rss(仅需包含标题与链接，其他随意(若已有摘要，此项目将不会去广告))  
2.复制生成的rss的xml地址  
3.Fork此仓库，修改其中的以下内容:  
  - 删除`originRss.xml`和`rss.xml`
  - 将`main.py`中的第29行的原始rss链接替换为你自己的
  - 将`.github/workflows/main.yml`中第47行、48行替换为你的用户名和邮箱(需与Github账号相对应)，或填写github action的(用户名github-action，邮箱action@github.com)
  - 转到你的仓库的Actions页面，开启Actions  
  
4.star你的仓库，它会自动进行初始化操作

经过第一次action即代表构筑完成，可以通过访问https://[你的用户名].github.io/[你的仓库名]/rss.xml来访问处理后的xml
