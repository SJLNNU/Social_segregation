from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier,export_text,plot_tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


def apply_decision_tree_analysis(city_list, n_clusters):
    '''
    使用 K-Means 进行聚类，并使用决策树分析特征重要性
    :param city_list: list[City] 城市数据
    :param n_clusters: 期望的聚类数量
    :return: 更新 city.cluster_class, 并返回数据分析结果
    '''
    data = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    city_names = [city.id for city in city_list]

    # KMeans 聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
    labels = kmeans.fit_predict(data)

    for city, label in zip(city_list, labels):
        city.cluster_class = label

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
#决策树可视化
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

    # 可视化 2: PCA 降维后散点图
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=reduced_data[:, 0], y=reduced_data[:, 1], hue=labels, palette="Set2", s=100)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.title("K-Means Clustering (PCA Projection)")
    plt.legend(title="Cluster")
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
    return city_list, df, feature_importance
if __name__ == '__main__':
    from Social_segregation.struct.data_reader import data_reader,save_results_to_csv,data_reader_census_tract
    #from visual_analysis_first_paper import plot_city_data_by_class
    from Social_segregation.visual import plot_city_data_combined,plot_city_data_by_cluster

    file_path = r'D:\data\social segregation\SSI\Data\Step2_SSI\NewYork_LocalSSI.csv'
    city_list = data_reader_census_tract(file_path,3)
    city_list,df, importance_df= apply_decision_tree_analysis(city_list, 3)
    plot_city_data_by_cluster(city_list)
    print(importance_df)

# Census Tract Level
# 30 个城市 ，可视化+莫兰指数
#