import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def add_patch_to_image(img_path, save_path=None, patch_length=100, real_size=10, show=False, save=True):
    """给单张图片添加尺度标注，可选择显示和/或保存"""
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')

    img_height, img_width = img.shape[0], img.shape[1]

    # 尺度线位置
    start_point = (img_width * 0.80, img_height * 0.99)
    end_point = (start_point[0] + patch_length, start_point[1])

    # 绘制线条
    line = patches.FancyArrowPatch(start_point, end_point,
                                   arrowstyle='-',
                                   linewidth=2,
                                   color='black')
    ax.add_patch(line)

    # 添加文本
    mid_point_x = (start_point[0] + end_point[0]) / 2 - 25
    mid_point_y = start_point[1] - 5
    ax.text(mid_point_x, mid_point_y, f'{real_size} mm',
            color='black', fontsize=12, ha='center', va='bottom')

    plt.tight_layout()

    if save and save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"已保存到: {save_path}")

    if show:
        plt.show()
    else:
        plt.close()

def batch_process_images(folder_path):
    """批量处理文件夹内所有符合规则的PNG图片"""
    patch_length1 = 103
    real_size1 = 20
    patch_length2 = 101
    real_size2 = 40

    output_folder = os.path.join(folder_path, 'add_patch')
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith('.png') and filename.startswith('geo'):
            img_path = os.path.join(folder_path, filename)

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
    img_path = '20250408-Variation-Geo\\crop\\geo1-1ice.png'
    save_path = "20250408-Variation-Geo\\label\\geo1-1ice.png"
    patch_length = 103
    real_size = 20

    # 显示图像，同时保存
    add_patch_to_image(img_path, save_path, patch_length, real_size, show=True, save=False)
