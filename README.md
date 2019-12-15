# 前程无忧python岗位信息爬取和分析

### 项目简介

- 爬取12月14日所有前程无忧中的python岗位信息, 共33751条数据
- 分析python岗位的以下情况:
  1. 各个城市的岗位数量分布
  2. 不同学历要求下的岗位数量分布
  3. 工作经验年限与工资的关系
  4. 城市与工资的关系
  5. 岗位要求的技能关键词的词频

### 项目内容

1. 各城市的岗位数量分布

   ![img](D:\git\爬虫\project\51job\images\地区职位数量分布图.png)

   2. 不同学历要求下的岗位数量分布

      - 有一些岗位没有学历要求, 所以只有28000多条数据

      ![img](D:\git\爬虫\project\51job\images\学历职位数量分布图.jpg)

      3. 工作经验年限与工资的关系
         - 所有的单位全部换算成了(元/月)
         - 岗位的工资一般都是一个区间, 在该次分析中都是使用工资区间的下限*1.2来计算的, 我认为这样可以较为准确的反应出岗位的实际工资
         - 使用箱型图可以比较好的忽略异常值, 反应出大体的工资情况

      ![img](D:\git\爬虫\project\51job\images\工作经验与工资箱型图.jpg)

      4. 城市与工资的关系
         - 为了方便展示, 只统计了岗位最多的8个城市

      ![img](D:\git\爬虫\project\51job\images\城市与工资箱型图.jpg)

      5. 岗位要求的技能关键词的词云

      ![img](D:\git\爬虫\project\51job\images\python技能词云图.jpg)

      - 词频统计如下, 大家可以观察一下哪些技能关键词是python岗位被提及较多的

        ![img](D:\git\爬虫\project\51job\images\词频表.png)

      

### 使用的库

爬虫部分: 

- requests: 用于请求url

- redis: 可以使用python连接redis, 用于临时存储url

- pymongo: 可以使用python连接mongodb, 存储爬下来的数据
- lxml: 主要使用其中的xpath相关模块, 用于解析html
- multiprocessing:  内置库, 用于开启线程池, 加快爬取速度

作图部分: 

- matplotlib: 用于作图
- jieba: 用于中文分词
- collections: 内置库, 用于统计词频
- wordcloud: 用于生成词云图片
- PIL: 用于图像处理