import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 读取数据
file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
data = pd.read_csv(file_path)

# 定义主题列名和颜色
theme_columns = ["Theme1", "Theme2", "Theme3", "Theme4", "Themes"]
theme_columns_name = ["SES", "HCD", "MSL", "HT", "Comp."]
theme_colors = ["#1f77b4", "#6a3d9a", "#e377c2", "#2ca02c", "#17becf"]

# 计算每个城市在每个主题下的排名
ranked_data = data.copy()
for theme in theme_columns:
    ranked_data[f"{theme}_rank"] = ranked_data[theme].rank(method="min", ascending=False)

# 找出每个主题SSI最高的城市
highlighted_cities = {}
for theme, color in zip(theme_columns, theme_colors):
    city = ranked_data.loc[ranked_data[theme].idxmax(), "City"]
    highlighted_cities[city] = color

# 为所有城市创建排名标签
sorted_data = data.sort_values("Themes", ascending=False).reset_index(drop=True)
sorted_data["Rank"] = sorted_data.index + 1
sorted_data["City_Rank"] = sorted_data["Rank"].astype(str) + ". " + sorted_data["City"]

# 转换排名数据到长格式
ranked_long = ranked_data.melt(id_vars=["City"],
                               value_vars=[f"{theme}_rank" for theme in theme_columns],
                               var_name="Theme", value_name="Rank")
ranked_long["Theme"] = ranked_long["Theme"].str.replace("_rank", "")

# 设置字体
plt.rcParams['font.family'] = 'Calibri'
plt.rcParams['font.size'] = 10

# 创建Bump Chart
plt.figure(figsize=(6, 4), dpi=300)
ax = plt.gca()
ax.grid(False)  # 移除网格线

# 绘制所有城市的线条
for city in ranked_data["City"].unique():
    city_data = ranked_long[ranked_long["City"] == city]
    if city in highlighted_cities:
        color = highlighted_cities[city]
        alpha = 1.0
        linewidth = 2.5
    else:
        color = "#808080"
        alpha = 0.2
        linewidth = 1

    plt.plot(city_data["Theme"], city_data["Rank"], marker="o",
             color=color, alpha=alpha, linewidth=linewidth)

# 标签与标题
plt.gca().invert_yaxis()
ax = plt.gca()
ax.set_ylim(30.5, 0.5)
ax.yaxis.set_major_locator(plt.MultipleLocator(1))

# 减小主题间距
plt.xticks(range(len(theme_columns)), theme_columns_name, fontsize=10)
plt.xlabel("Social Dimensions", fontsize=12)
plt.ylabel("Segregation Rank", fontsize=12)

# 添加右侧城市名称标签
ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
city_ranks = sorted_data["City_Rank"].tolist()
ax2.set_yticks(range(1, len(city_ranks) + 1))
ax2.set_yticklabels(city_ranks, fontsize=8)

# 为城市名称设置颜色
for i, tick in enumerate(ax2.get_yticklabels()):
    city = city_ranks[i].split(". ")[1]
    if city in highlighted_cities:
        tick.set_color(highlighted_cities[city])
    else:
        tick.set_color("#808080")

ax2.tick_params(axis='y', which='major', pad=2)

# # 添加图例
# legend_elements = [plt.Line2D([0], [0], color=color, label=name, linewidth=2.5)
#                   for color, name in zip(theme_colors[1:], theme_columns_name[1:])]
# ax.legend(
#     handles=legend_elements,
#     loc='lower right',
#     bbox_to_anchor=(0.92, 0.05),
#     frameon=False,
#     fontsize=8
# )

plt.tight_layout()
plt.show()
