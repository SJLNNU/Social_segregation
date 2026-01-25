import matplotlib.pyplot as plt
from Social_segregation.struct.data_reader import data_reader

colors = ['g', 'y', 'r', 'c', 'm', 'y', 'k']  # 颜色列表，按类别分配

def plot_city_data(city_list):
    '''
    可视化城市数据，不同类别使用不同颜色
    '''
    #colors = ['g', 'b', 'r', 'c', 'm', 'y', 'k']  # 颜色列表，按类别分配
    class_labels = set()  # 记录已经添加到图例的类别

    for city in city_list:
        class_label = f'Class {city.init_class}'
        if class_label not in class_labels:
            plt.plot([1, 2, 3, 4],
                     [city.theme1, city.theme2, city.theme3, city.theme4],
                     marker='o', linestyle='-', color=colors[city.init_class % len(colors)],
                     alpha=0.7, label=class_label)
            class_labels.add(class_label)  # 记录该类别已添加
        else:
            plt.plot([1, 2, 3, 4],
                     [city.theme1, city.theme2, city.theme3, city.theme4],
                     marker='o', linestyle='-', color=colors[city.init_class % len(colors)],
                     alpha=0.7)

    plt.xlabel('Themes')
    plt.ylabel('Values')
    plt.title('City Theme Data by Class')
    plt.xticks([1, 2, 3, 4], ['Theme1', 'Theme2', 'Theme3', 'Theme4'])
    plt.legend()
    plt.show()


def plot_city_data_by_class(city_list):
    '''
    分类别单独展示数据，保持相同的值域范围
    '''
    #colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # 颜色列表，按类别分配
    unique_classes = sorted(set(city.init_class for city in city_list))

    # 获取全局的值域范围
    all_values = [value for city in city_list for value in [city.theme1, city.theme2, city.theme3, city.theme4]]
    y_min, y_max = min(all_values), max(all_values)

    for class_id in unique_classes:
        plt.figure()
        plt.title(f'City Theme Data - Class {class_id}')

        for city in city_list:
            if city.init_class == class_id:
                plt.plot([1, 2, 3, 4],
                         [city.theme1, city.theme2, city.theme3, city.theme4],
                         marker='o', linestyle='-', color=colors[class_id % len(colors)],
                         alpha=0.7)
        plt.xlabel('Themes')
        plt.ylabel('Values')
        plt.xticks([1, 2, 3, 4], ['Theme1', 'Theme2', 'Theme3', 'Theme4'])
        plt.ylim(y_min, y_max)  # 统一Y轴范围
        plt.show()

if __name__ == '__main__':
    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
    city_list = data_reader(file_path, 3)
    plot_city_data(city_list)
    plot_city_data_by_class(city_list)