import os
import geopandas as gpd
import pandas as pd

# 设置文件夹路径
themes_folder = r"D:\Code\Social_segregation\data\Getis_Ord_themes_Results"
theme_folders = [
    r"D:\Code\Social_segregation\data\Getis_Ord_theme1_Results",
    r"D:\Code\Social_segregation\data\Getis_Ord_theme2_Results",
    r"D:\Code\Social_segregation\data\Getis_Ord_theme3_Results",
    r"D:\Code\Social_segregation\data\Getis_Ord_theme4_Results"
]

# 输出文件夹
output_folder = r"D:\Code\Social_segregation\data\Common_Hotspots"
os.makedirs(output_folder, exist_ok=True)

# 置信度水平
significance_levels = ['99%', '95%', '90%']

# 遍历 themes 文件夹
for filename in os.listdir(themes_folder):
    if filename.endswith('.geojson'):
        city_name = filename.split('_')[0]

        # 读取 themes 的 GeoJSON
        themes_gdf = gpd.read_file(os.path.join(themes_folder, filename))

        # 读取 theme1-4 的 GeoJSON
        theme_gdfs = []
        for folder in theme_folders:
            theme_file = next((f for f in os.listdir(folder) if f.startswith(city_name) and f.endswith('.geojson')), None)
            if theme_file:
                theme_gdf = gpd.read_file(os.path.join(folder, theme_file))
                theme_gdfs.append(theme_gdf)
            else:
                print(f"Warning: No matching file found for {city_name} in {folder}")
                break

        # 如果没有找到所有theme的文件，跳过这个城市
        if len(theme_gdfs) != 4:
            continue

        # 确保所有文件的 Census Tract 顺序一致
        all_gdfs = [themes_gdf] + theme_gdfs
        for gdf in all_gdfs:
            gdf.sort_values(by="id", inplace=True)
            gdf.reset_index(drop=True, inplace=True)

        # 检查是否对齐
        if not all(all_gdfs[0]["id"].equals(gdf["id"]) for gdf in all_gdfs[1:]):
            print(f"Warning: {city_name} - GEOIDs do not match exactly. Check input data.")
            continue

        # 找出共同的热点
        for level in significance_levels:
            common_hotspots = themes_gdf[f'themes_hotspot_{level}'].astype(int)
            for theme_gdf in theme_gdfs:
                theme_name = theme_gdf.columns[theme_gdf.columns.str.contains('_hotspot_')][0].split('_')[0]
                common_hotspots &= theme_gdf[f'{theme_name}_hotspot_{level}'].astype(int)

            # 创建包含共同热点的GeoDataFrame
            common_hotspots_gdf = themes_gdf[common_hotspots == 1].copy()

            # 保存结果
            output_filename = f"{city_name}_common_hotspots_{level}.geojson"
            output_path = os.path.join(output_folder, output_filename)
            common_hotspots_gdf.to_file(output_path, driver='GeoJSON')

            print(f"Saved common hotspots for {city_name} at {level} confidence level")

print("处理完成。共同热点已保存到指定文件夹。")
