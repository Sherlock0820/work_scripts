import asyncio
import logging
import sys
from math import ceil

from dsj_getinfo import dsj_getinfo, dsj_login
from excel_getinfo import csv_getinfo
from general_close import close_sites
from general_open import open_sites
from operate import page_fill
from qxb_getinfo import qxb_getinfo
from tj_getinfo import tj_getinfo

"""dsj_login={
        'username': '250065',
        'password': '123456'
        }"""  # 大数据平台登录账号
task_name = '浙江省客户清洗3月13日'  # 任务名
csv_path = r"../config/湖南省名单.csv"  # csv文件路径，记得要实时改
use_cols = ["企业名称", "城市基建", "能源", "交通", "水利", "工业服务", "施工", '设计/EPC']  # 筛选的行业列名
dtypes = {'设计/EPC': 'object', '交通': 'object', '水利': 'object'}  # 列名数据类型，用于声明以便处理数据，要随着use_cols更改键值
"""tj_login={
        'username': '15068822659',
        'password': 'Tj123456'
        }"""  # 探迹平台登录账号
target_num = 15
logging.basicConfig(filename=r"E:\python_codes_learning\ngwork\work_scripts\config\error.log", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")


async def main(target_num):
    """写两个循环。外循环负责当内层循环清洗完一页15条数据时，重新刷新未清洗页面；内循环就负责清洗一页的15条数据"""
    try:
        p, pages, browser = await open_sites()
        dsj_page = pages[0]
        tj_page = pages[1]
        qxb_page = pages[2]
        page_num = ceil(target_num / 15)
        print(1)
        for i in range(1, page_num + 1):
            try:
                wqx_page = await dsj_login(dsj_page, taskname=task_name)
                for j in range(15):
                    try:
                        new_page, company_name = await dsj_getinfo(wqx_page=wqx_page, count=j)
                        qxb_task = asyncio.create_task(qxb_getinfo(qxb_page, company_name=company_name))
                        csv_task = asyncio.create_task(
                            asyncio.to_thread(csv_getinfo, csvpath=csv_path, company_name=company_name,
                                              use_cols=use_cols,
                                              dtypes=dtypes))
                        tj_task = asyncio.create_task(tj_getinfo(tj_page, company_name=company_name))
                        company_type = await qxb_task  # return: 该企业性质 str
                        industry_info = await csv_task  # return:  返回字典，三对键值对：企业名称、新中大行业类别，业务类型dict
                        certifications_info = await tj_task  # return: 该企业的资质文本列表list
                        await page_fill(new_page=new_page, company_type=company_type, industry_info=industry_info,
                                        certifications_info=certifications_info)
                        print(f'data{j}')
                    except Exception as e:
                        logging.error(f"》》company: {company_name if company_name else 'Unknown'} is failed: {e}")
                print(f'》》》》》page{i}')
            except Exception as e:
                logging.error(f"》》》》》page{i} is failed: {e}")
    except Exception as e:
        logging.critical(f"》》》》》》》》main error: {e}")
    finally:
        await close_sites(p=p, pages=pages, browser=browser)


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main(target_num=target_num))
        finally:
            loop.close()
            print("》》》》》》》》has been done")
