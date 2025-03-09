# 导入必要的库
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据文件
file_path = r"D:\Code\Social_segregation\data\morans_i_results.csv"
df = pd.read_csv(file_path)

# 处理列名，确保一致性
df.rename(columns={"city_name": "City", "themes_moran": "Themes_Moran"}, inplace=True)

# 去除 "_census_tract" 后缀，仅保留城市名称
df["City"] = df["City"].str.replace("_census_tract", "", regex=True)

# 按 Themes_Moran 降序排序
df_sorted = df.sort_values(by="Morans_Cluster_Class", ascending=False)

# 选择要可视化的主题列
theme_columns = ["theme1_moran", "theme2_moran", "theme3_moran", "theme4_moran", "Themes_Moran"]
#theme_columns = ["theme2_moran"]
# 计算每个主题的平均值
means = df_sorted[theme_columns].mean()

# 设置颜色方案（高对比度）
colors = ["#1d73b6", "#24a645", "#f27830", "#8768a6", "#bdbf32"]  # 蓝、橙、绿、红、紫
#colors = [ "#24a645", "#f27830", "#8768a6", "#bdbf32"]

extreme_cities = {}
for theme in theme_columns:
    max_city = df_sorted.loc[df_sorted[theme].idxmax(), "City"]
    min_city = df_sorted.loc[df_sorted[theme].idxmin(), "City"]
    extreme_cities[theme] = {"max": max_city, "min": min_city}

# 创建散点图
plt.figure(figsize=(12, 6))

# 绘制散点
for theme, color in zip(theme_columns, colors):
    plt.scatter(df_sorted["City"], df_sorted[theme], label=theme, color=color, alpha=0.8)

# 添加平均值虚线
for theme, color in zip(theme_columns, colors):
    plt.axhline(y=means[theme], color=color, linestyle="--", alpha=0.7, label=f"{theme} Mean")

# 突出极值城市
for theme, color in zip(theme_columns, colors):
    max_city = extreme_cities[theme]["max"]
    min_city = extreme_cities[theme]["min"]

    max_value = df_sorted.loc[df_sorted["City"] == max_city, theme].values[0]
    min_value = df_sorted.loc[df_sorted["City"] == min_city, theme].values[0]

    plt.scatter(max_city, max_value, color=color, edgecolors="black", s=100, linewidth=1.5, label=f"{theme} Max")
    plt.scatter(min_city, min_value, color=color, edgecolors="black", s=100, linewidth=1.5, marker="s", label=f"{theme} Min")

cluster_changes = df_sorted["Morans_Cluster_Class"].ne(df_sorted["Morans_Cluster_Class"].shift()).cumsum()
for i in range(1, cluster_changes.max()):
    boundary_index = cluster_changes[cluster_changes == i].index[-1]
    plt.axvline(x=boundary_index, color='gray', linestyle=':', alpha=0.7)

# 调整标签和标题
plt.xticks(rotation=60)
plt.ylabel("Moran's Index")
plt.title("Scatter Plot of Moran's Index with Mean Lines (Sorted by Themes)")

# 调整图例位置，避免遮挡数据
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))

# 自动调整布局，防止标签重叠
plt.tight_layout()

# 显示图表
plt.show()
