from PIL import Image
import os

def stitch_images(image_paths, output_path):
    """
    将四张相同大小的图片拼接成一个2x2的网格图。

    参数:
        image_paths (list): 包含四张图片路径的列表。
                            顺序应为：左上、右上、左下、右下。
        output_path (str): 拼接后图片的保存路径。
    """
    try:
        images = [Image.open(p) for p in image_paths]
    except FileNotFoundError as e:
        print(f"错误: {e}。一个或多个图片文件未找到。")
        print("请确保图片文件存在于指定的路径。")
        return

    # 假设所有图片的尺寸都相同，从第一张图片获取尺寸
    width, height = images[0].size

    # 创建一个新的2x2网格大小的图片
    new_image = Image.new('RGB', (width * 2, height * 2))

    # 将四张图片粘贴到新图片中
    new_image.paste(images[0], (0, 0))
    new_image.paste(images[1], (width, 0))
    new_image.paste(images[2], (0, height))
    new_image.paste(images[3], (width, height))

    # 保存新图片
    new_image.save(output_path)
    print(f"拼接后的图片已保存到 {output_path}")

if __name__ == "__main__":
    # 定义图片名称和输出路径
    # 请确保这些图片与脚本位于同一目录中，
    # 或者提供完整的路径。
    image_names = ['Theme1.png', 'Theme2.png', 'Theme3.png', 'Theme4.png']
    output_filename = 'stitched_themes.png'

    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 创建图片的完整路径
    image_paths = [os.path.join(script_dir, name) for name in image_names]
    output_path = os.path.join(script_dir, output_filename)
    
    # 在尝试拼接之前，检查图片文件是否存在
    missing_files = [path for path in image_paths if not os.path.exists(path)]
    
    if missing_files:
        print("以下图片文件缺失:")
        for f in missing_files:
            print(f" - {os.path.basename(f)}")
        print("\n请将图片文件添加到脚本所在目录，或者在脚本中更新路径。")
    else:
        # To run this script, you need to install the Pillow library.
        # You can install it by running: pip install Pillow
        try:
            from PIL import Image
        except ImportError:
            print("错误: Pillow 库未安装。")
            print("请通过运行 'pip install Pillow' 来安装。")
            exit()
        stitch_images(image_paths, output_path) 