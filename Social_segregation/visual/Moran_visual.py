import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 读取数据
file_path = r"D:\Code\Social_segregation\data\morans_i_results.csv"
data = pd.read_csv(file_path)

# 确保列名一致
theme_columns = ["theme1_moran", "theme2_moran", "theme3_moran", "theme4_moran",'themes_moran']

# 计算每个城市在每个主题下的排名
ranked_data = data.copy()
for theme in theme_columns:
    ranked_data[f"{theme}_rank"] = ranked_data[theme].rank(method="min", ascending=False)

# 找出每个主题排名的极值城市（排名最高和最低的城市）
extreme_cities = set()
for theme in theme_columns:
    highest_city = ranked_data.loc[ranked_data[f"{theme}_rank"].idxmin(), "city_name"]
    lowest_city = ranked_data.loc[ranked_data[f"{theme}_rank"].idxmax(), "city_name"]
    extreme_cities.update([highest_city, lowest_city])

extreme_cities = list(extreme_cities)

# 为极值城市创建标签（带排名）
sorted_data = data.sort_values("Themes", ascending=False).reset_index(drop=True)
sorted_data["Rank"] = sorted_data.index + 1
sorted_data["City_Rank"] = sorted_data["Rank"].astype(str) + ". " + sorted_data["city_name"]

# 生成城市排名映射字典，并按照排名排序
city_rank_map = {city: sorted_data.loc[sorted_data["city_name"] == city, "City_Rank"].values[0] for city in extreme_cities}
selected_city_labels = sorted(city_rank_map.values(), key=lambda x: int(x.split(". ")[0]))

# 按照排名顺序重新排列 extreme_cities
extreme_cities_sorted = sorted(extreme_cities, key=lambda city: int(city_rank_map[city].split(". ")[0]))

# 转换排名数据到长格式
ranked_long = ranked_data.melt(id_vars=["city_name"],
                               value_vars=[f"{theme}_rank" for theme in theme_columns],
                               var_name="Theme", value_name="Rank")
ranked_long["Theme"] = ranked_long["Theme"].str.replace("_rank", "")

# 设置颜色
np.random.seed(42)
colors = {city: np.random.rand(3, ) for city in ranked_data["city_name"]}

# 创建Bump Chart
sns.set(style="whitegrid")
plt.figure(figsize=(14, 8))

legend_handles_dict = {}

for city in ranked_data["city_name"].unique():
    city_data = ranked_long[ranked_long["city_name"] == city]
    color = colors[city] if city in extreme_cities else "lightgray"
    alpha = 1.0 if city in extreme_cities else 0.5
    linewidth = 2.5 if city in extreme_cities else 1

    line, = plt.plot(city_data["Theme"], city_data["Rank"], marker="o",
                     color=color, alpha=alpha, linewidth=linewidth)

    if city in extreme_cities:
        legend_handles_dict[city] = line

# 生成 legend_handles_sorted 并按照排名排序
legend_handles_sorted = [legend_handles_dict[city] for city in extreme_cities_sorted]

# 标签与标题
plt.gca().invert_yaxis()
plt.xticks(theme_columns, fontsize=12)
plt.xlabel("Theme", fontsize=14)
plt.ylabel("Rank", fontsize=14)
plt.title("Rank Changes Across Themes (Extreme Cities Highlighted)", fontsize=16)

plt.tight_layout()
plt.subplots_adjust(right=0.85)

plt.legend(legend_handles_sorted, selected_city_labels, loc="upper right", bbox_to_anchor=(1.16, 1),
           fontsize=10, frameon=False, title="Extreme Ranked Cities")

# 显示图表
plt.show()