import matplotlib.pyplot as plt
from pymongo import MongoClient
import jieba  # 分词库
from collections import Counter  # 词频统计库
import wordcloud  # 词云展示库
from PIL import Image  # 图像处理库

mongo_cli = MongoClient()
database = mongo_cli["Job_detail"]
collection = database["python_jobs"]

mongo_objs = collection.find()

word_count_dic = dict()

skill_set = {'AI', 'ANALYSIS', 'ANDROID', 'BI', 'C#', 'C++', 'CSS', 'DOCKER', 'ETL',
             'GO', 'HADOOP', 'HIVE', 'HTML', 'JAVA', 'JAVASCRIPT', 'LINUX', 'MATLAB', 'MONGODB',
             'MYSQL', 'NGINX', 'ORACLE', 'PERL', 'PHP', 'PYTHON', 'REDIS',
             'SHELL', 'SPRING', 'SPSS', 'SQL', 'WEB', '人工智能', '分布式', '分析',
             '前端开发', '图像', '图像处理', '多线程', '大专', '市场营销', '建模', '挖掘',
             '操作系统', '数学', '数据', '数据仓库', '数据分析', '数据库', '数据挖掘', '服务器',
             '本科', '机器', '机器人', '架构设计', '测试', '测试工具',
             '测试用例', '深度', '游戏', '研究生', '硕士', '算法', '统计', '统计学',
             '网络', '网络安全', '自动化', '视觉', '设计', '调优', '软件测试', '运维',
             '金融', '集群', '项目管理'}


def desc_cut_and_count(desc):
    this_words = jieba.lcut(desc)
    for word in this_words:
        if len(word) > 1 and word.upper() in skill_set:
            word = word.upper()
            if word in word_count_dic:
                word_count_dic[word] += 1
            else:
                word_count_dic[word] = 1


def show_wordcloud(word_count_dic):
    wc = wordcloud.WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
        #     mask=mask, # 设置背景图
        max_words=100,  # 最多显示词数
        max_font_size=80,  # 字体最大值
        scale=3,  # 清晰度
        background_color="lightgray",  # 背景颜色
    )

    wc.generate_from_frequencies(word_count_dic)

    wc.generate_from_frequencies(word_count_dic)
    plt.axis('off')  # 关闭坐标轴
    plt.imshow(wc)  # 显示词云
    wc.to_file('result.jpg')  # 保存结果图片


def main():
    for mongo_obj in mongo_objs:
        desc = mongo_obj["description"]
        desc_cut_and_count(desc)

    result = Counter(word_count_dic).most_common()
    print(result)

    show_wordcloud(word_count_dic)


if __name__ == '__main__':
    main()
