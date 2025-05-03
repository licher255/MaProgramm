import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def add_patch_to_image(img_path, save_path=None,
                       patch_length=100, real_size=10,
                       show=False, save=True):
    """给单张图片添加尺度标注，可选择显示和/或保存"""
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')

    img_height, img_width = img.shape[0], img.shape[1]

    # 尺度线位置：右下角
    start_point = (img_width * 0.83, img_height * 0.99)
    end_point = (start_point[0] + patch_length, start_point[1])

    # 绘制线条
    line = patches.FancyArrowPatch(start_point, end_point,
                                   arrowstyle='-',
                                   linewidth=2,
                                   color='black')
    ax.add_patch(line)

    # 添加文本
    mid_x = (start_point[0] + end_point[0]) / 2
    ax.text(mid_x, start_point[1],
            f'{real_size} mm',
            color='black', fontsize=14,
            ha='center', va='bottom')

    plt.tight_layout()

    if save and save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"已保存: {save_path}")

    if show:
        plt.show()
    else:
        plt.close()


def batch_process_images(base_folder):
    """
    批量处理 base_folder/crop 下的所有 PNG 图像，
    并将结果保存在 base_folder/label 下。
    """
    # 1. 定义参数
    # patch_length1, real_size1 针对 geo1–4
    patch_length1, real_size1 = 52, 10
    # patch_length2, real_size2 针对 geo5–7
    patch_length2, real_size2 = 54, 20

    crop_folder = os.path.join(base_folder, 'crop')
    label_folder = os.path.join(base_folder, 'label')

    os.makedirs(label_folder, exist_ok=True)

    for fname in os.listdir(crop_folder):
        if not fname.lower().endswith('.png'):
            continue

        img_path = os.path.join(crop_folder, fname)

        # 根据文件名前缀选择尺度
        if fname.startswith(('geo1', 'geo2', 'geo3', 'geo4')):
            patch_length, real_size = patch_length1, real_size1
        elif fname.startswith(('geo5', 'geo6', 'geo7')):
            patch_length, real_size = patch_length2, real_size2
        else:
            print(f"跳过（不符合命名规则）: {fname}")
            continue

        save_path = os.path.join(label_folder, fname)
        add_patch_to_image(img_path, save_path,
                           patch_length, real_size,
                           show=False, save=True)
        print(f"处理完成: {fname}")


if __name__ == '__main__':
    # 指定主文件夹路径（不含 crop/label 后缀）
    base_dir = r'20250408-Variation-Geo'
    batch_process_images(base_dir)
