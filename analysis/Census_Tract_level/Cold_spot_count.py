# 读取Census Tract 数据，统计其中冷点的数量。
import geopandas as gpd
import json
import os
import numpy as np

geojson_fold=r'D:\Code\Social_segregation\data\Getis_Ord_themes_Results'
cur_theme=os.path.split(geojson_fold)[-1].split('_')[-2]

for cur_file in os.listdir(geojson_fold):
    if cur_file.endswith('.geojson'):
        cur_path=os.path.join(geojson_fold,cur_file)
        cur_city_data=gpd.read_file(cur_path)
        # 统计冷点的数量
        cold_points=cur_city_data[cur_city_data[cur_theme+'_gi']<0]
        cold_points_count=len(cold_points)
        print(f"{cur_file} 冷点数量：{cold_points_count}")