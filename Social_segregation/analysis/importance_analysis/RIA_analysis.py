import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def relative_importance_analysis(city_list):
    '''
    进行Relative Importance Analysis (RIA)分析，评估四个主题对themes的贡献度，并以百分比显示在图表中
    :param city_list: list[City] 城市数据
    :return: None (在控制台输出结果)
    '''
    X = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    y = np.array([city.themes for city in city_list])

    model = LinearRegression()
    model.fit(X, y)

    importance = permutation_importance(model, X, y, scoring='r2', random_state=42,n_repeats=30)
    feature_importance = importance.importances_mean

    # 转换为百分比
    total_importance = sum(feature_importance)
    feature_importance_percent = (feature_importance / total_importance) * 100

    feature_names = ["Theme1", "Theme2", "Theme3", "Theme4"]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(feature_names, feature_importance_percent, color=['blue', 'green', 'red', 'purple'])

    # 在柱子上方显示百分比数值
    for bar, percent in zip(bars, feature_importance_percent):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{percent:.2f}%',
                 ha='center', va='bottom', fontsize=12)

    plt.xlabel("Themes")
    plt.ylabel("Relative Importance (%)")
    plt.title("Relative Importance Analysis (RIA)")
    plt.show()

    print("Relative Importance of Each Theme (%):")
    for name, score in zip(feature_names, feature_importance_percent):
        print(f"{name}: {score:.2f}%")

def relative_importance_analysis_with_selected_initclass(city_list, selected_init_class):
    '''
    进行Relative Importance Analysis (RIA)分析，评估四个主题对themes的贡献度，并以百分比显示在图表中
    :param city_list: list[City] 城市数据
    :param selected_init_class: 选定的类别
    :return: None (在控制台输出结果)
    '''
    X = np.array([[city.theme1, city.theme2, city.theme3, city.theme4]
                  for city in city_list if city.init_class == selected_init_class])
    y = np.array([city.themes for city in city_list if city.init_class == selected_init_class])

    if X.shape[0] < 3:  # 设定一个最小样本阈值
        print("Warning: Sample size too small for reliable importance analysis.")
        return

    model = LinearRegression()
    model.fit(X, y)

    importance = permutation_importance(model, X, y, scoring='r2', random_state=42, n_repeats=30)
    feature_importance = np.maximum(importance.importances_mean, 0)  # 归零负值

    # 转换为百分比
    total_importance = sum(feature_importance)
    feature_importance_percent = (feature_importance / total_importance) * 100 if total_importance > 0 else np.zeros_like(feature_importance)

    feature_names = ["Theme1", "Theme2", "Theme3", "Theme4"]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(feature_names, feature_importance_percent, color=['blue', 'green', 'red', 'purple'])

    # 在柱子上方显示百分比数值
    for bar, percent in zip(bars, feature_importance_percent):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{percent:.2f}%',
                 ha='center', va='bottom', fontsize=12)

    plt.xlabel("Themes")
    plt.ylabel("Relative Importance (%)")
    plt.title(f"Relative Importance Analysis (RIA) for Init Class {selected_init_class}")
    plt.show()

    print(f"Relative Importance of Each Theme for Init Class {selected_init_class} (%):")
    for name, score in zip(feature_names, feature_importance_percent):
        print(f"{name}: {score:.2f}%")