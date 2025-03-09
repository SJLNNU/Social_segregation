# FILEPATH: D:/Code/Social_segregation/visual/Four_D_visual.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 读取数据
file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
data = pd.read_csv(file_path)

# 确保列名一致
theme_columns = ["Theme1", "Theme2", "Theme3", "Theme4", 'Themes']

# 按照 'Themes' 列对城市进行排序，从高到低
sorted_data = data.sort_values('Themes', ascending=False).reset_index(drop=True)

# 选择指定排名的城市
selected_ranks = [1, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
top_cities = sorted_data.loc[sorted_data.index.isin([i-1 for i in selected_ranks]), 'City'].tolist()

# 计算每个城市在每个主题下的排名（排名1为最优）
ranked_data = sorted_data.copy()
for theme in theme_columns:
    ranked_data[f"{theme}_rank"] = ranked_data[theme].rank(method="min", ascending=False)

# 转换为长格式
ranked_long = ranked_data.melt(id_vars=["City"],
                               value_vars=[f"{theme}_rank" for theme in theme_columns[:-1]],  # 不包括 'Themes'
                               var_name="Theme", value_name="Rank")

# 简化主题名称
ranked_long["Theme"] = ranked_long["Theme"].str.replace("_rank", "")

# 设定颜色
np.random.seed(42)
colors = {city: np.random.rand(3,) for city in top_cities}

# 设置 Seaborn 风格
sns.set_theme(style="whitegrid")

# 创建 Bump Chart
plt.figure(figsize=(16, 10))  # 增加图表大小以适应更大的图例

# 首先绘制非选中的城市
for city in ranked_data["City"]:
    if city not in top_cities:
        city_data = ranked_long[ranked_long["City"] == city]
        plt.plot(city_data["Theme"], city_data["Rank"], marker="o",
                 color="lightgray", alpha=0.3, linewidth=1)

# 然后绘制选中的城市
for city in top_cities:
    city_data = ranked_long[ranked_long["City"] == city]
    color = colors[city]
    label = f"{city} (Rank: {ranked_data[ranked_data['City'] == city].index[0] + 1})"
    plt.plot(city_data["Theme"], city_data["Rank"], marker="o", label=label,
             color=color, alpha=1.0, linewidth=2)

# 设置图表样式
plt.gca().invert_yaxis()  # 使排名 1 在顶部
plt.xticks(theme_columns[:-1], fontsize=12)  # 横轴标签，不包括 'Themes'
plt.xlabel("Theme", fontsize=14)
plt.ylabel("Rank", fontsize=14)
plt.title("Rank Changes Across Themes (Selected Cities Highlighted)", fontsize=16)

plt.tight_layout()  # 自动调整子图参数
plt.subplots_adjust(right=0.7)  # 为图例留出更多空间

# 添加图例，增加行间距
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10, frameon=False,
           title="Selected Cities", title_fontsize=12, labelspacing=1.2)

# 显示图表
plt.show()
