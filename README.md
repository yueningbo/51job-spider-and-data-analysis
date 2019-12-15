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

   ![img](https://github.com/397460848/51job-spider-and-data-analysis/blob/master/images/%E5%9C%B0%E5%8C%BA%E8%81%8C%E4%BD%8D%E6%95%B0%E9%87%8F%E5%88%86%E5%B8%83%E5%9B%BE.png)

   2. 不同学历要求下的岗位数量分布

      - 有一些岗位没有学历要求, 所以只有28000多条数据

      ![img](https://github.com/397460848/51job-spider-and-data-analysis/blob/master/images/%E5%AD%A6%E5%8E%86%E8%81%8C%E4%BD%8D%E6%95%B0%E9%87%8F%E5%88%86%E5%B8%83%E5%9B%BE.jpg)

      3. 工作经验年限与工资的关系
         - 所有的单位全部换算成了(元/月)
         - 岗位的工资一般都是一个区间, 在该次分析中都是使用工资区间的下限*1.2来计算的, 我认为这样可以较为准确的反应出岗位的实际工资
         - 使用箱型图可以比较好的忽略异常值, 反应出大体的工资情况

      ![img](https://github.com/397460848/51job-spider-and-data-analysis/blob/master/images/%E5%B7%A5%E4%BD%9C%E7%BB%8F%E9%AA%8C%E4%B8%8E%E5%B7%A5%E8%B5%84%E7%AE%B1%E5%9E%8B%E5%9B%BE.jpg)

      4. 城市与工资的关系
         - 为了方便展示, 只统计了岗位最多的8个城市

      ![img](https://github.com/397460848/51job-spider-and-data-analysis/blob/master/images/%E5%9F%8E%E5%B8%82%E4%B8%8E%E5%B7%A5%E8%B5%84%E7%AE%B1%E5%9E%8B%E5%9B%BE.jpg)

      5. 岗位要求的技能关键词的词云

      ![img](https://github.com/397460848/51job-spider-and-data-analysis/blob/master/images/python%E6%8A%80%E8%83%BD%E8%AF%8D%E4%BA%91%E5%9B%BE.jpg)

      - 词频统计如下, 大家可以观察一下哪些技能关键词是python岗位被提及较多的

        ![img](https://github.com/397460848/51job-spider-and-data-analysis/blob/master/images/%E8%AF%8D%E9%A2%91%E8%A1%A8.png)

      

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
