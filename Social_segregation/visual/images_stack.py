import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 设置图片所在目录和输出大图的文件名
image_folder = r"D:\Code\Social_segregation\data\Jaccard_similarity\heatmaps"  # 修改为你的文件夹路径
output_image_path = r"D:/Code/Social_segregation/merged_heatmap.png"

# 设定拼接方式（5行 × 6列）
rows = 5
cols = 6
total_images = rows * cols  # 需要的图片总数

# 读取所有图片
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
image_files.sort()  # 确保按文件名排序（可调整）

# 确保文件夹内至少有 30 张图片
if len(image_files) < total_images:
    print(f"错误：文件夹内只有 {len(image_files)} 张图片，需要至少 {total_images} 张！")
    exit()

# 读取并调整所有图片大小
images = []
for img_path in image_files[:total_images]:
    img = cv2.imread(img_path)
    img = img[:, :800]  # 保留所有行，但只取前800列
    images.append(img)

# 统一图片大小（取第一张图片的尺寸）
h, w, _ = images[0].shape
images_resized = [cv2.resize(img, (w, h)) for img in images]

# 将图片分割成 5×6 网格
grid = []
for i in range(rows):
    row_images = images_resized[i * cols: (i + 1) * cols]  # 每次取 6 张
    row_concat = np.hstack(row_images)  # 水平拼接
    grid.append(row_concat)

# 竖直拼接所有行
final_image = np.vstack(grid)

# 保存结果
cv2.imwrite(output_image_path, final_image)
print(f"拼接完成！大图已保存至: {output_image_path}")