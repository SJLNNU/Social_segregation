import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

themes = ["theme1", "theme2", "theme3", "theme4", "themes"]
theme_names = {
    "theme1": "SES",
    "theme2": "HCD",
    "theme3": "MSL",
    "theme4": "HT",
    "themes": "Comp."
}
base_dir = r"D:/Code/Social_segregation/data/Jaccard_similarity/"

# 创建一个字典来存储每个城市的数据
city_data = {}

for theme_x in themes:
    for theme_y in themes:
        if theme_x != theme_y:
            file_path = os.path.join(base_dir, theme_x, f"Jaccard_Similarity_{theme_x}-{theme_y}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)

                for _, row in df.iterrows():
                    city = row['City']
                    if city not in city_data:
                        city_data[city] = pd.DataFrame(index=themes, columns=themes)
                    city_data[city].loc[theme_x, theme_y] = row['Hotspot_95%']
                    city_data[city].loc[theme_y, theme_x] = row['Hotspot_95%']  # 确保对称性

# 为每个城市生成热力图
for city, data in city_data.items():
    # 创建重命名的数据框副本
    df_renamed = data.astype(float).copy()
    df_renamed.index = [theme_names[theme] for theme in df_renamed.index]
    df_renamed.columns = [theme_names[theme] for theme in df_renamed.columns]

    # 创建掩码以只显示下三角部分
    mask = np.zeros_like(df_renamed, dtype=bool)
    mask[np.triu_indices_from(mask, k=1)] = True  # k=1 表示不包括对角线

    # 创建热力图
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_renamed, annot=True, cmap="coolwarm", vmin=0, vmax=0.3, mask=mask)
    plt.title(f"Jaccard Similarity Heatmap for {city}")
    plt.tight_layout()

    # 保存图片
    output_dir = os.path.join(base_dir, "heatmaps")
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"{city}_heatmap.png"))
    plt.close()

print("所有热力图已生成完毕。")

# # 生成总体散点图
# plt.figure(figsize=(15, 10))
#
# # 为每个城市分配一个颜色
# colors = plt.cm.rainbow(np.linspace(0, 1, len(city_data)))
# city_color = dict(zip(city_data.keys(), colors))
#
# ax1 = plt.gca()
# ax2 = ax1.twinx()
#
# for city, data in city_data.items():
#     theme_x_list = []
#     theme_y_list = []
#     similarity_list = []
#     for i, theme_x in enumerate(themes):
#         for j, theme_y in enumerate(themes):
#             if theme_x != theme_y:
#                 similarity = data.loc[theme_x, theme_y]
#                 theme_x_list.append(theme_names[theme_x])
#                 theme_y_list.append(theme_names[theme_y])
#                 similarity_list.append(similarity)
#
#     ax1.scatter(theme_x_list, theme_y_list, c=[city_color[city]], s=100, alpha=0.6, label=city)
#     ax2.scatter(theme_x_list, similarity_list, c=[city_color[city]], s=100, alpha=0.6, marker='s')
#
# ax1.set_xlabel("Themes")
# ax1.set_ylabel("Themes")
# ax2.set_ylabel("Similarity")
#
# ax1.set_ylim(-0.5, len(themes) - 0.5)
# ax2.set_ylim(0, 1)
#
# plt.title("Overall Jaccard Similarity (Hotspot) at 95% Confidence Level")
#
# # 添加图例
# ax1.legend(title="Cities", bbox_to_anchor=(1.05, 1), loc='upper left')
#
# plt.tight_layout()
# plt.savefig(os.path.join(base_dir, "overall_similarity_scatter.png"), bbox_inches='tight')
# plt.close()
#
# print("总体散点图已生成完毕。")