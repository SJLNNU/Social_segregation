import numpy as np
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.tree import DecisionTreeClassifier,export_text,plot_tree
import seaborn as sns
from sklearn.cluster import SpectralClustering
from scipy.stats import f_oneway, kruskal
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

def apply_spectral_clustering(city_list, n_clusters):
    '''
    使用谱聚类算法进行聚类
    :param city_list: list[City] 城市数据
    :param n_clusters: 期望的聚类数量
    :return: 更新city.cluster_class
    '''
    data = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    spectral = SpectralClustering(n_clusters=n_clusters, random_state=0, affinity='nearest_neighbors')
    labels = spectral.fit_predict(data)

    for city, label in zip(city_list, labels):
        city.cluster_class = label
    return city_list


def apply_spectral_clustering(city_list, n_clusters):
    """
    使用谱聚类进行聚类，并分析变量贡献度
    """
    data = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    city_names = [city.id for city in city_list]
    # 计算 n_neighbors，避免超出样本数
    n_neighbors = min(len(city_list) - 1, 3)
    spectral = SpectralClustering(n_clusters=n_clusters, random_state=0, affinity='nearest_neighbors',
                                  n_neighbors=n_neighbors)
    labels = spectral.fit_predict(data)

    # 记录聚类标签
    for city, label in zip(city_list, labels):
        city.cluster_class = label

    # 转换为 DataFrame 进行分析
    df = pd.DataFrame({
        "City": [city.id for city in city_list],
        "Cluster": [city.cluster_class for city in city_list],
        "Theme 1": [city.theme1 for city in city_list],
        "Theme 2": [city.theme2 for city in city_list],
        "Theme 3": [city.theme3 for city in city_list],
        "Theme 4": [city.theme4 for city in city_list]
    })

    # 计算变量贡献度（ANOVA 和 Kruskal-Wallis）
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
    plt.title("Spectral Clustering (PCA Projection)")
    plt.legend(title="Cluster")
    plt.show()

    # 构建 DataFrame
    df = pd.DataFrame({
        "City": city_names,
        "Cluster": labels,
        "Theme 1": [city.theme1 for city in city_list],
        "Theme 2": [city.theme2 for city in city_list],
        "Theme 3": [city.theme3 for city in city_list],
        "Theme 4": [city.theme4 for city in city_list]
    })

    # 决策树分类器
    X = df[["Theme 1", "Theme 2", "Theme 3", "Theme 4"]]
    y = df["Cluster"]
    clf = DecisionTreeClassifier(random_state=0, max_depth=3)  # 限制树深度以提升可解释性
    clf.fit(X, y)

    # 决策树可视化
    plt.figure(figsize=(12, 8))
    plot_tree(clf, feature_names=X.columns, class_names=[str(i) for i in np.unique(y)], filled=True)
    plt.title("Decision Tree Visualization")
    plt.show()


    # 获取特征重要性
    feature_importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": clf.feature_importances_
    }).sort_values(by="Importance", ascending=False)
    # 可视化 1: 特征重要性柱状图
    plt.figure(figsize=(8, 5))
    sns.barplot(x=feature_importance["Importance"], y=feature_importance["Feature"], palette="Blues")
    plt.title("Feature Importance (Decision Tree Analysis)")
    plt.xlabel("Importance Score")
    plt.ylabel("Feature")
    plt.show()

    # 可视化变量分布（箱线图）
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Cluster", y="value", hue="variable",
                data=pd.melt(df, id_vars=["City", "Cluster"], value_vars=["Theme 1", "Theme 2", "Theme 3", "Theme 4"]))
    plt.title("Boxplot of Variables Across Clusters")
    plt.legend(title="Variable")
    plt.show()



    # 可视化变量贡献度（雷达图）
    cluster_means = df.groupby("Cluster").mean(numeric_only=True)
    num_vars = len(cluster_means.columns)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_ylim(0.45, 0.85)  # 设置雷达图的值域
    for idx, row in cluster_means.iterrows():
        ax.plot(angles + [angles[0]], row.tolist() + [row.tolist()[0]], label=f"Cluster {idx}")
    ax.set_xticks(angles)
    ax.set_xticklabels(cluster_means.columns)
    ax.set_title("Radar Chart of Cluster Characteristics")
    ax.legend()
    plt.show()

    return city_list,df, feature_importance


if __name__ == '__main__':
    from Social_segregation.struct.data_reader import data_reader, save_results_to_csv,data_reader_census_tract
    # from visual_analysis_first_paper import plot_city_data_by_class
    from Social_segregation.visual import plot_city_data_combined, plot_city_data_by_cluster,plot_selected_cities

    file_path = r'D:\data\social segregation\SSI\Data\Step2_SSI\NewYork_LocalSSI.csv'

    city_list = data_reader_census_tract(file_path, 3)

    city_list,df_result, importance_result = apply_spectral_clustering(city_list, n_clusters=3)
    print(importance_result)
    #city_list = apply_spectral_clustering(city_list, 3)
    # #plot_city_data_combined(city_list)
    plot_city_data_by_cluster(city_list)
    #save_results_to_csv(city_list, r"D:\Code\Social_segregation\data\SSI_golbal_data_spectral_result.csv")
    #plot_selected_cities(city_list,['Riverside','NewYork'])