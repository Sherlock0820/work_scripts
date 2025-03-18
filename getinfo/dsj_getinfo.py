import asyncio

import playwright.async_api

from general_close import close_sites
from general_open import open_sites


async def dsj_login(wqx_page, login: dict = None, taskname: str = None):
    '''
    登录大数据平台，返回筛选好的未清洗页面
    :param wqx_page: 未登录的大数据平台首页
    :param login: 登陆账号和密码
    :param taskname: 待清洗任务名称（如有）
    :return: 筛选好的待清洗页面 playwright.async_api._generated.Page
    '''
    try:
        await wqx_page.locator(
            '#cdk-overlay-1 > nz-modal-confirm-container > div > div > div > div > div.ant-modal-confirm-btns.ng-tns-c32-2 > button > span').click()
        if login == None:
            login = {
                'username': '250065',
                'password': '123456'
            }
        await wqx_page.locator(
            'body > app-root > div > div > div > app-login > div > div.container > div.rightPanel > div > form > nz-form-item:nth-child(1) > nz-form-control > div > div > nz-input-group > input').fill(
            login['username'])
        await wqx_page.locator(
            'body > app-root > div > div > div > app-login > div > div.container > div.rightPanel > div > form > nz-form-item:nth-child(2) > nz-form-control > div > div > nz-input-group > input').fill(
            login['password'])
        await wqx_page.locator(
            'body > app-root > div > div > div > app-login > div > div.container > div.rightPanel > div > form > button > span').click()  # 实现登录,点击确定
        await wqx_page.wait_for_timeout(timeout=1000)
        await wqx_page.locator(
            'body > app-root > div > app-header > div.fixed-head.ng-star-inserted > div > ul > li:nth-child(3) > a').click()  # 跳转到客户清洗列表
        await wqx_page.wait_for_selector(
            'body > app-root > div > div > div > app-customer-task-list > div:nth-child(2) > app-ng-table > nz-table > nz-spin > div > div > nz-table-inner-default > div > table > tbody > tr:nth-child(15) > td:nth-child(7) > span')
        await wqx_page.locator('#f_status > nz-select-top-control').click()
        await wqx_page.locator('#f_status > nz-select-top-control').type('未清洗\n')
        await wqx_page.wait_for_timeout(timeout=8000)
        if taskname is not None:
            await wqx_page.locator('#f_taskName > nz-select-top-control > nz-select-search > input').click()
            await wqx_page.locator('#f_taskName > nz-select-top-control > nz-select-search > input').type(
                taskname + '\n')
        await wqx_page.wait_for_timeout(timeout=1000)
        return wqx_page
    except Exception as e:
        print(f'dsj_login error: {e}')


async def dsj_getinfo(wqx_page, count=1):
    '''
    从大数据平台获取任务相关信息
    :param page: 筛选好的未清洗页面
    :param count:待清洗任务列表的第几条待清洗数据？ int
    :return:单个待操作的页面，公司名 playwright.async_api._generated.Page str
    '''
    try:
        """task_tag='body > app-root > div > div > div > app-customer-task-list > div:nth-child(2) > app-ng-table > nz-table > nz-spin > div > nz-pagination > li.ant-pagination-total-text.ng-star-inserted'
        task_text = await page.locator(task_tag).text_content()
        task_num=int(re.search(r'\d+',task_text).group()) if task_text else 0
        page_num=ceil(task_num/15)
        '''获取了任务数量有关参数'''"""
        row = wqx_page.locator(
            f'body > app-root > div > div > div > app-customer-task-list > div:nth-child(2) > app-ng-table > nz-table > nz-spin > div > div > nz-table-inner-default > div > table > tbody > tr:nth-child({count})')
        choices = await row.locator('td.ant-table-cell').all()
        if choices:
            choice = choices[-1]
            entrance = choice.locator('div>a', has_text='办理')
            async with wqx_page.context.expect_page() as new_page_info:
                await entrance.click()
            new_page = await new_page_info.value
            await new_page.wait_for_load_state('domcontentloaded')
            '''获取单个企业的需操作页面'''
            company_name = await get_name(new_page)
        return new_page, company_name
    except Exception as e:
        print(f'dsj_operate error: {e}')
        return None, None


async def get_name(new_page: playwright.async_api._generated.Page):
    '''
    提取公司名字以获取行业，性质等信息
    :param new_page: 单个待清洗的页面 playwright.async_api._generated.Page
    :return: 公司名字 str
    '''
    try:
        company_name = (await new_page.input_value("#nf_enpName")).strip()
        return company_name
    except Exception as e:
        print(f'get_name error: {e}')
        return None


async def test():
    try:
        p, pages, browser = await open_sites()
        wqx_page = await dsj_login(pages[0], taskname='湖南客户清洗3.10')
        new_page, name = await dsj_getinfo(wqx_page)
        print(type(name))
        print(name)
        page_url = new_page.url
        if "login" in page_url:
            print("Redirected to login page.")
        else:
            print(f"New page is loaded")
        await close_sites(p, pages, browser)
    except Exception as e:
        print(f'test error: {e}')


if __name__ == '__main__':
    asyncio.run(test())
