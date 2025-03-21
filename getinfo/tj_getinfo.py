import asyncio

from general_close import close_sites
from general_open import open_sites


async def tj_getinfo(page, company_name, login=None):
    '''
    从探迹平台获取资质证书的名称列表
    :param page: 函数opensite()中打开的探迹平台首页 playwright.async_api._generated.Page
    :param company_name: 需要查询的企业名，从大数据平台的待清洗列表获取 str
    :return: 该企业的资质文本列表list
    '''
    try:
        if login == None:
            login = {
                'username': '15068822659',
                'password': 'Tj123456'
            }
        await page.locator('#app > div > div._1ukL5 > div._1L2jN > div._1ocgW > div:nth-child(2)').click(timeout=3000)
        await page.locator(
            '#app > div > div._1ukL5 > div.ant-tabs.ant-tabs-top.ant-tabs-line > div.ant-tabs-content.ant-tabs-content-animated.ant-tabs-top-content > div.ant-tabs-tabpane.ant-tabs-tabpane-active > section > form > div:nth-child(1) > div > div > span > span > span > input').fill(
            login['username'])
        await page.locator(
            '#app > div > div._1ukL5 > div.ant-tabs.ant-tabs-top.ant-tabs-line > div.ant-tabs-content.ant-tabs-content-animated.ant-tabs-top-content > div.ant-tabs-tabpane.ant-tabs-tabpane-active > section > form > div:nth-child(2) > div > div > span > span > input').fill(
            login['password'])
        await page.locator(
            '#app > div > div._1ukL5 > div.ant-tabs.ant-tabs-top.ant-tabs-line > div.ant-tabs-content.ant-tabs-content-animated.ant-tabs-top-content > div.ant-tabs-tabpane.ant-tabs-tabpane-active > section > form > div._201kd > label > span.ant-checkbox > input').click(timeout=3000)
        await page.locator(
            '#app > div > div._1ukL5 > div.ant-tabs.ant-tabs-top.ant-tabs-line > div.ant-tabs-content.ant-tabs-content-animated.ant-tabs-top-content > div.ant-tabs-tabpane.ant-tabs-tabpane-active > section > form > div:nth-child(4) > div > div > span > span > button').click(timeout=3000)
        await page.wait_for_timeout(timeout=500)
        await page.locator(
            '#app-content > div._2_xLc > div._1MQTa > div > div > div.d9QSC > div._1_Kp9 > a:nth-child(1)').click(timeout=3000)
        await page.wait_for_timeout(timeout=1000)
        await page.locator('#input_search_id').type(company_name + '\n')
        await page.wait_for_timeout(timeout=2000)
        '''进入经营信息获取资质情况'''
        async with page.context.expect_page() as new_page_info:
            await page.locator(
                '#app-content > div > div > div._1L8tl > div._2LGEv > div._3q8AG > div._3uuyR > div > div > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > section > div._7AsBn._1ccTs > div._2BCLE > h3 > a').click(timeout=3000)
        new_page = await new_page_info.value
        await new_page.wait_for_timeout(timeout=1500)
        await new_page.locator(
            '#___reactour > div:nth-child(3) > div > section > div.GnkN5U6pZoc4jIizt2WK2 > div > button').click(timeout=3000)
        await new_page.locator(
            '#___reactour > div:nth-child(3) > div > section > div.GnkN5U6pZoc4jIizt2WK2 > div:nth-child(3) > button').click(timeout=3000)
        await new_page.locator(
            '#enterprise-details > div._27SC6.Cue1l.IXxa8 > div > div.ScrollbarsCustom-Wrapper > div > div > div._3Soam > div > div.cKi1K > div._1Y9j8 > div > ul > li:nth-child(6) > div').click(timeout=3000)
        await new_page.wait_for_timeout(timeout=3000)
        button = new_page.locator('#enterpriseDetails_anchorTabDomId > div > div > div > label:nth-child(10)')
        if await button.get_attribute('class') != 'ant-radio-button-wrapper':
            print('no certification')
            return None
        else:
            await button.click(timeout=3000)
            '''开始获取资质证书名称'''
            certifications = await new_page.locator(
                '#enterprise-detail-certificates > div:nth-child(5) > div.ant-table-wrapper._2eOit.t6Dbk > div > div > div > div > div > table > tbody > tr').all()
            await new_page.wait_for_timeout(timeout=3000)
            names = []
            for certification in certifications:
                name_locator = certification.locator('td:nth-child(4) > div > div:nth-child(1) > span:nth-child(1)')
                if await name_locator.count() > 0:
                    name = await name_locator.text_content()
                else:
                    name = await certification.locator('td:nth-child(4)').text_content()
                names.append(name)
            final_certifications = [name for name in names if name != '--']
            return final_certifications
    except Exception as e:
        print(f'tj_operate error: {e}')
        return None


async def test():
    '测试函数'
    try:
        p, pages, browser = await open_sites()
        certification = await tj_getinfo(pages[0], company_name='湖南广宇建设股份有限公司')
        print(certification)
        await close_sites(p, pages, browser)
    except Exception as e:
        print(f'test error: {e}')


if __name__ == '__main__':
    asyncio.run(test())
