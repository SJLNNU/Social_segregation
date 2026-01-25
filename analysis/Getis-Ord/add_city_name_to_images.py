from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def add_city_name_to_image(image_path, city_name, output_path):
    """
    Add city name to the upper right corner of an image.
    
    Parameters:
    -----------
    image_path : str
        Path to input image
    city_name : str
        Name of the city to add
    output_path : str
        Path to save the modified image
    """
    # Open the image
    img = Image.open(image_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    
    # Set font (using default font with size 36)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    # Calculate text size
    text_bbox = draw.textbbox((0, 0), city_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate position (upper right corner with padding)
    padding = 20
    x = img.width - text_width - padding
    y = padding
    
    # Add text with white color and black outline for better visibility
    # Draw black outline
    for offset_x in [-2, 2]:
        for offset_y in [-2, 2]:
            draw.text((x + offset_x, y + offset_y), city_name, font=font, fill='black')
    
    # Draw white text
    draw.text((x, y), city_name, font=font, fill='white')
    
    # Save the modified image
    img.save(output_path)

def process_directory(input_dir, output_dir, city_names):
    """
    Process all images in a directory and add city names.
    
    Parameters:
    -----------
    input_dir : str
        Directory containing input images
    output_dir : str
        Directory to save modified images
    city_names : dict
        Dictionary mapping image filenames to city names
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all images in the input directory
    for image_path in Path(input_dir).glob('*.png'):  # Adjust extension if needed
        # Get city name for this image
        city_name = city_names.get(image_path.stem, "Unknown City")
        
        # Create output filename
        output_filename = f"labeled_{image_path.name}"
        output_path = os.path.join(output_dir, output_filename)
        
        # Add city name to image
        add_city_name_to_image(str(image_path), city_name, output_path)
        print(f"Processed {image_path.name} -> {output_filename}")

if __name__ == "__main__":
    # Example usage
    input_directory = r"D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_tertile_filter_result"
    output_directory = r"D:\Code\Social_segregation\data\Census_tract_shp_EPSG5070_OHSA_tertile_filter_result_labeled"
    
    # Dictionary mapping image filenames to city names
    # Modify this dictionary according to your image filenames and corresponding city names
    city_names = {
        "tertile_filtered_Atlanta": "Atlanta",
        "tertile_filtered_Boston": "Boston",
        # Add more mappings as needed
    }
    
    process_directory(input_directory, output_directory, city_names) 