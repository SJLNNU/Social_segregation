import geopandas as gpd
import numpy as np
from libpysal.weights import KNN
from esda.getisord import G_Local
import os
from scipy.stats import zscore

# 变量名称列表
thmemlist = ['theme1','theme2','theme3','theme4','themes']

# 文件路径
folder_path = r"D:\Code\Social_segregation\data\Census_tract"

for variable in thmemlist:
    print(f"\n开始处理 {variable} 的分析...")
    output_folder = r"D:\Code\Social_segregation\data\Z_score_Corrected\Getis_Ord_{}_Results".format(variable)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 首先收集所有数据来计算百分位数
    all_values = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.geojson'):
            file_path = os.path.join(folder_path, filename)
            gdf = gpd.read_file(file_path)
            if variable in gdf.columns:
                all_values.extend(gdf[variable].tolist())

    # 计算66%和33%的分位数
    hotspot_threshold = np.percentile(all_values, 66)
    coldspot_threshold = np.percentile(all_values, 33)

    print(f"{variable} 热点阈值 (66%分位数): {hotspot_threshold}")
    print(f"{variable} 冷点阈值 (33%分位数): {coldspot_threshold}")

    for filename in os.listdir(folder_path):
        if filename.endswith('.geojson'):
            file_path = os.path.join(folder_path, filename)
            city_name = filename.split('.')[0]

            # 读取 GeoJSON
            gdf = gpd.read_file(file_path)

            # 变量检查
            if variable in gdf.columns:
                # 标准化数据（Z-score 标准化）
                #gdf[variable] = zscore(gdf[variable])

                # K 近邻权重（确保每个点至少有 8 个邻居）
                w = KNN.from_dataframe(gdf, k=8)
                w.transform = 'r'

                # 计算 Getis-Ord Gi*
                g_local = G_Local(gdf[variable], w)

                # 赋值到 DataFrame
                gdf[f'{variable}_gi'] = g_local.Gs
                gdf[f'{variable}_gi_p'] = g_local.p_sim

                # 计算不同显著性水平下的热点和冷点
                significance_levels = {
                    '99%': 0.01,
                    '95%': 0.05,
                    '90%': 0.10
                }
                for level, alpha in significance_levels.items():
                    # 修改热点和冷点的判断逻辑，使用百分位数作为阈值
                    gdf[f'{variable}_hotspot_{level}'] = (g_local.p_sim <= alpha) & (g_local.Gs > 0) & (gdf[variable] > hotspot_threshold)
                    gdf[f'{variable}_coldspot_{level}'] = (g_local.p_sim <= alpha) & (g_local.Gs < 0) & (gdf[variable] < coldspot_threshold)

                    gdf[f'{variable}_hotcold_{level}'] = np.select(
                        [gdf[f'{variable}_hotspot_{level}'], gdf[f'{variable}_coldspot_{level}']],
                        [f'Hot Spot ({level})', f'Cold Spot ({level})'],
                        default='Not Significant'
                    )

                # 保存结果
                output_filename = f"{city_name}_getis_ord_results.geojson"
                output_path = os.path.join(output_folder, output_filename)
                gdf.to_file(output_path, driver='GeoJSON')

                print(f"已完成 {city_name} 的 {variable} 分析，结果保存在 {output_path}")

    print(f"{variable} 的 Getis-Ord Gi* 分析已完成。")

print("所有主题的 Getis-Ord Gi* 分析已完成。")
