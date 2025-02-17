#读取SSI_golbal_data.csv文件
import csv
from Social_segregation.struct.data_struct import city
import matplotlib.pyplot as plt

def data_reader(file_path,init_classes):
    '''
    读取合并以后的CSV，返回list[data_struct]
    :param file_path:
    :return:
    '''
    city_list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cur_city=city(row[0])
            cur_city.theme1=float(row[1])
            cur_city.theme2=float(row[2])
            cur_city.theme3=float(row[3])
            cur_city.theme4=float(row[4])
            cur_city.themes=float(row[5])
            city_list.append(cur_city)
        # 按 themes 进行排序
        city_list.sort(key=lambda x: x.themes)

        # 计算每个类别的边界索引
        total_cities = len(city_list)
        class_size = total_cities // init_classes

        # 赋值类别
        for i, cur_city in enumerate(city_list):
            cur_city.init_class = min(i // class_size, init_classes - 1)
        return city_list

def save_results_to_csv(city_list, output_file):
    '''
    保存城市数据到CSV文件
    :param city_list: list[City] 城市数据
    :param output_file: 输出CSV文件路径
    '''
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["City", "Theme1", "Theme2", "Theme3", "Theme4", "Themes", "Init_Class", "Cluster_Class"])
        for city in city_list:
            writer.writerow([city.name, city.theme1, city.theme2, city.theme3, city.theme4, city.themes, city.init_class, city.cluster_class])




if __name__ == '__main__':
    file_path = r"../data/SSI_golbal_data.csv"
    city_list = data_reader(file_path,3)
    from Social_segregation.analysis.importance_analysis.RIA_analysis import relative_importance_analysis,relative_importance_analysis_with_selected_initclass
    relative_importance_analysis_with_selected_initclass(city_list,0)
    relative_importance_analysis_with_selected_initclass(city_list,1)
    relative_importance_analysis_with_selected_initclass(city_list,2)

    #relative_importance_analysis(city_list)

