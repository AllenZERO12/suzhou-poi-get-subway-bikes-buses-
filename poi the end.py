import requests
import pandas as pd
import time

# 高德地图 API Key
API_KEY = "3c0750db1002647d11b6a6d3dd2398a4"

# 苏州地铁 1 号线各站点及其经纬度
stations = [
    {"name": "唐庄", "location": "120.683611,31.340454"},
    {"name": "倪浜", "location": "120.673421,31.333304"},
    {"name": "烟雨桥", "location": "120.677802,31.323757"},
    {"name": "东方之门", "location": "120.678894,31.316815"},
    {"name": "李公堤西", "location": "120.679706,31.306657"},
    {"name": "金厍桥", "location": "120.67834,31.296533"},
    {"name": "东振路", "location": "120.676358,31.288555"},
    {"name": "墅浦路北", "location": "120.674025,31.28008"},
    {"name": "通园路南", "location": "120.667888,31.269491"},
    {"name": "北港路", "location": "120.656549,31.269906"},
    {"name": "迎春路", "location": "120.640353,31.267662"}

]
    # 要查询的 POI 类型
poi_types = [
     '010000', '020000', '030000', '040000', '050000',
    '060000', '070000', '080000',  '090000','100000', '110000',
    '120000', '130000', '140000', '150000', '160000',
    '170000'

]

# 半径范围（单位：米）
radius = 800

# 高德 API URL
url_template = "https://restapi.amap.com/v3/place/around"

# 存储统计结果
results = []

# 遍历每个站点
for station in stations:
    station_name = station["name"]
    location = station["location"]

    # 初始化当前站点的 POI 类型统计
    poi_counts = {poi_type: 0 for poi_type in poi_types}

    # 查询每种类型的 POI
    for poi_type in poi_types:
        params = {
            "key": API_KEY,
            "location": location,
            "types": poi_type,
            "radius": radius,
            "offset": 120,
            "page": 1,
            "extensions": "base"
        }

        total_count = 0
        while True:
            response = requests.get(url_template, params=params)
            data = response.json()

            if data.get("status") != "1":
                print(f"查询失败: {station_name}, 类型: {poi_type}")
                break

            # 累计当前页结果
            total_count += len(data.get("pois", []))

            # 判断是否有下一页
            if int(data.get("count", 0)) <= params["page"] * 50:
                break

            params["page"] += 1
            time.sleep(0.2)  # 防止请求过快被限制

        poi_counts[poi_type] = total_count

    # 将统计结果加入总表
    results.append({"站点名称": station_name, **poi_counts})

# 保存结果到 Excel
output_path = r"C:\Users\acer\PycharmProjects\pythonProject\POI统计结果.xlsx"
df = pd.DataFrame(results)
df.to_excel(output_path, index=False)

print(f"POI 统计结果已保存至: {output_path}")

