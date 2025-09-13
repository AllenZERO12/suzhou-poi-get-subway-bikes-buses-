import requests
import geopandas as gpd
import pandas as pd


def get_railway_stop(city_name, save_file=''):
    """
    数据来源于高德地图: https://ditu.amap.com/

    :param city_name: 要爬取的地铁城市名，必须正确输入
    :param save_file: 是否保存为文件
                      1 = 存成 Excel 文件
                      2 = 存成 Shapefile 文件
                      其他值 = 不保存文件
    示例:
    get_railway_stop(city_name='上海市', save_file=1)
    """
    # 获取支持爬取地铁信息的城市列表
    citylist = requests.get(
        url='https://map.amap.com/service/subway?_1707184339116&srhdata=citylist.json'
    ).json()

    spell, adcode = '', ''
    for city in citylist['citylist']:
        if city['cityname'] == city_name:
            spell, adcode = city['spell'], city['adcode']
            break

    if not spell:
        print('城市名输入错误')
        return

    # 构建目标城市地铁信息的 URL
    city_url = (
        f'https://map.amap.com/service/subway?_1707184339123&srhdata={adcode}_drw_{spell}.json'
    )
    target_city = requests.get(url=city_url).json()

    # 文件名设置
    filename = target_city['s']

    # 初始化结果数据
    result = {
        'name': [],  # 地铁站名
        'line': [],  # 完整线路名称，如 "地铁5号线 莘庄--闵行开发区"
        'line_': [],  # 简略线路名称，如 "地铁5号线"
        'color': [],  # 线路颜色
        'lon': [],  # 经度
        'lat': [],  # 纬度
        'transfer': []  # 是否为换乘站（1: 是，0: 否）
    }

    # 解析地铁线路与站点信息
    for line in target_city['l']:
        for stop in line['st']:
            result['name'].append(stop['n'])
            result['line'].append(line['kn'] + line['la'])
            result['line_'].append(line['kn'])
            result['color'].append(line['cl'])

            lon, lat = map(float, stop['sl'].split(','))
            result['lon'].append(lon)
            result['lat'].append(lat)
            result['transfer'].append(stop['t'])

    # 将结果转换为 DataFrame
    data = pd.DataFrame(result)

    # 根据保存选项保存为 Excel 或 Shapefile
    if save_file == 1:
        data.to_excel(f'{filename}.xlsx', index=False)
    elif save_file == 2:
        gdf = gpd.GeoDataFrame(
            data, geometry=gpd.points_from_xy(data['lon'], data['lat']),
            crs='EPSG:4326'
        )
        gdf.to_file(f'{filename}.shp', driver='ESRI Shapefile', encoding='utf-8')

    return data
get_railway_stop(city_name='苏州市', save_file=1)



