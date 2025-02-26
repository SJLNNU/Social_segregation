import geopandas as gpd
import numpy as np
from libpysal.weights import Queen
from esda.moran import Moran
import os
import pandas as pd

# 定义要分析的变量列表
variables = ['theme1', 'theme2', 'theme3', 'theme4', 'themes']

# 创建一个空的字典来存储结果
results = {}

# 遍历文件夹中的所有GeoJSON文件
folder_path = r"/Social_segregation/data/Census_tract"  # 替换为你的文件夹路径
for filename in os.listdir(folder_path):
    if filename.endswith('.geojson'):
        file_path = os.path.join(folder_path, filename)
        city_name = filename.split('.')[0]  # 假设文件名是城市名

        # 读取GeoJSON文件
        gdf = gpd.read_file(file_path)

        # 构造基于Queen邻接方式的权重矩阵
        w = Queen.from_dataframe(gdf)
        w.transform = 'r'  # 归一化权重

        # 初始化这个城市的结果
        city_results = {'city_name': city_name}

        # 对每个变量计算Moran's I
        for variable in variables:
            if variable in gdf.columns:
                moran = Moran(gdf[variable], w)
                city_results[f'{variable}_moran'] = moran.I
                city_results[f'{variable}_moran_p'] = moran.p_norm
            else:
                city_results[f'{variable}_moran'] = np.nan
                city_results[f'{variable}_moran_p'] = np.nan

        results[city_name] = city_results

# 将结果转换为DataFrame
df_results = pd.DataFrame.from_dict(results, orient='index')

# 重新排列列的顺序
columns_order = ['city_name'] + [f'{var}_moran' for var in variables] + [f'{var}_moran_p' for var in variables]
df_results = df_results[columns_order]

# 将结果保存到CSV文件
output_path = r"/Social_segregation/data/morans_i_results.csv"
df_results.to_csv(output_path, index=False)

print(f"分析完成，结果已保存到 {output_path}")
