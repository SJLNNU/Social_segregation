import geopandas as gpd
import numpy as np
from libpysal.weights import Queen
from esda.moran import Moran

# 读取 GeoJSON 文件
gdf = gpd.read_file(r"D:\Code\Social_segregation\struct\newyork_census_tract.geojson")  # 替换为你的 GeoJSON 文件路径

# 选择用于计算 Moran's I 的变量
variable = "themes"  # 确保字段名称与 GeoJSON 文件匹配

# 构造基于 Queen 邻接方式的权重矩阵
w = Queen.from_dataframe(gdf)
w.transform = 'r'  # 归一化权重

# 计算 Moran's I
moran = Moran(gdf[variable], w)

# 输出结果
print(variable)
print(f"Moran's I: {moran.I}")
print(f"p-value: {moran.p_norm}")
