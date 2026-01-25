import geopandas as gpd
import os
from pathlib import Path
import pandas as pd

# Dictionary mapping input shapefile names to full names
name_mapping = {
    'Atlanta_MSA_CT': 'Atlanta-Sandy Springs-Alpharetta',
    'Austin_MSA_CT': 'Austin-Round Rock-Georgetown',
    'Baltimore_MSA_CT': 'Baltimore-Columbia-Towson',
    'Boston_MSA_CT': 'Boston-Cambridge-Newton',
    'Charlotte_MSA_CT': 'Charlotte-Concord-Gastonia',
    'Chicago_MSA_CT': 'Chicago-Naperville-Elgin',
    'Cincinnati_MSA_CT': 'Cincinnati',
    'Dallas_MSA_CT': 'Dallas-Fort Worth-Arlington',
    'Denver_MSA_CT': 'Denver-Aurora-Lakewood',
    'Detroit_MSA_CT': 'Detroit-Warren-Dearborn',
    'Houston_MSA_CT': 'Houston-The Woodlands-Sugar Land',
    'LasVegas_MSA_CT': 'Las Vegas-Henderson-Paradise',
    'LosAngeles_MSA_CT': 'Los Angeles-Long Beach-Anaheim',
    'Minneapolis_MSA_CT': 'Minneapolis-St. Paul-Bloomington',
    'Miami_MSA_CT': 'Miami-Fort Lauderdale-Pompano Beach',
    'NewYork_MSA_CT': 'New York-Newark-Jersey City',
    'Orlando_MSA_CT': 'Orlando-Kissimmee-Sanford',
    'Philadelphia_MSA_CT': 'Philadelphia-Camden-Wilmington',
    'Phoenix_MSA_CT': 'Phoenix-Mesa-Chandler',
    'Pittsburgh_MSA_CT': 'Pittsburgh',
    'Portland_MSA_CT': 'Portland-Vancouver-Hillsboro',
    'Riverside_MSA_CT': 'Riverside-San Bernardino-Ontario',
    'Sacramento_MSA_CT': 'Sacramento-Roseville-Folsom',
    'SanAntonio_MSA_CT': 'San Antonio-New Braunfels',
    'SanDiego_MSA_CT': 'San Diego-Chula Vista-Carlsbad',
    'SanFrancisco_MSA_CT': 'San Francisco-Oakland-Berkeley',
    'Seattle_MSA_CT': 'Seattle-Tacoma-Bellevue',
    'StLouis_MSA_CT': 'St. Louis',
    'Tampa_MSA_CT': 'Tampa-St. Petersburg-Clearwater',
    'Washington_MSA_CT': 'Washington-Arlington-Alexandria'
}

def process_shapefiles(input_dir, output_dir):
    """
    Process all shapefiles in the input directory:
    1. Merge each shapefile into a single polygon
    2. Rename according to the mapping
    3. Save to output directory
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all shapefiles in the input directory
    shapefiles = [f for f in os.listdir(input_dir) if f.endswith('.shp')]
    
    for shapefile in shapefiles:
        # Get the short name (remove .shp extension)
        short_name = os.path.splitext(shapefile)[0]
        
        if short_name in name_mapping:
            # Read the shapefile
            gdf = gpd.read_file(os.path.join(input_dir, shapefile))
            
            # Merge all geometries into a single polygon
            merged = gdf.unary_union
            
            # Create a new GeoDataFrame with the merged geometry
            merged_gdf = gpd.GeoDataFrame(geometry=[merged], crs=gdf.crs)
            
            # Get the new name
            new_name = name_mapping[short_name]
            
            # Save the merged shapefile with the new name
            output_path = os.path.join(output_dir, f"{new_name}.shp")
            merged_gdf.to_file(output_path)
            print(f"Processed {short_name} -> {new_name}")
        else:
            print(f"Warning: No mapping found for {short_name}")

def merge_all_shapefiles(input_dir, output_path):
    """
    Merge all shapefiles in the input directory into a single shapefile.
    Each feature will have 'city_name' (full name) and 'short_name' attributes.
    
    Args:
        input_dir (str): Directory containing the shapefiles
        output_path (str): Path where the merged shapefile will be saved
    """
    # Get all shapefiles in the input directory
    shapefiles = [f for f in os.listdir(input_dir) if f.endswith('.shp')]
    
    # List to store all GeoDataFrames
    gdfs = []
    
    for shapefile in shapefiles:
        # Get the short name (remove .shp extension)
        short_name = os.path.splitext(shapefile)[0]
        
        if short_name in name_mapping:
            # Read the shapefile
            gdf = gpd.read_file(os.path.join(input_dir, shapefile))
            
            # Merge all geometries into a single polygon
            merged = gdf.unary_union
            
            # Create a new GeoDataFrame with the merged geometry
            merged_gdf = gpd.GeoDataFrame(geometry=[merged], crs=gdf.crs)
            
            # Add city name columns
            merged_gdf['city_name'] = name_mapping[short_name]  # Full name
            merged_gdf['short_name'] = short_name.replace('_MSA_CT', '')  # Short name
            
            # Add to list
            gdfs.append(merged_gdf)
            print(f"Processed {short_name} -> {name_mapping[short_name]}")
    
    # Concatenate all GeoDataFrames
    if gdfs:
        final_gdf = pd.concat(gdfs, ignore_index=True)
        
        # Save the merged shapefile
        final_gdf.to_file(output_path)
        print(f"Successfully merged all shapefiles into {output_path}")
    else:
        print("No shapefiles were processed")

if __name__ == "__main__":
    # Specify your input and output directories
    input_directory = r"D:\data\social segregation\SSI\Data\Shapefiles\Shapefiles"  # Replace with your input directory
    output_directory = r"D:\data\social segregation\SSI\Data\Shapefiles\Merged_shapefile"  # Replace with your output directory
    
    # Process individual shapefiles
    # process_shapefiles(input_directory, output_directory)
    
    # Merge all shapefiles into one
    merged_save_fold=r'D:\data\social segregation\SSI\Data\Shapefiles'
    merged_output_path = os.path.join(merged_save_fold, "all_cities_merged.shp")
   

    merge_all_shapefiles(input_directory, merged_output_path)
