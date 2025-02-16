import matplotlib.pyplot as plt
import random

def plot_city_data_combined(city_list):
    '''
    在一张图中可视化 init_class 和 cluster_class
    '''
    init_colors = ['g', 'y', 'r', 'purple', 'black']
    random.seed(42)
    cluster_colors = {i: f'#{random.randint(0x100000, 0xFFFFFF):06x}' for i in
                      set(city.cluster_class for city in city_list) if i is not None}
    plt.figure(figsize=(10, 6))
    for city in city_list:
        plt.plot([1, 2, 3, 4],
                 [city.theme1, city.theme2, city.theme3, city.theme4],
                 marker='o', linestyle='-',
                 color=init_colors[city.init_class],
                 alpha=0.7, label=f'Init {city.init_class}' if city_list.index(city) == 0 else "")
        plt.plot([1, 2, 3, 4],
                 [city.theme1, city.theme2, city.theme3, city.theme4],
                 marker='s', linestyle='--',
                 color=cluster_colors[city.cluster_class],
                 alpha=0.7)

    plt.xlabel('Themes')
    plt.ylabel('Values')
    plt.title('City Theme Data by Init and Cluster Class')
    plt.xticks([1, 2, 3, 4], ['Theme1', 'Theme2', 'Theme3', 'Theme4'])
    plt.show()


def plot_city_data_by_cluster(city_list):
    '''
    按 cluster_class 进行单独可视化，颜色使用 init_class 配色
    '''
    init_colors = ['g', 'y', 'r',  'purple', 'black']
    unique_clusters = sorted(set(city.cluster_class for city in city_list if city.cluster_class is not None))

    all_values = [value for city in city_list for value in [city.theme1, city.theme2, city.theme3, city.theme4]]
    y_min, y_max = min(all_values), max(all_values)

    for cluster_id in unique_clusters:
        plt.figure()
        plt.title(f'City Theme Data - Cluster {cluster_id}')

        for city in city_list:
            if city.cluster_class == cluster_id:
                plt.plot([1, 2, 3, 4],
                         [city.theme1, city.theme2, city.theme3, city.theme4],
                         marker='o', linestyle='-', color=init_colors[city.init_class],
                         alpha=0.7)

        plt.xlabel('Themes')
        plt.ylabel('Values')
        plt.xticks([1, 2, 3, 4], ['Theme1', 'Theme2', 'Theme3', 'Theme4'])
        plt.ylim(y_min, y_max)
        plt.show()


def plot_selected_cities(city_list, selected_cities):
    '''
    可视化选定城市的四个主题曲线图，使用不同颜色
    :param city_list: list[City] 城市数据
    :param selected_cities: list[str] 选定的城市名称
    '''
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # 颜色列表
    plt.figure(figsize=(10, 6))

    for idx, city in enumerate(city_list):
        if city.name in selected_cities:
            plt.plot([1, 2, 3, 4],
                     [city.theme1, city.theme2, city.theme3, city.theme4],
                     marker='o', linestyle='-', color=colors[idx % len(colors)],
                     alpha=0.7, label=city.name)

    plt.xlabel('Themes')
    plt.ylabel('Values')
    plt.title('Comparison of Selected Cities by Themes')
    plt.xticks([1, 2, 3, 4], ['Theme1', 'Theme2', 'Theme3', 'Theme4'])
    plt.legend()
    plt.show()
