import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def add_patch_to_image(img_path, save_path, patch_length=54, real_size=20):
    """Add a scale bar to a single image and save it."""
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')  # Turn off axes

    img_height, img_width = img.shape[:2]

    # Define start and end points for the scale bar
    start_point = (img_width * 0.83, img_height * 0.99)
    end_point = (start_point[0] + patch_length, start_point[1])

    # Draw the scale bar
    line = patches.FancyArrowPatch(
        start_point, end_point,
        arrowstyle='-', linewidth=2, color='black'
    )
    ax.add_patch(line)

    # Add scale text label
    mid_x = (start_point[0] + end_point[0]) / 2
    mid_y = start_point[1] - 2  # Slightly above the line
    ax.text(mid_x, mid_y, f'{real_size} mm',
            color='black', fontsize=14,
            ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def batch_process_images(folder_path, patch_length=54, real_size=20):
    """
    Batch process images under:
      folder_path\crop  -> input
      folder_path\label -> output
    """
    crop_folder = os.path.join(folder_path, 'crop')
    label_folder = os.path.join(folder_path, 'label')
    os.makedirs(label_folder, exist_ok=True)

    for fname in os.listdir(crop_folder):
        if not fname.lower().endswith('.png'):
            continue

        img_path = os.path.join(crop_folder, fname)
        save_path = os.path.join(label_folder, fname)

        add_patch_to_image(
            img_path, save_path,
            patch_length=patch_length,
            real_size=real_size
        )
        print(f"Processed and saved: {save_path}")


if __name__ == '__main__':
    # 只需修改这一行，指向你的主目录
    base_dir = r'20250507-Variation-3D Stoff-closedDefect'
    batch_process_images(base_dir)
    
    #img_path= "20250507-Variation-3D Stoff-closedDefect\crop\AlIce-airDefect.png"
    #save_path = "20250507-Variation-3D Stoff-closedDefect\label\AlIce-airDefect.png"
    #add_patch_to_image(img_path, save_path, patch_length=54, real_size=20)
