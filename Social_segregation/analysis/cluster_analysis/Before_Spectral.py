from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.cluster import KMeans
from scipy.linalg import eigh
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering
from scipy.linalg import eigh

def extract_features(city_list):
    data = []
    for city in city_list:
        data.append([city.theme1, city.theme2, city.theme3, city.theme4])
    return np.array(data)

def determine_optimal_k(data, k_max=10):
    # 1. 数据标准化
    data_std =data

    # 2. 计算RBF相似度矩阵
    gamma = 1.0  # 可调整或使用启发式方法确定
    affinity = rbf_kernel(data_std, gamma=gamma)

    # ========== 拉普拉斯矩阵计算 ==========
    D = np.diag(affinity.sum(axis=1))
    D_inv_sqrt = np.linalg.inv(np.sqrt(D))
    laplacian = D_inv_sqrt @ (D - affinity) @ D_inv_sqrt

    # ========== 特征分解 ==========
    eigenvalues, eigenvectors = eigh(laplacian)
    eigenvectors = eigenvectors[:, :k_max]
    eigenvectors_normalized = eigenvectors / np.linalg.norm(eigenvectors, axis=1, keepdims=True)

    # ========== 惯性计算 ==========
    inertias = []
    for k in range(1, k_max + 1):
        if k == 1:
            inertias.append(np.inf)  # K=1时设为无穷大便于后续处理
            continue
        X = eigenvectors_normalized[:, :k]
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
        inertias.append(kmeans.inertia_)

    # ========== 自动肘点检测算法 ==========
    diffs = np.diff(inertias)
    acceleration = np.diff(diffs)
    optimal_k = np.argmax(acceleration) + 2  # +2补偿两次diff操作

    # ========== 可视化与结果输出 ==========
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, k_max + 1), inertias, 'bo-', label='Inertia')
    plt.axvline(optimal_k, color='r', linestyle='--', label=f'Suggested K={optimal_k}')
    plt.xlabel('Number of clusters (K)')
    plt.ylabel('Inertia')
    plt.title(f'Elbow Analysis (Suggested K={optimal_k})')
    plt.legend()
    plt.xticks(range(1, k_max + 1))
    plt.grid(True)
    plt.show()

    return optimal_k


if __name__ == '__main__':
    from Social_segregation.data_struct.data_reader import data_reader, save_results_to_csv, save_city_location
    # from visual_analysis_first_paper import plot_city_data_by_class
    from Social_segregation.visual import plot_city_data_combined, plot_city_data_by_cluster

    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"# 调用函数
    city_list = data_reader(file_path, 3)  # 调用分析函数
    city_features = extract_features(city_list)
    best_k=determine_optimal_k(city_features, k_max=10)
    print(f'[结果] 推荐聚类数 K = {best_k}')