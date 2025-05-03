import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def add_patch_to_image(img_path, save_path, patch_length, real_size):
    """给单张图片添加尺度标注，并保存到指定位置"""
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')

    img_height, img_width = img.shape[0], img.shape[1]

    # 尺度线位置
    start_point = (img_width * 0.85, img_height * 0.95)
    end_point = (start_point[0] + patch_length, start_point[1])

    # 绘制线条
    line = patches.FancyArrowPatch(start_point, end_point,
                                   arrowstyle='-',
                                   linewidth=2,
                                   color='black')
    ax.add_patch(line)

    # 添加文本
    mid_point_x = (start_point[0] + end_point[0]) / 2
    mid_point_y = start_point[1] - 5  # 稍微上移一点
    ax.text(mid_point_x, mid_point_y, f'{real_size} mm',
            color='black', fontsize=12, ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def batch_process_images(folder_path):
    """批量处理文件夹内所有符合规则的PNG图片"""
    # 参数设定
    patch_length1 = 103
    real_size1 = 20
    patch_length2 = 101
    real_size2 = 40

    output_folder = os.path.join(folder_path, 'add_patch')
    os.makedirs(output_folder, exist_ok=True)

    # 遍历所有PNG文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') and filename.startswith('geo'):
            img_path = os.path.join(folder_path, filename)

            # 根据名字选择不同参数
            if filename.startswith(('geo1', 'geo2', 'geo3', 'geo4')):
                patch_length = patch_length1
                real_size = real_size1
            elif filename.startswith(('geo5', 'geo6', 'geo7')):
                patch_length = patch_length2
                real_size = real_size2
            else:
                print(f"跳过不符合规则的文件: {filename}")
                continue

            save_path = os.path.join(output_folder, filename)
            add_patch_to_image(img_path, save_path, patch_length, real_size)
            print(f"处理完成: {filename}")

if __name__ == '__main__':
    folder_path = '20250408-Variation-Geo'
    batch_process_images(folder_path)
