import matplotlib.pyplot as plt
from pymongo import MongoClient

mongo_cli = MongoClient()
database = mongo_cli["Job_detail"]
collection = database["python_jobs"]

aggs = [
    {"$match": {}},
    {"$sort": {"职位数": -1}},
    {"$group": {"_id": "$experience", "职位数": {"$sum": 1}}}
]

res = collection.aggregate(aggs)

dic = {}
for i in res:
    key = i['_id']
    if key in dic:
        dic[key] += i['职位数']
    else:
        dic[key] = i['职位数']

list_dic = list(dic.items())
list_dic = sorted(list_dic, key=lambda x: x[1], reverse=True)

experience_list = [x[0] for x in list_dic]
count_list = [x[1] for x in list_dic]

# plt.axes(aspect=2)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['font.size'] = 20
plt.figure(figsize=(25, 35))
plt.pie(x=count_list, labels=experience_list, autopct='%3.1f %%')
plt.title("工作经验职位数量分布图")
# plt.legend() # 图例

table_vals = list(zip(experience_list, count_list))
the_table = plt.table(cellText=table_vals, colWidths=[0.1, 0.05], loc='best')
the_table.set_fontsize(23)
the_table.scale(1, 3)

plt.savefig(r"C:\Users\81421\Desktop\python资料\数据分析\51job分析报告\工作经验职位数量分布图.jpg")
plt.show()

dic_exp = dict()

res = collection.find({"experience": "无工作经验"})
