import asyncio

from playwright.async_api import async_playwright


async def check_page(page, tag):
    '''作为open_site()的子模块，用于网页登陆后稳定性检查'''
    try:
        await page.wait_for_selector(tag, timeout=30000)
    except Exception as e:
        print(f'check_page error: {e}')
    return None


async def open_site(browser, url, tag):
    try:
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        # await check_page(page, tag)
        # print(f'open: {url}')
        return page
    except Exception as e:
        print(f'open_site error: {e}')
        return None


async def open_sites():
    try:
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=True)
        urls = [
            'https://k8s.ns820.com/marketTask/#/customerList',  # 大数据平台
            'https://sales.tungee.com/home',  # 探迹
            'https://www.qixin.com/'  # 企信宝
        ]
        tags = {
            '大数据': "text=黄炜 ",
            '探迹': "#usedBySidebarInBasicformation > div:nth-child(1) > div._2m49szG9dkP4vX9a77sEAf > ul > li:nth-child(14) > div > div",
            '企信宝': "#universal-head > div.z-fixed.p-fixed.left-0.b-b-gray-3.w-100vw.p-relative > div > div.d-inline-flex.align-items-center.m-l-30.line-height-1 > div > div.overflow-hidden.d-inline-flex.justify-content-center.align-items-center.p-relative.f-16.line-height-1.bg-white.b-radius-4.cursor-pointer > div > img",
        }  # 页面长时间运行后检查是否稳定的标签
        '打开所有网页'
        pages = await asyncio.gather(
            open_site(browser, urls[0], tags['大数据']),
            # open_site(browser,urls[1],tags['探迹']),
            # open_site(browser,urls[2],tags['企信宝'])
        )
        pages = [page for page in pages if page is not None]
        return p, pages, browser
    except Exception as e:
        print(f'open_sites error: {e}')
        return None, None, None


async def test():
    '''主函数，用于测试'''
    try:
        p, pages, browser = await open_sites()
        print(f"成功打开的页面数量: {len(pages)}")
        await pages[0].wait_for_event('close', timeout=30000)
        await browser.close()
        await p.stop()
    except Exception as e:
        print(f'test error: {e}')


if __name__ == '__main__':
    asyncio.run(test())
