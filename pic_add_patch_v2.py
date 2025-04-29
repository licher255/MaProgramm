import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

def add_patch_to_image(img_path, save_path, patch_length=101, real_size=40):
    """Add a scale bar to a single image and save it."""
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')  # Turn off axes

    img_height, img_width = img.shape[0], img.shape[1]

    # Define start and end points for the scale bar
    start_point = (img_width * 0.85, img_height * 0.95)
    end_point = (start_point[0] + patch_length, start_point[1])

    # Draw the scale bar
    line = patches.FancyArrowPatch(start_point, end_point,
                                   arrowstyle='-',
                                   linewidth=2,
                                   color='black')
    ax.add_patch(line)

    # Add scale text label
    mid_point_x = (start_point[0] + end_point[0]) / 2
    mid_point_y = start_point[1] - 2  # Slightly above the line
    ax.text(mid_point_x, mid_point_y, f'{real_size} mm',
            color='black', fontsize=12, ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def batch_process_images(folder_path):
    """Batch process all PNG images in the given folder (no subfolders)."""
    output_folder = os.path.join(folder_path, 'add_patch')
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            img_path = os.path.join(folder_path, filename)
            save_path = os.path.join(output_folder, filename)
            add_patch_to_image(img_path, save_path)
            print(f"Processed: {filename}")

if __name__ == '__main__':
    folder_path = '20250411-Variation-3D Stoff/StainSteel347'
    batch_process_images(folder_path)
