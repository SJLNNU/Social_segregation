# FILEPATH: D:/Code/Social_segregation/analysis/Moran/Data_range_analysis.py

import geopandas as gpd
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取Moran's I 结果
morans_results = pd.read_csv('D:/Code/Social_segregation/data/morans_i_results.csv')
morans_results.set_index('city_name', inplace=True)
# 读取城市数据
fold_path = r'D:\Code\Social_segregation\data\Census_tract'
save_fold=r'D:\Code\Social_segregation\data\visual_result\Cencus_tract_level_box_plot'

for cur_city_file in os.listdir(fold_path):
    city_name = cur_city_file.split('.')[0]
    city_data = gpd.read_file(os.path.join(fold_path, cur_city_file))

    # 读取每一个Census Tract 的Them1-4 和Themes的数据
    themes = ['theme1', 'theme2', 'theme3', 'theme4', 'themes']
    data = {theme: city_data[theme] for theme in themes}
    df = pd.DataFrame(data)

    # 绘制箱体图
    fig, ax = plt.subplots(figsize=(14, 10))
    box_plot = df.boxplot(ax=ax, return_type='dict')
    plt.title(f"{city_name} - Theme Distribution with Outlier Counts")

    # 分析离群点并在图上标注
    for i, theme in enumerate(themes):
        Q1 = df[theme].quantile(0.25)
        Q3 = df[theme].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        lower_outliers = df[df[theme] < lower_bound][theme]
        upper_outliers = df[df[theme] > upper_bound][theme]

        # 在图上标注离群点数量
        ax.text(i + 1.1, lower_bound, f'Lower: {len(lower_outliers)}',
                verticalalignment='top', fontsize=12)
        ax.text(i + 1.1, upper_bound, f'Upper: {len(upper_outliers)}',
                verticalalignment='bottom', fontsize=12)

        # 添加莫兰指数
        moran_i = morans_results.loc[city_name, f'{theme}_moran']
        ax.text(i + 1, ax.get_ylim()[0], f"Moran's I: {moran_i:.3f}",
                horizontalalignment='center', verticalalignment='bottom', fontsize=12,)

        # 调整x轴标签位置
    plt.xticks(range(1, len(themes) + 1), themes, rotation=0, )

    y_min, y_max = ax.get_ylim()
    ax.set_ylim(y_min, y_max + (y_max - y_min) * 0.1)
    # 调整布局并保存图片
    plt.tight_layout()
    save_path=os.path.join(save_fold,f"{city_name}_boxplot_with_outliers.png")
    plt.savefig(save_path)
    plt.close()

    # 打印离群点分析结果
    print(f"\n城市: {city_name}")
    print("离群点分析:")
    for theme in themes:
        lower_count = len(df[df[theme] < lower_bound])
        upper_count = len(df[df[theme] > upper_bound])
        print(f"  {theme}:")
        print(f"    小于25%的离群点数量: {lower_count}")
        print(f"    大于75%的离群点数量: {upper_count}")
    print("\n" + "="*50)

# ... existing code ...
