import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 读取数据
file_path = r"D:\Code\Social_segregation\data\morans_i_results.csv"
data = pd.read_csv(file_path)

# 确保列名一致
theme_columns = ["theme1_moran", "theme2_moran", "theme3_moran", "theme4_moran",'themes_moran']

# 计算每个城市在每个主题下的排名（排名1为最优）
ranked_data = data.copy()
for theme in theme_columns:
    ranked_data[f"{theme}_rank"] = ranked_data[theme].rank(method="min", ascending=False)

# 仅保留排名数据，并转换为长格式
ranked_long = ranked_data.melt(id_vars=["city_name"],
                               value_vars=[f"{theme}_rank" for theme in theme_columns],
                               var_name="Theme", value_name="Rank")

# 替换 Theme1_rank -> Theme1，简化主题名称
ranked_long["Theme"] = ranked_long["Theme"].str.replace("_rank", "")

# 设定颜色
np.random.seed(42)
colors = {city: np.random.rand(3,) for city in ranked_data["city_name"]}

# 设置 Seaborn 风格
sns.set(style="whitegrid")

# 创建更清晰的 Bump Chart
plt.figure(figsize=(14, 8))

# 选取前10个城市进行高亮，其余城市使用浅灰色提高可读性
top_cities = ranked_data["city_name"].unique()[:10]

for city in ranked_data["city_name"].unique():
    city_data = ranked_long[ranked_long["city_name"] == city]
    color = colors[city] if city in top_cities else "lightgray"  # 仅高亮前10个城市
    alpha = 1.0 if city in top_cities else 0.5  # 非重点城市透明度降低
    linewidth = 2 if city in top_cities else 1  # 重点城市加粗

    plt.plot(city_data["Theme"], city_data["Rank"], marker="o", label=city if city in top_cities else None,
             color=color, alpha=alpha, linewidth=linewidth)

# 设定标签与标题
plt.gca().invert_yaxis()  # 使排名 1 在顶部
plt.xticks(theme_columns, fontsize=12)  # 横轴标签
plt.xlabel("Theme", fontsize=14)
plt.ylabel("Rank", fontsize=14)
plt.title("City Rank Changes Across Themes (Selected 10 Highlighted)", fontsize=16)

plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
plt.subplots_adjust(right=0.85)  # 为图例留出空间
# 仅展示前 10 个城市的图例，避免视觉混乱
plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1), fontsize=10, frameon=False, title="Highlighted Cities")

# 显示图表
plt.show()