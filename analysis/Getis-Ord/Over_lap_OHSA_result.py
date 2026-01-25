import os
import geopandas as gpd
import re
from collections import defaultdict

def process_city_shapefiles(folder_path, output_folder):
    # 用于分组
    city_files = defaultdict(list)
    # 匹配城市名
    pattern = re.compile(r"^(.*?)_census_tract_theme[1-4]_OHSA_result\.shp$")
    for f in os.listdir(folder_path):
        if f.endswith('_OHSA_result.shp'):
            m = pattern.match(f)
            if m:
                city = m.group(1)
                city_files[city].append(f)
    print("分组结果：", city_files)  # 调试用
    for city, files in city_files.items():
        print(f"{city} 包含文件：{files}")  # 调试用
        if len(files) != 4:
            print(f"{city} 主题数量不足4个，实际为{len(files)}")
            continue
        gdfs = [gpd.read_file(os.path.join(folder_path, shp)) for shp in files]
        print("字段名：", gdfs[0].columns)  # 调试用
        all_tracts = gdfs[0][['SOURCE_ID', 'geometry']].copy()
        for val in [-3, -2, -1, 0, 1, 2, 3]:
            all_tracts[str(val)] = 0
        for gdf in gdfs:
            for idx, row in gdf.iterrows():
                fid = row['SOURCE_ID']
                gi_bin = row['Gi_Bin']
                all_tracts.loc[all_tracts['SOURCE_ID'] == fid, str(gi_bin)] += 1
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        out_path = os.path.join(output_folder, f"{city}_summary.shp")
        all_tracts.to_file(out_path)
        print(f"{city} 处理完成，输出：{out_path}")

# 用法
input_folder = r"D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_tertile_filter_result"
output_folder = r"D:\Code\Social_segregation\data\Overlap_EPSG5070_OHSA_tertile_filter_result"
process_city_shapefiles(input_folder, output_folder)
