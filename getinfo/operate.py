"""这是一个临时使用的operate工作脚本，主要作用是定义操作，精确的工作脚本在main文件里"""
import asyncio
import random as rnd
import re

import playwright.async_api

from dsj_getinfo import dsj_getinfo, dsj_login
from general_open import open_sites


async def page_fill(new_page: playwright.async_api._generated.Page, company_type: str = '民企',
                    industry_info: dict = {},
                    certifications_info: list = []):
    '''
    完成清洗操作！操作完后关闭new_page
    :param new_page: 单个待清洗的页面 playwright.async_api._generated.Page
    :param company_type: 企业性质 str
    :param industry_info: 业务类型及新中大行业类别 dict
    :param certifications_info: 承包及设计资质 list
    :return: 不返回，关闭这个已清洗页面new_page
    '''
    try:
        amount = await new_page.eval_on_selector("#nf_registerCapital", "el => el.value")
        if amount.strip() != "":
            amount_value = float(re.sub(r'[^\d.]', '', amount))
            if amount_value < 10000:
                amount_in_wan = f"{amount_value} 万元"
            else:
                amount_in_wan = f"{amount_value / 10000} 万元"
            await new_page.locator("#nf_registerCapital").click()
            await new_page.locator("#nf_registerCapital").fill(" ")
            await new_page.locator("#nf_registerCapital").type(amount_in_wan)
        '''转化注册资本单位为万元'''
        xz_flag = new_page.locator('#nf_markEnpNatureNew > nz-select-top-control')
        xz_tag = await xz_flag.locator('nz-select-item[title]').count() <= 0
        if xz_tag:
            await new_page.locator('#nf_markEnpNatureNew').click()
            await new_page.locator('#nf_markEnpNatureNew').type(company_type + '\n')
            await new_page.wait_for_timeout(timeout=1000)
        '''上面输入企业性质'''
        hy_type, yw_type = industry_get(industry_info)
        yw_flag = new_page.locator('#nf_serviceType > div')
        yw_tag = await yw_flag.locator('nz-select-item[title]').count() <= 0
        if yw_tag:
            await new_page.locator('#nf_serviceType').click()
            await new_page.wait_for_timeout(timeout=1000)
            yw_xpath = f"//nz-tree-node-title[@title='{yw_type}']"
            yw_select = new_page.locator(yw_xpath)
            yw_node = yw_select.locator("xpath=ancestor::nz-tree-node")
            await yw_node.locator("nz-tree-node-checkbox").click()
            await new_page.wait_for_timeout(timeout=1000)
        '''上面选择业务类型选项卡'''
        hy_flag = new_page.locator('#nf_industryCategory')
        hy_tag = await hy_flag.locator("nz-select-item[title]").count() <= 0
        if hy_tag:
            await new_page.locator('#nf_industryCategory > div > nz-select-search > input').click()
            await new_page.wait_for_timeout(timeout=1000)
            await new_page.locator('#nf_industryCategory > div > nz-select-search > input').type(hy_type + '\n')
            await new_page.wait_for_timeout(timeout=1000)
            hy_xpath = f"//nz-tree-node-title[@title='{hy_type}']"
            hy_select = new_page.locator(hy_xpath)
            hy_node = hy_select.locator("xpath=ancestor::nz-tree-node")
            await hy_node.locator("nz-tree-node-checkbox").click()
            await new_page.wait_for_timeout(timeout=1000)
        '''上面选择新中大行业类别选项卡'''
        zcb, zycb = certifications_get(certifications_info)
        zcb_flag = new_page.locator('#nf_generalContractingQualification > nz-select-top-control')
        zcb_tag = await zcb_flag.locator('nz-select-item[title]').count() <= 0
        if zcb_tag:
            await new_page.locator("#nf_generalContractingQualification > nz-select-top-control").click()
            await new_page.locator("#nf_generalContractingQualification > nz-select-top-control").type(zcb + '\n')
            await new_page.wait_for_timeout(timeout=1000)
        '''上面输入总承包资质'''
        zycb_flag = new_page.locator('#nf_professionalContractingQualification > nz-select-top-control')
        zycb_tag = await zycb_flag.locator('nz-select-item[title]').count() <= 0
        if zycb_tag:
            await new_page.locator(
                "#nf_professionalContractingQualification > nz-select-top-control > nz-select-search > input").click()
            await new_page.locator(
                "#nf_professionalContractingQualification > nz-select-top-control > nz-select-search > input").type(
                zycb + '\n')
            await new_page.wait_for_timeout(timeout=1000)
        '''上面输入专业承包资质'''
        await new_page.wait_for_timeout(timeout=1000)
        confirm_button = new_page.locator(
            'body > app-root > div > div > div > app-customer-task-detail > div > app-pick-pool > div:nth-child(3) > button')
        await new_page.keyboard.press("PageDown")
        await new_page.wait_for_selector(
            'body > app-root > div > div > div > app-customer-task-detail > div > app-pick-pool > div:nth-child(3) > button',
            timeout=3000)
        await confirm_button.click()
        await new_page.wait_for_selector("button:has-text('确定')", timeout=2000)
        await new_page.locator("button:has-text('确定')").click(timeout=10000)
        await new_page.wait_for_timeout(timeout=2000)
        await new_page.close()
        '''上面找到清洗完成按钮并保存关闭操作页面'''
    except Exception as e:
        print(f'page_fill error:{e}')


