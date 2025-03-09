import geopandas as gpd
import random
import json
from shapely.geometry import Point, LineString


def generate_mobility_data(input_geojson, output_geojson, connection_ratio=0.3, num_intermediate_points=10):
    # 读取Census Tract GeoJSON
    gdf = gpd.read_file(input_geojson)

    # 计算几何中心
    gdf['centroid'] = gdf.geometry.centroid

    # 获取所有几何中心点
    centroids = gdf['centroid'].tolist()

    # 计算需要连接的点数
    num_connections = int(len(centroids) * connection_ratio)

    # 随机选择点进行连接
    mobility_lines = []
    for j in range(num_connections):
        p1, p2 = random.sample(centroids, 2)

        # 生成多个中间点
        intermediate_points = []
        for i in range(1, num_intermediate_points + 1):
            fraction = i / (num_intermediate_points + 1)
            intermediate_x = p1.x + fraction * (p2.x - p1.x)
            intermediate_y = p1.y + fraction * (p2.y - p1.y)
            intermediate_points.append(Point(intermediate_x, intermediate_y))

        # 生成折线
        line = LineString([p1] + intermediate_points + [p2])
        mobility_lines.append({
            "type": "Feature",
            "geometry": json.loads(gpd.GeoSeries([line]).to_json())['features'][0]['geometry'],
            "properties": {"Index":j}
        })

    # 生成GeoJSON结构
    mobility_geojson = {
        "type": "FeatureCollection",
        "features": mobility_lines
    }

    # 保存到GeoJSON文件
    with open(output_geojson, 'w') as f:
        json.dump(mobility_geojson, f, indent=4)

    print(f"Mobility data saved to {output_geojson}")


# 示例用法
#generate_mobility_data('census_tracts.geojson', 'mobility_data.geojson')

# 示例用法
generate_mobility_data(r'D:\Code\Social_segregation\data\Getis_Ord\Processed_Results\NewYork_processed.geojson',r'New_york_simi.geojson',0.01 )
