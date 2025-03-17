from typing import Any

import dask.dataframe as dd


def csv_getinfo(csvpath: str, company_name: str, use_cols: list = None, dtypes: dict = None) -> dict[str, Any] | None:
    '''
    从csv文件里获取单个企业的行业相关信息
    :param csvpath: 行业信息.csv路径 str
    :param company_name: 企业名 str
    :param use_cols:筛选需要用到的列名字符串列表  list
    :param dtypes: 列名数据类型，用于声明以便处理数据
    :return:  返回字典，三对键值对：企业名称、新中大行业类别，业务类型dict
    '''
    try:
        if use_cols is None:
            use_cols = ["企业名称", "城市基建", "能源", "交通", "水利", "工业服务", "施工", '设计', 'EPC']
            '''表头和对应的列数据类型记得根据文件修改一下'''
            dtypes: dict[str, str] = {'EPC': 'object', '交通': 'object', '水利': 'object', '设计': 'object'}
        df = dd.read_csv(urlpath=csvpath, usecols=use_cols, dtype=dtypes).fillna(' ')
        info = df[df['企业名称'] == company_name].compute().to_string(index=False, header=False)
        parts = info.split()
        dict_headers = ["企业名称", "新中大行业类别", "业务类型"]
        info_dict = {}
        i = 0
        for part in parts:
            info_dict[dict_headers[i]] = part
            # print(f' copy already: {part}')
            i += 1
        return info_dict
    except Exception as e:
        print(f'get_info error:{e}')
        return None


def test():
    '测试函数'
    try:
        hn_csv = r"../config/湖南省名单.csv"
        use_cols = ["企业名称", "城市基建", "能源", "交通", "水利", "工业服务", "施工", '设计/EPC']
        dtypes = {'设计/EPC': 'object', '交通': 'object', '水利': 'object'}
        info = csv_getinfo(csvpath=hn_csv, company_name='安化县方圆天下建筑有限责任公司', use_cols=use_cols,
                           dtypes=dtypes)
        print(info)
    except Exception as e:
        print(f'test error:{e}')


if __name__ == '__main__':
    test()