def industry_get(info_dict: dict = None):
    '''获取业务类型和新中大行业类别，返回字符串str'''
    try:
        hys = ['传统施工', '电力', '水利工程', '传统施工', '环境治理', '工业服务', '公路', '传统施工', ]
        yws = ['施工', '设计', '施工', '施工', '运营', '施工', '规划', '施工', ]
        hy_type = info_dict.get('新中大行业类别', hys[rnd.randint(0, len(hys) - 1)])
        yw_type = info_dict.get('业务类型', yws[rnd.randint(0, len(yws) - 1)])
        return hy_type, yw_type
    except Exception as e:
        print(f'industry_get error:{e}')


def certifications_get(certifications_info: list = None):
    '''获取总承包、专业承包、工程设计资质（如有）'''
    try:
        zcbs = [
            "市政公用工程施工总承包二级", "市政公用工程施工总承包三级", "建筑工程施工总承包三级",
            "建筑工程施工总承包二级", "机电工程施工总承包二级", "水利水电工程施工总承包二级", "建筑工程施工总承包特级",
        ]
        zycbs = [
            "建筑装修装饰工程专业承包一级", "建筑装修装饰工程专业承包二级", "建筑机电安装工程专业承包一级",
            "建筑机电安装工程专业承包二级", "水利水电机电安装工程专业承包一级", "建筑幕墙工程专业承包二级",
            "建筑幕墙工程专业承包一级",
        ]
        zcb = zcbs[rnd.randint(0, len(zcbs) - 1)]
        zycb = zycbs[rnd.randint(0, len(zycbs) - 1)]
        for certification in certifications_info:
            if '总承包' in certification:
                zcb = certification
                break
        for certification in certifications_info:
            if '专业承包' in certification:
                zycb = certification
                break
        return zcb, zycb
    except Exception as e:
        print(f'certifications_get error:{e}')


async def test():
    '''测试函数'''
    try:
        p, pages, browser = await open_sites()
        wqx_page = await dsj_login(pages[0], taskname='湖南省客户清洗3月19日')  # 改成了无头模式，记得改回来
        new_page, name = await dsj_getinfo(wqx_page)
        await page_fill(new_page)
        await pages[0].wait_for_timeout(timeout=1000)
        await pages[0].close()
        await browser.close()
        await p.stop()
    except Exception as e:
        print(f'test error:{e}')


if __name__ == '__main__':
    for i in range(6):
        asyncio.run(test())
        print(i)
