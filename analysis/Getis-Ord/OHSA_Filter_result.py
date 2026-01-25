# 通过三分类法将OHSA结果进行分类，所有被定义为OHSA定义为热点的区域，需要满足值大于三分类法中的前33.33%
# 所有被定义为OHSA定义为冷点的区域，需要满足值小于三分类法中的后33.33%

import geopandas as gpd
import numpy as np
import os
from pathlib import Path

def process_shapefile(input_shapefile, output_shapefile):
    """
    Process a shapefile to filter OHSA results based on tercile thresholds.
    
    Parameters:
    -----------
    input_shapefile : str
        Path to input shapefile
    output_shapefile : str
        Path to save output shapefile
    """
    # Read the shapefile
    gdf = gpd.read_file(input_shapefile)
    
    # Get all theme columns
    theme_cols = [col for col in gdf.columns if col.startswith('theme')]
    
    # Create a mask for valid features
    valid_mask = np.ones(len(gdf), dtype=bool)
    
    # Process each theme column
    for theme_col in theme_cols:
        # Calculate tercile thresholds
        lower_threshold = np.percentile(gdf[theme_col], 33.33)
        upper_threshold = np.percentile(gdf[theme_col], 66.66)
        
        # Create masks for hotspots and coldspots
        hotspot_mask = (gdf['Gi_Bin'] > 0) & (gdf[theme_col] > upper_threshold)
        coldspot_mask = (gdf['Gi_Bin'] < 0) & (gdf[theme_col] < lower_threshold)
        
        # Update valid mask
        valid_mask = valid_mask & (hotspot_mask | coldspot_mask)
    
    # Filter the GeoDataFrame
    filtered_gdf = gdf[valid_mask]
    
    # Save the filtered results
    filtered_gdf.to_file(output_shapefile)

def batch_process_directory(input_dir, output_dir):
    """
    Batch process all shapefiles in a directory.
    
    Parameters:
    -----------
    input_dir : str
        Directory containing input shapefiles
    output_dir : str
        Directory to save output shapefiles
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all shapefiles in the input directory
    for shapefile in Path(input_dir).glob('*.shp'):
        # Create output filename
        output_filename = f"tertile_filtered_{shapefile.name}"
        output_path = os.path.join(output_dir, output_filename)
         
        # Process the shapefile
        process_shapefile(str(shapefile), output_path)
        print(f"Processed {shapefile.name} -> {output_filename}")

if __name__ == "__main__":
    # Example usage
    input_directory = r"D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_result"
    output_directory = r"D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_tertile_filter_result"
    batch_process_directory(input_directory, output_directory)


