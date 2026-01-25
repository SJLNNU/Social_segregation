import os
import geopandas as gpd
from pathlib import Path

def convert_geojson_to_shapefile(input_folder: str, output_folder: str):
    """
    Convert all GeoJSON files in the input folder to Shapefiles in the output folder.
    
    Args:
        input_folder (str): Path to the folder containing GeoJSON files
        output_folder (str): Path to the folder where Shapefiles will be saved
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all GeoJSON files from input folder
    input_path = Path(input_folder)
    geojson_files = list(input_path.glob('*.geojson'))
    
    if not geojson_files:
        print(f"No GeoJSON files found in {input_folder}")
        return
    
    # Process each GeoJSON file
    for geojson_file in geojson_files:
        try:
            # Read GeoJSON file
            gdf = gpd.read_file(geojson_file)
            
            # Create output filename (replace .geojson with .shp)
            output_file = Path(output_folder) / f"{geojson_file.stem}.shp"
            
            # Save as Shapefile
            gdf.to_file(output_file)
            print(f"Successfully converted {geojson_file.name} to {output_file.name}")
            
        except Exception as e:
            print(f"Error converting {geojson_file.name}: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_folder = r"D:\Code\Social_segregation\data\Census_tract"  # Replace with your input folder path
    output_folder = r"D:\Code\Social_segregation\data\Census_tract_shp"  # Replace with your output folder path
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    convert_geojson_to_shapefile(input_folder, output_folder)
