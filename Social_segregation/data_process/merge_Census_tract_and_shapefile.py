import geopandas as gpd
from data_reader import data_reader_census_tract,associate_shapes,save_census_tracts_to_geojson

city_name = 'LosAngeles'
file_path = r'D:\data\social segregation\SSI\Data\Step2_SSI\{}_LocalSSI.csv'.format(city_name)
shapefile_path = r'D:\data\social segregation\SSI\Data\Shapefiles\Shapefiles\{}_MSA_CT.shp'.format(city_name)
census_tract_list = data_reader_census_tract(file_path, 3)
census_tract_list = associate_shapes(census_tract_list, shapefile_path)
save_census_tracts_to_geojson(census_tract_list, '../data/Census_tract/{}_census_tract.geojson'.format(city_name))
