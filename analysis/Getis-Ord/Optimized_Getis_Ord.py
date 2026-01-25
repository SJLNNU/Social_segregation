import geopandas as gpd
import numpy as np
from libpysal.weights import KNN, DistanceBand
from esda.getisord import G_Local
import os
from scipy.stats import zscore
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

def find_optimal_k(gdf, variable, k_range=range(2, 21)):
    """
    找到最优的K值
    使用轮廓系数（Silhouette Score）来评估不同K值的效果
    """
    best_score = -1
    best_k = 8  # 默认值
    
    for k in k_range:
        try:
            w = KNN.from_dataframe(gdf, k=k)
            w.transform = 'r'
            g_local = G_Local(gdf[variable], w)
            
            # 使用Gi*统计量和p值计算轮廓系数
            labels = np.where(g_local.p_sim <= 0.05, 
                            np.where(g_local.Gs > 0, 1, -1), 0)
            
            if len(np.unique(labels)) > 1:  # 确保至少有两个不同的类别
                score = silhouette_score(gdf[[variable]], labels)
                if score > best_score:
                    best_score = score
                    best_k = k
        except:
            continue
            
    return best_k

def find_optimal_distance(gdf, variable, distance_range=None):
    """
    找到最优的距离阈值
    使用轮廓系数来评估不同距离阈值的效果
    """
    if distance_range is None:
        # 计算数据集中点之间的平均距离
        coords = np.array([(x, y) for x, y in zip(gdf.geometry.x, gdf.geometry.y)])
        distances = []
        for i in range(len(coords)):
            for j in range(i+1, len(coords)):
                distances.append(np.sqrt(np.sum((coords[i] - coords[j])**2)))
        mean_dist = np.mean(distances)
        distance_range = np.linspace(mean_dist * 0.1, mean_dist * 2, 10)
    
    best_score = -1
    best_distance = None
    
    for distance in distance_range:
        try:
            w = DistanceBand.from_dataframe(gdf, distance)
            w.transform = 'r'
            g_local = G_Local(gdf[variable], w)
            
            labels = np.where(g_local.p_sim <= 0.05,
                            np.where(g_local.Gs > 0, 1, -1), 0)
            
            if len(np.unique(labels)) > 1:
                score = silhouette_score(gdf[[variable]], labels)
                if score > best_score:
                    best_score = score
                    best_distance = distance
        except:
            continue
            
    return best_distance

def optimized_hot_spot_analysis(gdf, variable):
    """
    执行优化的热点分析
    自动选择最优的空间权重矩阵
    """
    # 尝试KNN方法
    optimal_k = find_optimal_k(gdf, variable)
    w_knn = KNN.from_dataframe(gdf, k=optimal_k)
    w_knn.transform = 'r'
    g_local_knn = G_Local(gdf[variable], w_knn)
    
    # 尝试距离带方法
    optimal_distance = find_optimal_distance(gdf, variable)
    w_dist = DistanceBand.from_dataframe(gdf, optimal_distance)
    w_dist.transform = 'r'
    g_local_dist = G_Local(gdf[variable], w_dist)
    
    # 比较两种方法的结果，选择更好的一个
    knn_score = silhouette_score(gdf[[variable]], 
                                np.where(g_local_knn.p_sim <= 0.05,
                                       np.where(g_local_knn.Gs > 0, 1, -1), 0))
    dist_score = silhouette_score(gdf[[variable]], 
                                np.where(g_local_dist.p_sim <= 0.05,
                                       np.where(g_local_dist.Gs > 0, 1, -1), 0))
    
    if knn_score > dist_score:
        return g_local_knn, 'KNN', optimal_k
    else:
        return g_local_dist, 'DistanceBand', optimal_distance

# 变量名称列表
thmemlist = ['theme1','theme2','theme3','theme4','themes']

# 文件路径
folder_path = r"D:\Code\Social_segregation\data\Census_tract"

for variable in thmemlist:
    print(f"\n开始处理 {variable} 的分析...")
    output_folder = r"D:\Code\Social_segregation\data\Z_score_Corrected\Optimized_Getis_Ord_{}_Results".format(variable)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 首先收集所有数据来计算百分位数
    all_values = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.geojson'):
            file_path = os.path.join(folder_path, filename)
            gdf = gpd.read_file(file_path)
            if variable in gdf.columns:
                all_values.extend(gdf[variable].tolist())

    # 计算66%和33%的分位数
    hotspot_threshold = np.percentile(all_values, 66)
    coldspot_threshold = np.percentile(all_values, 33)

    print(f"{variable} 热点阈值 (66%分位数): {hotspot_threshold}")
    print(f"{variable} 冷点阈值 (33%分位数): {coldspot_threshold}")

    for filename in os.listdir(folder_path):
        if filename.endswith('.geojson'):
            file_path = os.path.join(folder_path, filename)
            city_name = filename.split('.')[0]

            # 读取 GeoJSON
            gdf = gpd.read_file(file_path)

            # 变量检查
            if variable in gdf.columns:
                # 执行优化的热点分析
                g_local, method, optimal_param = optimized_hot_spot_analysis(gdf, variable)
                print(f"{city_name} 使用 {method} 方法，最优参数: {optimal_param}")

                # 赋值到 DataFrame
                gdf[f'{variable}_gi'] = g_local.Gs
                gdf[f'{variable}_gi_p'] = g_local.p_sim

                # 计算不同显著性水平下的热点和冷点
                significance_levels = {
                    '99%': 0.01,
                    '95%': 0.05,
                    '90%': 0.10
                }
                for level, alpha in significance_levels.items():
                    gdf[f'{variable}_hotspot_{level}'] = (g_local.p_sim <= alpha) & (g_local.Gs > 0) & (gdf[variable] > hotspot_threshold)
                    gdf[f'{variable}_coldspot_{level}'] = (g_local.p_sim <= alpha) & (g_local.Gs < 0) & (gdf[variable] < coldspot_threshold)

                    gdf[f'{variable}_hotcold_{level}'] = np.select(
                        [gdf[f'{variable}_hotspot_{level}'], gdf[f'{variable}_coldspot_{level}']],
                        [f'Hot Spot ({level})', f'Cold Spot ({level})'],
                        default='Not Significant'
                    )

                # 保存结果
                output_filename = f"{city_name}_optimized_getis_ord_results.geojson"
                output_path = os.path.join(output_folder, output_filename)
                gdf.to_file(output_path, driver='GeoJSON')

                print(f"已完成 {city_name} 的 {variable} 分析，结果保存在 {output_path}")

    print(f"{variable} 的优化 Getis-Ord Gi* 分析已完成。")

print("所有主题的优化 Getis-Ord Gi* 分析已完成。") 