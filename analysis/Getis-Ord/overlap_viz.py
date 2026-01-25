import os
import json
import geopandas as gpd

# 设定文件夹路径（示例路径，需替换为实际路径）
base_path = r"D:\Code\Social_segregation\data\Z_score_Corrected"  # 你的数据所在路径
folders = [
    "Getis_Ord_theme1_Results",
    "Getis_Ord_theme2_Results",
    "Getis_Ord_theme3_Results",
    "Getis_Ord_theme4_Results",
    #"Getis_Ord_themes_Results"
]

# 存储每个城市的数据
data_by_city = {}

# 遍历所有主题文件夹
for folder in folders:
    folder_path = os.path.join(base_path, folder)
    for filename in os.listdir(folder_path):
        if filename.endswith(".geojson"):
            city_name = filename.replace("_census_tract_getis_ord_results.geojson", "")
            file_path = os.path.join(folder_path, filename)

            # 读取 GeoJSON 文件
            with open(file_path, "r") as f:
                geojson_data = json.load(f)

            # 初始化城市数据
            if city_name not in data_by_city:
                data_by_city[city_name] = {}

            # 遍历所有 Census Tract
            for feature in geojson_data["features"]:
                tract_id = feature["properties"].get("id")
                if tract_id not in data_by_city[city_name]:
                    data_by_city[city_name][tract_id] = {
                        "Coldspot_90%": 0, "Coldspot_95%": 0, "Coldspot_99%": 0,
                        "Hotspot_90%": 0, "Hotspot_95%": 0, "Hotspot_99%": 0,
                        "geometry": feature["geometry"]
                    }

                # 计算冷点（coldspot）
                for conf in ["90%", "95%", "99%"]:
                    data_by_city[city_name][tract_id][f"Coldspot_{conf}"] += int(
                        feature["properties"].get(f"{folder.split('_')[-2]}_coldspot_{conf}", False))

                # 计算热点（hotspot）
                for conf in ["90%", "95%", "99%"]:
                    data_by_city[city_name][tract_id][f"Hotspot_{conf}"] += int(
                        feature["properties"].get(f"{folder.split('_')[-2]}_hotspot_{conf}", False))

# 生成新的 GeoJSON 文件
output_folder = os.path.join(base_path, "Processed_Results")
os.makedirs(output_folder, exist_ok=True)

for city, tracts in data_by_city.items():
    output_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for tract_id, data in tracts.items():
        feature = {
            "type": "Feature",
            "properties": {
                "Coldspot_90%": data["Coldspot_90%"],
                "Coldspot_95%": data["Coldspot_95%"],
                "Coldspot_99%": data["Coldspot_99%"],
                "Hotspot_90%": data["Hotspot_90%"],
                "Hotspot_95%": data["Hotspot_95%"],
                "Hotspot_99%": data["Hotspot_99%"]
            },
            "geometry": data["geometry"]
        }
        output_geojson["features"].append(feature)

    # 保存文件
    output_path = os.path.join(output_folder, f"{city}_processed.geojson")
    with open(output_path, "w") as f:
        json.dump(output_geojson, f)
    print(f"Processed file saved: {output_path}")