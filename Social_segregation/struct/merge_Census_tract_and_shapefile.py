import geopandas as gpd
from data_reader import data_reader_census_tract

def merge_census_tract_and_shapefile(shapefile_path,census_tract_path):
    '''
    读取Shapefile 取得几何数据，读取Census tract的数值，然后合并成geojson
    :param shapefile_path:
    :param census_tract_path:
    :return:
    '''
    # 读取Shapefile
    shapefile = gpd.read_file(shapefile_path)

