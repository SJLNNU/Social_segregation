# FILEPATH: D:/Code/Social_segregation/analysis/Moran/Hotspot_Coldspot_Analysis.py

import geopandas as gpd
import os
import pandas as pd

def analyze_city(city_file, input_folder, output_folder):
    # 读取城市数据
    city_name = city_file.split('.')[0]
    city_data = gpd.read_file(os.path.join(input_folder, city_file))

    # 创建城市输出文件夹
    city_output_folder = os.path.join(output_folder, city_name)
    os.makedirs(city_output_folder, exist_ok=True)

    # 读取每一个Census Tract 的Theme1-4 和Themes的数据
    themes = ['theme1', 'theme2', 'theme3', 'theme4', 'themes']
    data = {theme: city_data[theme] for theme in themes}
    df = pd.DataFrame(data)

    # 分析离群点并保存冷点和热点
    outliers = {}
    for theme in themes:
        Q1 = df[theme].quantile(0.25)
        Q3 = df[theme].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        lower_outliers = city_data[city_data[theme] < lower_bound]
        upper_outliers = city_data[city_data[theme] > upper_bound]

        outliers[theme] = {
            "lower": len(lower_outliers),
            "upper": len(upper_outliers)
        }

        # 保存冷点和热点的GeoJSON
        lower_outliers.to_file(os.path.join(city_output_folder, f"{theme}_coldspot.geojson"), driver='GeoJSON')
        upper_outliers.to_file(os.path.join(city_output_folder, f"{theme}_hotspot.geojson"), driver='GeoJSON')

    # 打印离群点分析结果
    print(f"\n城市: {city_name}")
    print("离群点分析:")
    for theme, counts in outliers.items():
        print(f"  {theme}:")
        print(f"    冷点数量: {counts['lower']}")
        print(f"    热点数量: {counts['upper']}")
    print("\n" + "="*50)

def main():
    input_folder = r'D:\Code\Social_segregation\data\Census_tract'
    output_folder = r'D:\Code\Social_segregation\output\hotspot_coldspot'

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 处理每个城市的数据
    for city_file in os.listdir(input_folder):
        if city_file.endswith('.geojson'):
            analyze_city(city_file, input_folder, output_folder)

if __name__ == "__main__":
    main()
