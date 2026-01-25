from PIL import Image, ImageDraw, ImageFont
import os

def stitch_images(image_paths, output_path, labels):
    """
    将四张相同大小的图片拼接成一个2x2的网格图,并在每张图的左下角添加标签。

    参数:
        image_paths (list): 包含四张图片路径的列表。
                            顺序应为：左上、右上、左下、右下。
        output_path (str): 拼接后图片的保存路径。
        labels (list): 对应四张图片的标签列表。
    """
    try:
        # 打开图片并转换为RGBA模式，以便在其上绘制带透明度的内容
        images = [Image.open(p).convert("RGBA") for p in image_paths]
    except FileNotFoundError as e:
        print(f"错误: {e}。一个或多个图片文件未找到。")
        print("请确保图片文件存在于指定的路径。")
        return
    except Exception as e:
        print(f"打开图片时发生错误: {e}")
        return

    processed_images = []
    for i, img in enumerate(images):
        draw = ImageDraw.Draw(img)
        
        # 字体设置
        font_path = "C:/Windows/Fonts/calibri.ttf"  # Calibri 字体路径
        try:
            # 动态设置字体大小，例如图片高度的5%
            font_size = int(img.height * 0.05)
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"字体 '{font_path}' 未找到。将使用默认字体。")
            font_size = int(img.height * 0.05)
            try:
                # 尝试加载带大小的默认字体
                font = ImageFont.load_default(size=font_size)
            except AttributeError:
                 # 兼容旧版Pillow
                font = ImageFont.load_default()

        text = labels[i]
        
        # 计算文本位置（左下角）
        padding = int(img.height * 0.02)  # 2% 的边距
        try:
            # 使用 textbbox 获取精确的文本边界框
            bbox = draw.textbbox((0, 0), text, font=font)
            text_height = bbox[3] - bbox[1]
            position = (padding, img.height - text_height - bbox[1] - padding)
        except (AttributeError, TypeError):
            # 兼容旧版Pillow的 textsize
            text_width, text_height = draw.textsize(text, font=font)
            position = (padding, img.height - text_height - padding)

        # 为文字添加黑色描边以提高可见性
        stroke_color = "black"
        stroke_width = 0
        x, y = position
        for dx in [-stroke_width, 0, stroke_width]:
            for dy in [-stroke_width, 0, stroke_width]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=stroke_color)

        # 在顶部绘制黑色的主文字
        draw.text(position, text, font=font, fill="black")

        # 将图片转换回RGB模式并添加到列表中
        processed_images.append(img.convert("RGB"))
    
    images = processed_images
    width, height = images[0].size

    # 创建一个新的2x2网格大小的图片
    new_image = Image.new('RGB', (width * 2, height * 2))

    # 将四张图片粘贴到新图片中
    new_image.paste(images[0], (0, 0))
    new_image.paste(images[1], (width, 0))
    new_image.paste(images[2], (0, height))
    new_image.paste(images[3], (width, height))

    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir:
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")

    # 保存新图片
    new_image.save(output_path)
    print(f"拼接后的图片已保存到 {output_path}")

if __name__ == "__main__":
    # --- 请在这里配置您的路径 ---
    # 包含 'Theme1.png' 到 'Theme4.png' 的文件夹路径
    # 例如: r"D:\path\to\your\images"
    # 或者使用相对路径: "images"
    image_folder = r"D:\Files\jianguoyun\Files\Paper\Social Segregation\作图\V2\OHSA_Tertile_filter" 

    # 拼接后图片的完整保存路径, 包括文件名
    # 例如: r"D:\path\to\output\stitched_image.png"
    output_path = r"D:\Files\jianguoyun\Files\Paper\Social Segregation\作图\V3\stitched_themes.png"
    # --- 配置结束 ---

    # 定义图片名称和标签
    image_names = ['Theme1.png', 'Theme2.png', 'Theme3.png', 'Theme4.png']
    labels = ["SES", "HCD", "MSL", "H&T"]
    
    # 创建图片的完整路径
    image_paths = [os.path.join(image_folder, name) for name in image_names]
    
    # 在尝试拼接之前，检查图片文件夹和文件是否存在
    if not os.path.isdir(image_folder):
        print(f"错误: 图片文件夹不存在: {image_folder}")
        print("\n请在脚本中更新 'image_folder' 变量为您正确的图片文件夹路径。")
    else:
        missing_files = [path for path in image_paths if not os.path.exists(path)]
        if missing_files:
            print(f"在文件夹 '{image_folder}' 中，以下图片文件缺失:")
            for f in missing_files:
                print(f" - {os.path.basename(f)}")
            print("\n请确保所有图片文件都在指定的文件夹中。")
        else:
            # 要运行此脚本，您需要安装 Pillow 库。
            # 您可以通过运行以下命令来安装: pip install Pillow
            try:
                from PIL import Image, ImageDraw, ImageFont
            except ImportError:
                print("错误: Pillow 库未安装。")
                print("请通过运行 'pip install Pillow' 来安装。")
                exit()
            
            stitch_images(image_paths, output_path, labels) 