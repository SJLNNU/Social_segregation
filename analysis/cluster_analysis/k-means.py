import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.stats import f_oneway, kruskal
import pandas as pd
import seaborn as sns


def apply_kmeans_clustering(city_list, n_clusters):
    '''
    使用K-means算法进行聚类
    :param city_list: list[City] 城市数据
    :param n_clusters: 期望的聚类数量
    :return: 更新city.cluster_class
    '''
    data = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    city_names = [city.name for city in city_list]
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
    labels = kmeans.fit_predict(data)

    for city, label in zip(city_list, labels):
        city.cluster_class = label
    # 转换为 DataFrame 进行分析
    df = pd.DataFrame({
        "City": [city.name for city in city_list],
        "Cluster": [city.cluster_class for city in city_list],
        "Theme 1": [city.theme1 for city in city_list],
        "Theme 2": [city.theme2 for city in city_list],
        "Theme 3": [city.theme3 for city in city_list],
        "Theme 4": [city.theme4 for city in city_list]
    })

    # 计算 ANOVA & Kruskal-Wallis 贡献度分析
    variable_importance = {}
    for theme in ["Theme 1", "Theme 2", "Theme 3", "Theme 4"]:
        groups = [df[df["Cluster"] == c][theme].values for c in np.unique(labels)]
        f_stat, p_value = f_oneway(*groups) if all(len(g) > 1 for g in groups) else (np.nan, np.nan)
        h_stat, kw_p_value = kruskal(*groups) if all(len(g) > 1 for g in groups) else (np.nan, np.nan)
        variable_importance[theme] = {"ANOVA_p": p_value, "Kruskal_p": kw_p_value}

    importance_df = pd.DataFrame(variable_importance).T
    importance_df.sort_values(by="ANOVA_p", ascending=True, inplace=True)

    # 可视化 1: PCA 降维后散点图
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=reduced_data[:, 0], y=reduced_data[:, 1], hue=labels, palette="Set2", s=100)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.title("K-Means Clustering (PCA Projection)")
    plt.legend(title="Cluster")
    plt.show()

    # 可视化 2: 变量分布的箱线图
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Cluster", y="value", hue="variable",
                data=pd.melt(df, id_vars=["City", "Cluster"],
                             value_vars=["Theme 1", "Theme 2", "Theme 3", "Theme 4"]))
    plt.title("Boxplot of Variables Across Clusters")
    plt.legend(title="Variable")
    plt.show()

    # 可视化 3: 雷达图（Radar Chart）
    cluster_means = df.groupby("Cluster").mean(numeric_only=True)

    # 仅选择数值列，避免 num_vars 计算错误
    num_vars = len(cluster_means.select_dtypes(include=[np.number]).columns)

    # 可视化变量贡献度（雷达图）
    cluster_means = df.groupby("Cluster").mean(numeric_only=True)
    num_vars = len(cluster_means.columns)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_ylim(0.45, 0.65)  # 设置雷达图的值域
    for idx, row in cluster_means.iterrows():
        ax.plot(angles + [angles[0]], row.tolist() + [row.tolist()[0]], label=f"Cluster {idx}")
    ax.set_xticks(angles)
    ax.set_xticklabels(cluster_means.columns)
    ax.set_title("Radar Chart of Cluster Characteristics")
    ax.legend()
    plt.show()

    return city_list, df, importance_df


if __name__ == '__main__':
    from Social_segregation.struct.data_reader import data_reader

    #from visual_analysis_first_paper import plot_city_data_by_class

    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
    city_list = data_reader(file_path,3)
    city_list,df, importance_df= apply_kmeans_clustering(city_list, 3)
    print(importance_df)
    #plot_city_data_combined(city_list)
    #plot_city_data_by_cluster(city_list)

    #save_results_to_csv(city_list,r"D:\Code\Social_segregation\data\SSI_golbal_data_kmeans_result.csv")