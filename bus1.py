import requests
import pandas as pd
from geopy.distance import geodesic

# 高德API Key
API_KEY = '8eabaf5867c625908f73a0a8934213dd'
BASE_URL = 'https://restapi.amap.com/v3/place/around'

# 苏州市地铁1号线各站点及坐标
stations = {
    "木渎": (31.270695, 120.511676),
    "金枫路": (31.283938, 120.543441),
    "汾湖路": (31.292061, 120.558045),
    "玉山路": (31.298528, 120.574113),
    "狮子山": (31.299813, 120.592715),
    "塔园路": (31.301711, 120.601667),
    "滨河路": (31.305499, 120.611751),
    "西环路": (31.311907, 120.623064),
    "桐泾北路": (31.315036, 120.637413),
    "广济南路": (31.316984, 120.652238),
    "养育巷": (31.318177, 120.666371),
    "乐桥": (31.319857, 120.679539),
    "临顿路": (31.320491, 120.688859),
    "相门": (31.320525, 120.698639),
    "东环路": (31.319186, 120.711546),
    "中央公园": (31.316877, 120.721894),
    "星海广场": (31.317307, 120.735233),
    "东方之门": (31.317845, 120.744595),
    "文化博览中心": (31.319149, 120.754256),
    "时代广场": (31.318826, 120.767419),
    "星湖街": (31.319273, 120.777755),
    "南施街": (31.320175, 120.787787),
    "星塘街": (31.325644, 120.744297),
    "钟南街": (31.326865, 120.800673)
}

# 计算距离
def calculate_distance(poi_coords, station_coords):
    return geodesic(poi_coords, station_coords).meters

# 获取公交站台POI数据
def fetch_poi_data(station_name, station_coords):
    pois = []
    page = 1
    poi_type = '150700'  # 公交站台类型代码

    while True:
        params = {
            'key': API_KEY,
            'location': f"{station_coords[1]},{station_coords[0]}",  # 经度,纬度
            'radius': 800,  # 800米范围
            'types': poi_type,
            'offset': 20,  # 每页最多返回20条数据
            'page': page
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data['status'] != '1':
            print(f"获取 {station_name} 数据失败: {data['info']}")
            break

        # 提取POI数据
        if 'pois' in data:
            for poi in data['pois']:
                poi_coords = (float(poi['location'].split(',')[1]), float(poi['location'].split(',')[0]))
                distance = calculate_distance(poi_coords, station_coords)
                pois.append({
                    'station_name': station_name,
                    'station_coords': station_coords,
                    'poi_name': poi.get('name', '未知'),
                    'distance': distance,
                    'address': poi.get('address', '未知'),
                    'poi_coords': poi_coords
                })

        # 判断是否还有下一页
        if len(data.get('pois', [])) < 20:
            break
        page += 1

    return pois

# 保存结果到Excel
def save_poi_data(poi_data):
    if not poi_data:
        print("没有获取到POI数据，未生成Excel!")
        return

    df = pd.DataFrame(poi_data)
    filename = 'bus_station_poi_1号线.xlsx'
    df.to_excel(filename, index=False)
    print(f"POI数据已保存至 {filename}")

# 主函数
def main():
    all_pois = []

    for station_name, station_coords in stations.items():
        print(f"正在获取 {station_name} 周围公交站台数据...")
        pois = fetch_poi_data(station_name, station_coords)
        all_pois.extend(pois)

    save_poi_data(all_pois)

if __name__ == "__main__":
    main()
