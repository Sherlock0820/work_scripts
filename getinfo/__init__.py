"""async def process(page,page_num):
    'dsj_operate()的子模块，用于批量点击跳转页面'
    try:
        for i in range(1,page_num+1):
            rows=await page.locator('body > app-root > div > div > div > app-customer-task-list > div:nth-child(2) > app-ng-table > nz-table > nz-spin > div > div > nz-table-inner-default > div > table > tbody > tr').all()
            for row in rows:
                choices=await row.locator('td.ant-table-cell').all()
                if choices:
                    choice=choices[-1]
                    entrance=choice.locator('div>a',has_text='办理')
                    async with page.context.expect_page() as new_page_info:
                        await entrance.click()
                    new_page=await new_page_info.value
                    await new_page.wait_for_load_state('domcontentloaded')
                    await page.wait_for_timeout(timeout=5000)
                    '''已经打开了具体操作界面，部署剩余操作……'''
                    await fill_data(new_page=new_page)
                    await new_page.close()
                    await page.wait_for_timeout(timeout=2000)
            # print(f'page {i} ')
            i=i+1
            next_button=page.locator('body > app-root > div > div > div > app-customer-task-list > div:nth-child(2) > app-ng-table > nz-table > nz-spin > div > nz-pagination > li.ant-pagination-next.ng-star-inserted > button')
            is_clickable = await next_button.evaluate(
                'button => !button.disabled && window.getComputedStyle(button).pointerEvents !== "none"')
            if is_clickable:
                await next_button.click()
                await page.wait_for_timeout(timeout=10000)
            else:
                print('last page already')
                break
    except Exception as e:
        print(f'process error: {e}')"""
""" company_type, industry_info, certifications_info = await asyncio.gather(
     qxb_getinfo(qxb_page, company_name=company_name),  # return: 该企业性质 str
     asyncio.to_thread(csv_getinfo, csvpath=csvpath, company=company_name, use_cols=use_cols),
     # return:  返回字典，三对键值对：企业名称、新中大行业类别，业务类型dict
     tj_getinfo(tj_page, company_name=company_name),  # return: 该企业的资质文本列表list
 )"""
