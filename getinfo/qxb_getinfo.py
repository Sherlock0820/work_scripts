import asyncio

from general_close import close_sites
from general_open import open_sites

'''还可能会有验证码，添加一段捕捉交互代码'''


async def qxb_getinfo(page, company_name):
    '''
    从企信宝平台获取企业性质
    :param page: 函数opensite()中打开的企信宝平台首页 playwright.async_api._generated.Page
    :param company_name: 需要查询的企业名，从大数据平台的待清洗列表获取 str
    :return: 该企业性质 str
    '''
    try:
        await page.locator(
            '#universal-head > div.w-100.p-relative > div > div.d-inline-flex.align-items-center.m-l-30.line-height-1 > div').click()  # 登录
        login = {
            'user': '18470754656',
            'password': '20040820Hw'
        }
        await page.locator(
            'body > div.z-modal.fade-in > div.slide-down-in > div > div > div.p-h-50 > div.d-flex.justify-content-around.f-16.m-t-70 > div:nth-child(2)').click()
        await page.locator(
            'body > div.z-modal.fade-in > div.slide-down-in > div > div > div.p-h-50 > div.b-radius-4.m-t-30.b-gray-4 > div > div > div.ant-input-number > div.ant-input-number-input-wrap > input').fill(
            login['user'])
        await page.locator(
            'body > div.z-modal.fade-in > div.slide-down-in > div > div > div.p-h-50 > div.d-block.p-12.m-t-20.b-radius-4.p-relative.b-gray-4 > input').fill(
            login['password'])
        await page.locator(
            'body > div.z-modal.fade-in > div.slide-down-in > div > div > div.p-h-50 > label > span.ant-checkbox > input').click()
        await page.wait_for_timeout(timeout=5000)
        await page.locator(
            'body > div.z-modal.fade-in > div.slide-down-in > div > div > div.p-h-50 > div.button.middle.main.m-t-32.w-100.h-48').click()
        print('Complete the verification code to log in->')
        await page.locator(
            '#__nuxt > div > div.z-fixed.p-fixed.left-0.right-0.top-0.bottom-0.d-flex.flex-center > div.p-relative > img.d-block.m-h-auto.cursor-pointer').click(
            timeout=600000)
        await page.wait_for_timeout(timeout=2000)
        print('qxb has login')
        await page.locator(
            '#__nuxt > div > div:nth-child(1) > div.p-b-50.bg-cover.head-bg > div.container > div > div:nth-child(2) > div.focus-visible.p-relative.d-flex.flex-grow-1 > input').type(
            company_name + '\n')
        '加个验证码的分支捕捉程序'
        await page.wait_for_timeout(timeout=2000)  # 这里可能有验证码
        spans = await page.locator(
            '#content > div:nth-child(2) > div.col-2.m-l-20.flex-grow-1.p-relative > div.col-2-1 > div.d-flex.justify-content-between > div.flex-grow-1 > div.m-t-8.m-b--6 > span').all()
        spans_text = [await span.text_content() for span in spans]
        # for span in spans_text:
        #     print(span)
        if '国有企业' not in spans_text:
            company_type = '民企'
        else:
            company_type = '国企'
        return company_type
    except Exception as e:
        print(f'qxb_operate error: {e}')
        return '民企'


async def test():
    '测试函数'
    try:
        p, pages, browser = await open_sites()
        type = await qxb_getinfo(page=pages[0], company_name='中铁十九局')
        print(type)
        await close_sites(p, pages, browser)
    except Exception as e:
        print(f'test error: {e}')


if __name__ == '__main__':
    asyncio.run(test())
