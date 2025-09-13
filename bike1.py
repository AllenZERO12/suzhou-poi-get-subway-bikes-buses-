import requests
import pandas as pd
from geopy.distance import geodesic

# 高德API Key
API_KEY = '8eabaf5867c625908f73a0a8934213dd'
BASE_URL = 'https://restapi.amap.com/v3/place/around'

# 苏州市地铁1号线站点及坐标
stations = {
    "木渎": (31.265931, 120.512721),
    "金枫路": (31.301448, 120.521507),
    "汾湖路": (31.309318, 120.530903),
    "玉山路": (31.313149, 120.540297),
    "狮子山": (31.317253, 120.552142),
    "塔园路": (31.319747, 120.562296),
    "滨河路": (31.320980, 120.574050),
    "西环路": (31.321467, 120.585881),
    "桐泾北路": (31.321535, 120.595593),
    "广济南路": (31.321694, 120.606524),
    "养育巷": (31.323944, 120.618949),
    "乐桥": (31.325902, 120.630928),
    "临顿路": (31.325399, 120.640776),
    "相门": (31.324844, 120.652579),
    "东环路": (31.325000, 120.664444),
    "中央公园": (31.324290, 120.676713),
    "星海广场": (31.323444, 120.689222),
    "东方之门": (31.322111, 120.701417),
    "文化博览中心": (31.321667, 120.712889),
    "时代广场": (31.321111, 120.724278),
    "星湖街": (31.318611, 120.736167),
    "南施街": (31.313611, 120.747111),
    "星塘街": (31.308667, 120.756278),
    "钟南街": (31.300278, 120.767000),
}

# 计算两点距离（单位：米）
def calculate_distance(poi_coords, station_coords):
    return geodesic(poi_coords, station_coords).meters

# 调用高德API获取公共自行车站点数据
def fetch_poi_data(station_name, station_coords):
    pois = []
    page = 1

    while True:
        params = {
            'key': API_KEY,
            'location': f"{station_coords[1]},{station_coords[0]}",  # 经纬度：经度,纬度
            'radius': 800,  # 查找800米范围内的POI
            'types': '190301',  # 公共自行车停放点类型代码
            'offset': 20,  # 每次返回的数据条数
            'page': page  # 页码
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        # 错误处理
        if data['status'] != '1':
            print(f"Error fetching data for {station_name}: {data['info']}")
            break

        # 解析POI数据
        pois_page = data.get('pois', [])
        for poi in pois_page:
            poi_coords = (float(poi['location'].split(',')[1]), float(poi['location'].split(',')[0]))
            distance = calculate_distance(poi_coords, station_coords)
            pois.append({
                '地铁站': station_name,
                '地铁站坐标': station_coords,
                '自行车站点': poi.get('name', '未知'),
                '地址': poi.get('address', '未知'),
                '自行车站坐标': poi_coords,
                '距离(米)': round(distance, 2)
            })

        # 判断是否为最后一页
        if len(pois_page) < 20:
            break
        page += 1

    return pois

# 主函数
def main():
    all_pois = []

    for station_name, station_coords in stations.items():
        print(f"正在获取 {station_name} 站周围的公共自行车站点...")
        pois = fetch_poi_data(station_name, station_coords)
        all_pois.extend(pois)

    # 保存结果到Excel
    if all_pois:
        df = pd.DataFrame(all_pois)
        output_file = "1号线_公共自行车站点分布.xlsx"
        df.to_excel(output_file, index=False)
        print(f"数据已保存至 {output_file}")
    else:
        print("未获取到任何数据！")

if __name__ == "__main__":
    main()
