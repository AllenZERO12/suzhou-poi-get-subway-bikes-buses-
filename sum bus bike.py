import pandas as pd

# 读取 Excel 文件
file_path = r"C:\\Users\\acer\\Desktop\\POI AND BUILDING AREA\\5\\5号线_公共自行车站点分布.xlsx"
df = pd.read_excel(file_path, dtype=str)  # 读取为字符串，避免数据类型问题

# 确保 "station_name" 列存在
if "station_name" not in df.columns:
    raise ValueError("缺少 'station_name' 列，请检查 Excel 文件")

# 统计每个站点的数量，并保持原文件顺序
df["count"] = df.groupby("station_name")["station_name"].transform("count")

# 去重，保留第一条出现的站点（保持原顺序）
df_unique = df.drop_duplicates(subset=["station_name"], keep="first")

# 只保留需要的列（站点名称 + 统计数量）
result = df_unique[["station_name", "count"]]

# 保存结果到 Excel，确保文件路径包含扩展名
output_file = r"C:/Users/acer/PycharmProjects/pythonProject/站点数量统计.xlsx"
result.to_excel(output_file, index=False)

print(f"站点数量统计完成，已保存到 {output_file}")
