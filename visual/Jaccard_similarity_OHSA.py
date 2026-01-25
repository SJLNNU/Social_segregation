import os
import geopandas as gpd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.metrics import jaccard_score


def create_similarity_heatmap(similarity_matrix, themes, city_name, output_folder):
    """Create and save similarity heatmap"""
    font_size = 20
    plt.figure(figsize=(10, 6))  # Increased figure width to accommodate city name
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = font_size

    # 只保留城市名（去掉前缀）
    # 支持多种前缀格式，取最后一个下划线后的内容
    city_short = re.split(r'_|-', city_name)[-1]

    # Create mask for upper triangle
    mask = np.zeros_like(similarity_matrix, dtype=bool)
    mask[np.triu_indices_from(mask, k=1)] = True  # k=1 to exclude diagonal

    # Create heatmap using coolwarm colormap
    heatmap = sns.heatmap(similarity_matrix,
                         mask=mask,
                         annot=True,
                         cmap="coolwarm",
                         vmin=0,
                         vmax=1,
                         center=0.5,
                         square=True,
                         fmt='.2f',
                         annot_kws={'size': font_size, 'weight': 'bold'},
                         xticklabels=themes,
                         yticklabels=themes,
                         linewidths=0.5,
                         )

    # Add black border to the heatmap
    for _, spine in heatmap.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_color('black')
    
    # 在热力图右上角空白区域添加城市名
    plt.text(0.6, 0.85, city_short, 
             transform=plt.gca().transAxes,
             rotation=0,
             fontsize=font_size+4,
             fontweight='bold',
             verticalalignment='center',
             horizontalalignment='center')
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save the heatmap
    output_path = os.path.join(output_folder, f"{city_name}_jaccard_similarity.png")
    plt.xlabel('Different Dimensions', fontsize=font_size)
    plt.ylabel('Different Dimensions', fontsize=font_size)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def process_city_shapefiles(folder_path, output_folder):
    city_files = defaultdict(list)
    pattern = re.compile(r"^(.*?)_census_tract_theme([1-4])_OHSA_result\.shp$")
    theme_names = {
        '1': 'SES',
        '2': 'HCD',
        '3': 'MSL',
        '4': 'H&T'
    }
    for f in os.listdir(folder_path):
        if f.endswith('_OHSA_result.shp'):
            m = pattern.match(f)
            if m:
                city = m.group(1)
                city_files[city].append(f)
    for city, files in city_files.items():
        if len(files) != 4:
            print(f"{city} 主题数量不足4个，实际为{len(files)}")
            continue
        # 处理城市名
        if 'washington' in city.strip().lower():
            city_display = "Washington,DC MSA"
        else:
            city_display = f"{city} MSA"
        theme_sets = []
        themes = []
        for shp in sorted(files):
            m = pattern.match(shp)
            theme_num = m.group(2)
            theme = theme_names[theme_num]
            themes.append(theme)
            gdf = gpd.read_file(os.path.join(folder_path, shp))
            tracts_gi3 = set(gdf[gdf['Gi_Bin'] == 3]['SOURCE_ID'])
            theme_sets.append(tracts_gi3)
        # 计算全集
        all_tracts = sorted(set.union(*theme_sets))
        n_themes = len(themes)
        # 生成0/1向量
        binary_matrix = np.zeros((n_themes, len(all_tracts)), dtype=int)
        for i, s in enumerate(theme_sets):
            binary_matrix[i] = [1 if tid in s else 0 for tid in all_tracts]
        # 计算Jaccard相似度矩阵
        similarity_matrix = np.zeros((n_themes, n_themes))
        for i in range(n_themes):
            for j in range(n_themes):
                similarity_matrix[i, j] = jaccard_score(binary_matrix[i], binary_matrix[j])
        create_similarity_heatmap(similarity_matrix, themes, city_display, output_folder)
        print(f"{city_display} 处理完成")

# Usage
input_folder = r"D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_tertile_filter_result"
output_folder = r"D:\Code\Social_segregation\data\Jaccard_similarity_OHSA"
process_city_shapefiles(input_folder, output_folder)
