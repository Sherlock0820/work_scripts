import asyncio

from general_open import open_sites


async def close_sites(p, pages, browser):
    '关闭所有页面'
    try:
        await asyncio.gather(
            pages[0].wait_for_event('close', timeout=18000000),  # 大数据平台
            # pages[1].wait_for_event('close', timeout=18000000),    #探迹
            # pages[0].wait_for_event('close', timeout=18000000)      #企信宝,索引记得改回来
        )
        await browser.close()
        await p.stop()
    except Exception as e:
        print(f'close_sites error: {e}')


async def test():
    '测试函数'
    try:
        p, pages, browser = await open_sites()
        await close_sites(p, pages, browser)
    except Exception as e:
        print(f'test error: {e}')


if __name__ == '__main__':
    asyncio.run(test())
