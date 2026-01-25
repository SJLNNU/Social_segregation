# 读取原始shapefile文件和经过三分类筛选以后的shapefile文件
# 对比原始OHSA的结果和经过三分类筛选以后的结果。

import geopandas as gpd
import os

def get_feature_count(shapefile_path):
    """
    Reads a Shapefile and returns the total number of features.

    Args:
        shapefile_path (str): Path to the Shapefile.

    Returns:
        int: The number of features, or 0 if an error occurs.
    """
    try:
        gdf = gpd.read_file(shapefile_path)
        return len(gdf)
    except Exception as e:
        print(f"Error reading Shapefile {shapefile_path}: {e}")
        return 0

def get_feature_count_by_attribute(shapefile_path, attribute_name, attribute_value):
    """
    Counts the number of features in a Shapefile with a specific attribute value.

    Args:
        shapefile_path (str): Path to the Shapefile.
        attribute_name (str): The name of the attribute (column).
        attribute_value: The value of the attribute to query.

    Returns:
        int: The number of features matching the query, or 0 if an error occurs.
    """
    try:
        gdf = gpd.read_file(shapefile_path)
        if attribute_name not in gdf.columns:
            print(f"Attribute '{attribute_name}' not found in {shapefile_path}.")
            return 0
        
        count = gdf[gdf[attribute_name] >= attribute_value].shape[0]
        return count
    except Exception as e:
        print(f"Error processing Shapefile {shapefile_path}: {e}")
        return 0





if __name__ == '__main__':
    city_list=['Atlanta','Austin','Baltimore','Boston','Charlotte',
               'Chicago','Cincinnati','Dallas','Denver','Detroit',
               'Houston','LasVegas','LosAngeles','Miami','Minneapolis',
               'NewYork','Orlando','Philadelphia','Phoenix','Pittsburgh',
               'Portland','Riverside','Sacramento','SanAntonio','SanDiego',
               'SanFrancisco','Seattle','StLouis','Tampa','Washington',
               ]


    for city_name in city_list:
        ori_shapefile_path=r'D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_result\{}_census_tract_theme1_OHSA_result.shp'.format(city_name)
        filtered_shapefile_path=r'D:\Code\Social_segregation\data\Overlap_EPSG5070_OHSA_tertile_filter_result\tertile_filtered_{}_summary.shp'.format(city_name)
        ori_feature_count=get_feature_count(ori_shapefile_path)
        filtered_feature_count=get_feature_count_by_attribute(filtered_shapefile_path,'3',1)

        print(city_name,filtered_feature_count,filtered_feature_count/ori_feature_count*100)
    
    # ori_shapefile_path=r'D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_result\{}_census_tract_theme1_OHSA_result.shp'.format(city_name)
    # filtered_shapefile_path=r'D:\Code\Social_segregation\data\Overlap_EPSG5070_OHSA_tertile_filter_result\tertile_filtered_{}_summary.shp'.format(city_name)
    # ori_feature_count=get_feature_count(ori_shapefile_path)
    # filtered_feature_count=get_feature_count_by_attribute(filtered_shapefile_path,'3',0)

    # print(ori_feature_count,filtered_feature_count,filtered_feature_count/ori_feature_count*100)
