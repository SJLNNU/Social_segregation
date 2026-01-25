# 我们计算出莫兰指数以后，看这个莫兰指数与原来的theme1-4，以及themes的相关性
#Paper*
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)
from data_process.data_reader import data_reader,read_moran_results
import pandas as pd


# 读取原始数据以及墨兰指数
city_list=data_reader(r"D:\Code\Social_segregation\data\SSI_golbal_data.csv",3)
city_list=read_moran_results(r"D:\Code\Social_segregation\data\morans_i_results_added_z.csv",city_list)

# 可视化theme1 和theme1_moran.
import matplotlib.pyplot as plt
import numpy as np

# city_list=sorted(city_list,key=lambda x:x.theme1)
# theme1_list=[city.theme1 for city in city_list]
# theme1_moran_list=[city.theme1_moran for city in city_list]

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# 定义主题名称映射
theme_names = {
    'theme1': 'SES',
    'theme2': 'HCD',
    'theme3': 'MSL',
    'theme4': 'H&T',
    'themes': 'Comp.'
}

# 定义颜色映射
theme_colors = {
    'theme1': '#1f77b4',  # 深蓝
    'theme2': '#6a3d9a',  # 紫色
    'theme3': '#e377c2',  # 品红
    'theme4': '#2ca02c',  # 绿色
    'themes': '#17becf'   # 蓝绿色
}

def visualize_theme_and_moran(city_list, theme, init_class=None, show_plot=True):
    # 确保theme是有效的
    valid_themes = ['theme1', 'theme2', 'theme3', 'theme4', 'themes']
    if theme not in valid_themes:
        raise ValueError("theme must be one of 'theme1', 'theme2', 'theme3', 'theme4', or 'themes'")

    theme_col = theme
    moran_col = f'{theme}_moran'
    theme_name = theme_names[theme]
    theme_color = theme_colors[theme]

    # 筛选城市
    if init_class is not None:
        filtered_cities = [city for city in city_list if city.init_class == init_class]
    else:
        filtered_cities = city_list

    # 将筛选后的城市列表转换为DataFrame
    df = pd.DataFrame([(city.name, getattr(city, theme_col), getattr(city, moran_col)) for city in filtered_cities],
                      columns=['city', theme_col, moran_col])

    # 按theme值排序
    df = df.sort_values(theme_col)

    # 计算Spearman's Rank Correlation
    correlation, p_value = stats.spearmanr(df[theme_col], df[moran_col])

    if show_plot:
        # 创建图形和坐标轴
        fig, ax1 = plt.subplots(figsize=(20, 10))  # 增加图表大小

        # 绘制theme的折线（使用左侧y轴）
        #ax1.set_xlabel('Cities')
        ax1.set_ylabel(theme_name, color=theme_color)
        ax1.plot(df['city'], df[theme_col], color=theme_color, label=theme_name, marker='o')
        ax1.tick_params(axis='y', labelcolor=theme_color)
        num_cities = len(df)
        step = max(1, num_cities // 20)  # 显示大约20个标签
        ax1.set_xticks(range(0, num_cities, step))
        ax1.set_xticklabels(df['city'][::step], rotation=45, ha='center')  # 垂直显示标签

        # 在每个数据点处添加一个小的垂直线，以指示城市位置
        for i in range(num_cities):
            ax1.axvline(x=i, color='grey', linestyle=':', alpha=0.5)

        # 创建第二个y轴
        ax2 = ax1.twinx()

        # 绘制theme_moran的折线（使用右侧y轴）
        moran_color = '#ff7f0e'  # 使用橙色作为Moran's I的颜色
        ax2.set_ylabel(f"{theme_name} Moran's I", color=moran_color)
        ax2.plot(df['city'], df[moran_col], color=moran_color, label=f"{theme_name} Moran's I", marker='s')
        ax2.tick_params(axis='y', labelcolor=moran_color)

        # 设置图表标题
        title = f"{theme_name} and Moran's I Comparison"
        if init_class is not None:
            title += f" for Init Class {init_class}"
        title += f"\nSpearman's Rank Correlation: {correlation:.4f} (p-value: {p_value:.4f})"
        plt.title(title)

        # 旋转x轴标签以避免重叠
        plt.xticks(rotation=45)

        # 添加图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        # 调整布局
        plt.tight_layout()

        # 显示图表
        plt.show()

    return {
        'theme': theme_name,
        'init_class': init_class,
        'spearman_correlation': correlation,
        'p_value': p_value,
        'city_count': len(df)
    }

# 使用示例
# 假设我们已经有了city_list
# city_list = data_reader(r"D:\Code\Social_segregation\data\SSI_golbal_data.csv", 3)
# city_list = read_moran_results(r"D:\Code\Social_segregation\data\morans_i_results.csv", city_list)

# 可视化Themes和其Moran's I
result=visualize_theme_and_moran(city_list, 'theme1',init_class=None,)
result=visualize_theme_and_moran(city_list, 'theme2',init_class=None,)
result=visualize_theme_and_moran(city_list, 'theme3',init_class=None,)
result=visualize_theme_and_moran(city_list, 'theme4',init_class=None,)
result=visualize_theme_and_moran(city_list, 'themes',init_class=None,)
print(result)


