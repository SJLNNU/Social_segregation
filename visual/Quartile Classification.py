import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_process.data_struct import  city,census_tract
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import mapping
import json
from shapely.geometry import Point
from data_process.data_reader import data_reader

def plot_quartile_classification(city_list):
    # 按 themes 进行排序
    city_list.sort(key=lambda x: x.themes)
    themes_list = [city.themes for city in city_list]
    city_names = [city.name for city in city_list]
    
    # 计算分位数（使用三分位数）
    q1 = np.percentile(themes_list, 33.33)  # 33.33% 分位数
    q2 = np.percentile(themes_list, 66.67)  # 66.67% 分位数
    
    # 创建图形
    plt.figure(figsize=(8, 16), dpi=300)
    
    # 设置字体
    plt.rcParams['font.family'] = 'Calibri'
    plt.rcParams['font.size'] = 8
    
    # 创建渐变色映射
    colors = ['#7597f6', '#dcdddd', '#ea7c61']  # 绿色(低) -> 黄色(中) -> 红色(高)
    
    # 绘制水平柱状图
    bars = plt.barh(range(len(city_list)), themes_list, height=0.3)
    
    # 根据init_class设置颜色
    for i, bar in enumerate(bars):
        bar.set_color(colors[city_list[i].init_class])
    
    # 添加分位数线（竖线）
    # plt.axvline(x=q1, color='black', linestyle='--', linewidth=2, alpha=0.1, label='33.33th Percentile')
    # plt.axvline(x=q2, color='black', linestyle='--', linewidth=2, alpha=0.1, label='66.67th Percentile')
    
    # 设置图形属性
    plt.ylabel('MSAs', fontsize=10, labelpad=20)
    plt.xlabel('Global SSI-Comp.', fontsize=10, labelpad=10)
    plt.yticks(range(len(city_list)), city_names, fontsize=8)
    plt.xticks(fontsize=8)
    plt.grid(True, axis='x', linestyle='--', alpha=0.3)
    
    # 设置x轴范围，让差异更明显
    x_min = min(themes_list) - 0.01
    x_max = max(themes_list) + 0.01
    plt.xlim(x_min, x_max)
    
    # 添加图例
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor=colors[0], label='Low Segregation'),
        plt.Rectangle((0,0),1,1, facecolor=colors[1], label='Medium Segregation'),
        plt.Rectangle((0,0),1,1, facecolor=colors[2], label='High Segregation'),
        # plt.Line2D([0], [0], color='black', linestyle='--', linewidth=2, alpha=0.5, label='33.33th Percentile'),
        # plt.Line2D([0], [0], color='black', linestyle='--', linewidth=2, alpha=0.5, label='66.67th Percentile')
    ]
    plt.legend(handles=legend_elements, loc='lower right')
    
    # 调整布局，减少左侧和底部留白
    plt.tight_layout(pad=4.0)
    plt.subplots_adjust(left=0.18, bottom=0.18)
    plt.margins(y=0.05)
    
    # 显示图形
    plt.show()

if __name__ == '__main__':

    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
    city_list = data_reader(file_path, 3, classification_strategy='tertiles')
    plot_quartile_classification(city_list)
    
    
    
