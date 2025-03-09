#读取SSI_golbal_data.csv文件
import csv
from data_process.data_struct import  city,census_tract
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import mapping
import json
from shapely.geometry import Point


def data_reader(file_path,init_classes,cluster_file=None):
    '''
    读取合并以后的CSV，返回list[data_process]
    :param file_path:
    :return:
    '''
    city_location_file=r'D:\Code\Social_segregation\data\Location.json'
    with open(city_location_file, 'r') as f:
        city_location_data = json.load(f)

    city_list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            #跳过第一行
            if reader.line_num == 1:
                continue
            cur_city=city(row[0])
            cur_city.latitude=city_location_data[row[0]]['lat']
            cur_city.longitude=city_location_data[row[0]]['lng']
            cur_city.theme1=float(row[1])
            cur_city.theme2=float(row[2])
            cur_city.theme3=float(row[3])
            cur_city.theme4=float(row[4])
            cur_city.themes=float(row[5])

            cur_city.cluster_class = float(row[7])

            city_list.append(cur_city)
        # 按 themes 进行排序
        city_list.sort(key=lambda x: x.themes)
        themes_list = [city.themes for city in city_list]
        q1 = np.percentile(themes_list, 25)  # 25% 分位数
        q2 = np.percentile(themes_list, 50)  # 50% 分位数（中位数）
        q3 = np.percentile(themes_list, 75)  # 75% 分位数

        # 赋值类别
        for cur_city in city_list:
            if cur_city.themes < q1:
                cur_city.init_class = 0  # 低隔离
            elif cur_city.themes < q3:
                cur_city.init_class = 1  # 中等隔离
            else:
                cur_city.init_class = 2  # 高隔离

        # city_names = [city.name for city in city_list]
        # themes_list = [city.themes for city in city_list]

        # plt.figure(figsize=(12, 6))
        # plt.bar(city_names, themes_list, color='skyblue', edgecolor='black', alpha=0.7)

        # # 绘制分位数线
        # plt.axhline(q1, color='r', linestyle='dashed', linewidth=2, label='25% Quantile')
        # plt.axhline(q2, color='g', linestyle='dashed', linewidth=2, label='50% Quantile (Median)')
        # plt.axhline(q3, color='b', linestyle='dashed', linewidth=2, label='75% Quantile')
        #
        # plt.xlabel('City')
        # plt.ylabel('Themes Score')
        # plt.title('Distribution of City Isolation Levels')
        # plt.xticks(rotation=90)
        # plt.legend()
        # plt.grid(axis='y', linestyle='--', alpha=0.7)
        # plt.ylim(0.53, 0.65)
        # plt.show()
        if cluster_file is not None:
            with open(cluster_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    # 跳过第一行
                    if reader.line_num == 1:
                        continue

        return city_list

def read_moran_results(file_path,city_list):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                continue
            city_name=row[0].split('_')[0]
            for cur_city in city_list:
                if cur_city.name == city_name:
                    cur_city.theme1_moran = float(row[1])
                    cur_city.theme2_moran = float(row[2])
                    cur_city.theme3_moran = float(row[3])
                    cur_city.theme4_moran = float(row[4])
                    cur_city.themes_moran=float(row[5])
    return  city_list


def data_reader_census_tract(file_path, init_classes):
    '''
    读取合并以后的CSV，返回list[data_process]
    :param file_path:
    :return:
    '''
    city_list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            #跳过第一行
            if reader.line_num == 1:
                continue
            cur_city = census_tract(int(row[0]))
            cur_city.theme1 = float(row[11])
            cur_city.theme2 = float(row[12])
            cur_city.theme3 = float(row[13])
            cur_city.theme4 = float(row[14])
            cur_city.themes = float(row[15])
            city_list.append(cur_city)
        # 按 themes 进行排序
        city_list.sort(key=lambda x: x.themes)

        themes_list = [city.themes for city in city_list]
        q1 = np.percentile(themes_list, 25)  # 25% 分位数
        q2 = np.percentile(themes_list, 50)  # 50% 分位数（中位数）
        q3 = np.percentile(themes_list, 75)  # 75% 分位数

        # 赋值类别
        for cur_city in city_list:
            if cur_city.themes < q1:
                cur_city.init_class = 0  # 低隔离
            elif cur_city.themes < q3:
                cur_city.init_class = 1  # 中等隔离
            else:
                cur_city.init_class = 2  # 高隔离
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

def save_results_to_csv_census_track(census_tract_list , output_file):
    '''
    保存城市数据到CSV文件
    :param city_list: list[City] 城市数据
    :param output_file: 输出CSV文件路径
    '''
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Theme1", "Theme2", "Theme3", "Theme4", "Themes", "Init_Class", "Cluster_Class"])
        for cur_cencus_tract in census_tract_list:
            writer.writerow([cur_cencus_tract.id, cur_cencus_tract.theme1, cur_cencus_tract.theme2, cur_cencus_tract.theme3, cur_cencus_tract.theme4, cur_cencus_tract.themes, cur_cencus_tract.init_class, cur_cencus_tract.cluster_class])

def associate_shapes(census_tract_list, shapefile_path):
    '''
    读取 shapefile 并将 shape 数据关联到 census_tract_list
    :param census_tract_list: Census Tract 对象列表
    :param shapefile_path: Shapefile 文件路径
    :return: 关联后的 census_tract_list
    '''
    # 读取 shapefile
    gdf = gpd.read_file(shapefile_path)

    # 将 shapefile 数据转换为字典（key: geoid, value: geometry）
    shape_dict = {int(row['GEOID']): row['geometry'] for _, row in gdf.iterrows()}

    # 关联 shape 数据
    for tract in census_tract_list:
        if tract.id in shape_dict:
            tract.shape = shape_dict[tract.id]
    return census_tract_list

def save_census_tracts_to_geojson(census_tract_list, output_file):
    '''
    将 census_tract_list 保存为 GeoJSON 文件
    :param census_tract_list: census_tract 对象列表
    :param output_file: 输出的 GeoJSON 文件路径
    '''
    # 构建 GeoDataFrame 所需的数据
    data = []
    for tract in census_tract_list:
        if tract.shape:  # 确保 shape 存在
            data.append({
                "id": tract.id,
                "theme1": tract.theme1,
                "theme2": tract.theme2,
                "theme3": tract.theme3,
                "theme4": tract.theme4,
                "themes": tract.themes,
                "init_class": tract.init_class,
                "cluster_class": tract.cluster_class,
                "geometry": tract.shape  # 这里 shape 仍然是 Shapely Polygon
            })

    # 创建 GeoDataFrame（geometry 直接使用 Shapely Polygon）
    gdf = gpd.GeoDataFrame(data, geometry=[d["geometry"] for d in data])

    # 保存为 GeoJSON
    gdf.to_file(output_file, driver="GeoJSON")
    print(f"✅ GeoJSON 文件已成功保存至: {output_file}")

def save_city_location(city_list, output_file,init_class=None,cluster_class=None):
    """
    保存城市的经纬度到Geojson点坐标的形式
    :param city_list:
    :param output_file:
    :param init_class:
    :param cluster_class:
    :return:
    """
    #读取城市列表，根据init_class 和cluster_class , 保存结果到Geojson
    data = []
    for city in city_list:
        if (init_class is None or city.init_class == init_class) and \
                (cluster_class is None or city.cluster_class == cluster_class):
            data.append({
                "name": city.name,
                "theme1": city.theme1,
                "theme2": city.theme2,
                "theme3": city.theme3,
                "theme4": city.theme4,
                "themes": city.themes,
                "init_class": city.init_class,
                "cluster_class": city.cluster_class,
                "geometry": Point(city.longitude, city.latitude)
            })
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # 保存为GeoJSON
    gdf.to_file(output_file, driver="GeoJSON")
    print(f"✅ 城市位置GeoJSON文件已成功保存至: {output_file}")

if __name__ == '__main__':
    #file_path = r"../data/SSI_golbal_data.csv"
    #city_list = data_reader(file_path,3)
    save_file_path=r'../data/city_location_morans_cluster.geojson'

    # from analysis.importance_analysis.Importance_analysis import relative_importance_analysis,relative_importance_analysis_with_selected_initclass
    # relative_importance_analysis(city_list)
    # relative_importance_analysis_with_selected_initclass(city_list,0)
    # relative_importance_analysis_with_selected_initclass(city_list,1)
    # relative_importance_analysis_with_selected_initclass(city_list,2)
    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data_moran_kmeans_result.csv"
    #moran_results_path = r'D:\Code\Social_segregation\data\morans_i_results.csv'

    city_list = data_reader(file_path, 3)
    #city_list = read_moran_results(moran_results_path, city_list)
    save_city_location(city_list, save_file_path)



    #relative_importance_analysis(census_tract_list)
    # relative_importance_analysis_with_selected_initclass(census_tract_list,0)
    # relative_importance_analysis_with_selected_initclass(census_tract_list,1)
    # relative_importance_analysis_with_selected_initclass(census_tract_list,2)

    # city_name='Minneapolis'
    # file_path=r'D:\data\social segregation\SSI\Data\Step2_SSI\{}_LocalSSI.csv'.format(city_name)
    # shapefile_path=r'D:\data\social segregation\SSI\Data\Shapefiles\Shapefiles\{}_MSA_CT.shp'.format(city_name)
    # census_tract_list=data_reader_census_tract(file_path, 3)
    # census_tract_list=associate_shapes(census_tract_list, shapefile_path)
    # save_census_tracts_to_geojson(census_tract_list,'../data/Census_tract/{}_census_tract.geojson'.format(city_name))