import requests
from lxml import etree
import re
import redis
from multiprocessing import Pool
from pymongo import MongoClient
import time


class JobSpider:
    def __init__(self):
        self.page_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html" \
                        "?lang=c&" \
                        "stype=&" \
                        "postchannel=0000&" \
                        "workyear=99&" \
                        "cotype=99&" \
                        "degreefrom=99&jobterm=99&companysize=99&providesalary=99&" \
                        "lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&" \
                        "dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        self.redis_db = 'jobs_url_from_51job'

    def main(self):
        # 进程池对象,用于开启多进程
        pool = Pool(15)

        job_counts, page_counts = self.get_total_page()
        self.get_multi_page_urls(page_counts, pool)
        pool.close()
        pool.join()

    # 获取总的记录条数
    def get_total_page(self):
        this_url = self.page_url.format(1)
        response = requests.get(this_url)
        response.encoding = 'gbk'
        html_ele = etree.HTML(response.text)

        job_counts_str = html_ele.xpath("//*[@id='resultList']/div[2]/div[4]/text()")[0]
        job_counts = re.search(r"\d+", job_counts_str).group()
        print("总共有%s条职位记录" % job_counts)

        page_counts_str = html_ele.xpath('//*[@id="resultList"]/div[55]/div/div/div/span[1]/text()')[0]
        page_counts = re.search(r"\d+", page_counts_str).group()
        print("总共有%s页" % page_counts)

        return int(job_counts), int(page_counts)

    # 获取每页的html连接并保存
    def get_multi_page_urls(self, page_counts, pool):
        for page in range(page_counts - 1, -1, -1):
            pool.apply_async(self.get_one_page_urls, (page,))

    # 保存一个页面的url
    def get_one_page_urls(self, page):
        this_url = self.page_url.format(page)
        response = requests.get(this_url)
        response.encoding = "gbk"
        html_ele = etree.HTML(response.text)

        urls = html_ele.xpath('//*[@id="resultList"]/div/p/span/a/@href')
        for url in urls:
            self.redis_save(url)
        print(f'第{page}页已完成')

    # 将单条数据存入redis
    def redis_save(self, item):
        client = redis.StrictRedis()
        client.sadd(self.redis_db, item)


class JobDetailSpider:
    mongo_cli = MongoClient()
    database = mongo_cli["Job_detail"]
    collection = database["python_jobs"]

    redis_cli = redis.StrictRedis()
    redis_db = "jobs_url_from_51job"

    def get_one_detail(self, index, start_time):
        url = self.redis_cli.spop(self.redis_db)
        response = requests.get(url)
        response.encoding = 'gbk'
        html_ele = etree.HTML(response.text)

        data = dict()

        data["name"] = html_ele.xpath("/html/body/div//h1/text()")[0]

        tags_list = html_ele.xpath("/html/body//p[@class='msg ltype']/text()")
        tags_list = [tag.replace('\xa0', '') for tag in tags_list]
        print(tags_list)

        data["location"] = tags_list[0]
        data["experience"] = tags_list[1]

        offset = 0
        data["education"] = ""
        if len(tags_list) >= 5:
            offset = 1
            data["education"] = tags_list[2]

        data["nums"] = tags_list[2 + offset]
        data["pub_date"] = tags_list[3 + offset]

        data["salary"] = html_ele.xpath("/html/body//div[@class='cn']/strong/text()")
        if data["salary"]:
            data["salary"] = data["salary"][0]
        else:
            data["salary"] = ""

        data["company"] = html_ele.xpath("/html/body/div//p/a[@class='catn']/text()")[0]
        data["description"] = '\n'.join(html_ele.xpath("/html//div[@class='bmsg job_msg inbox']//text()"))

        self.save_one_detail(data)

        passed_time = time.time() - start_time
        print(f'第{index}条数据存储完成, 经过了{passed_time:.2f}秒')

    def save_one_detail(self, data):
        self.collection.insert(data)

    def main(self):
        total = self.redis_cli.scard(self.redis_db)
        # total = 100
        start_time = time.time()

        pool = Pool(21)
        for i in range(1, total+1):
            pool.apply_async(self.get_one_detail, (i, start_time))

        pool.close()
        pool.join()


if __name__ == '__main__':
    # 获取所有职位的urls
    # jobSpider = JobSpider()
    # jobSpider.main()

    # 获取urls中的详细信息
    jobDetailSpider = JobDetailSpider()

    jobDetailSpider.main()
