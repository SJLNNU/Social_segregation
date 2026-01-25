import os
import geopandas as gpd
import pandas as pd
from sklearn.metrics import jaccard_score

# 设置文件夹路径
main_class_number=1
themes_folder = r"D:\Code\Social_segregation\data\Getis_Ord_theme{}_Results".format(main_class_number)  # themes 结果文件夹
sub_class_number=2
sub_theme1_folder = r"D:\Code\Social_segregation\data\Getis_Ord_theme{}_Results".format(sub_class_number)  # theme1-4 结果文件夹


output_csv = r"D:\Code\Social_segregation\data\Jaccard_Similarity_theme{}-theme{}.csv".format(main_class_number,sub_class_number)  # 结果文件路径

# 置信度水平
significance_levels = ['99%', '95%', '90%']

# 初始化结果列表
results = []

# 遍历 themes 文件夹
for filename in os.listdir(themes_folder):
    if filename.endswith('.geojson'):
        city_name = filename.split('_')[0]  # 例如 "NewYork_getis_ord_results.geojson"，提取 "NewYork"

        # 读取 themes 的 GeoJSON
        themes_gdf = gpd.read_file(os.path.join(themes_folder, filename))

        # 遍历 theme1-4 结果文件夹
        for sub_filename in os.listdir(sub_theme1_folder):
            if sub_filename.startswith(city_name) and sub_filename.endswith('.geojson'):
                sub_theme_name = 'theme{}'.format(sub_class_number) # 例如 "NewYork_theme1_getis_ord_results.geojson"，提取 "theme1"
                # 读取 theme1-4 的 GeoJSON
                sub_gdf = gpd.read_file(os.path.join(sub_theme1_folder, sub_filename))
                # 确保两个文件的 Census Tract 顺序一致
                themes_gdf = themes_gdf.sort_values(by="id").reset_index(drop=True)
                sub_gdf = sub_gdf.sort_values(by="id").reset_index(drop=True)

                # 检查是否对齐
                if not all(themes_gdf["id"] == sub_gdf["id"]):
                    print(f"Warning: {city_name} - {sub_theme_name} GEOIDs do not match exactly. Check input data.")
                    continue

                # 计算 Jaccard 相似系数
                jaccard_scores = {'City': city_name, 'Comparison': f'Theme{main_class_number}-{sub_theme_name}'}

                for level in significance_levels:
                    # 提取热点和冷点数据（转换为二进制）
                    themes_hotspot = themes_gdf[f'theme{main_class_number}_hotspot_{level}'].astype(int)
                    sub_hotspot = sub_gdf[f'{sub_theme_name}_hotspot_{level}'].astype(int)

                    themes_coldspot = themes_gdf[f'theme{main_class_number}_coldspot_{level}'].astype(int)
                    sub_coldspot = sub_gdf[f'{sub_theme_name}_coldspot_{level}'].astype(int)

                    # 计算 Jaccard 相似度
                    jaccard_hotspot = jaccard_score(themes_hotspot, sub_hotspot)
                    jaccard_coldspot = jaccard_score(themes_coldspot, sub_coldspot)

                    # 存入字典
                    jaccard_scores[f'Hotspot_{level}'] = jaccard_hotspot
                    jaccard_scores[f'Coldspot_{level}'] = jaccard_coldspot

                # 添加到结果列表
                results.append(jaccard_scores)

# 转换为 DataFrame 并保存为 CSV
df_results = pd.DataFrame(results)
df_results.to_csv(output_csv, index=False)

print(f"Jaccard 相似系数计算完成，结果已保存至 {output_csv}")
