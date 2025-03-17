# main.py
import numpy as np
from image_processor import ImageProcessor

def localization_error(gt_coord, hm_coord):
    """
    Compute the Euclidean distance between the ground truth centroid and
    the heatmap centroid.
    
    Parameters:
    - gt_coord: tuple, (x, y) coordinates of ground truth centroid.
    - hm_coord: tuple, (x, y) coordinates of heatmap centroid.
    
    Returns:
    The localization error in mm.
    """
    if gt_coord[0] is None or hm_coord[0] is None:
        return None
    return np.sqrt((gt_coord[0] - hm_coord[0]) ** 2 + (gt_coord[1] - hm_coord[1]) ** 2)

if __name__ == '__main__':
    # Create ImageProcessor instances for the ground truth and heatmap images.

    gt_processor = ImageProcessor('pic_rec/gt2.png', image_type='ground_truth')
    heatmap1_processor = ImageProcessor('pic_rec/ice.png', image_type='heatmap')
    heatmap2_processor = ImageProcessor('pic_rec/water.png', image_type='heatmap')

    # Compute centroids (localization) for each image.
    gt_loc = gt_processor.compute_localization_error()
    hm1_loc = heatmap1_processor.compute_localization_error()
    hm2_loc = heatmap2_processor.compute_localization_error()

    # Calculate the localization errors (Euclidean distances) between ground truth and each heatmap.
    error1 = localization_error(gt_loc, hm1_loc)
    error2 = localization_error(gt_loc, hm2_loc)
    
    # Print the localization errors.
    print("Localization error for heatmap 1: {:.2f} mm".format(error1))
    print("Localization error for heatmap 2: {:.2f} mm".format(error2))
    
    # Optionally, compute and print the RMS contrast for each image.
    print("Contrast for ground truth: {:.4f}".format(gt_processor.compute_contrast()))
    print("Contrast for heatmap 1: {:.4f}".format(heatmap1_processor.compute_contrast()))
    print("Contrast for heatmap 2: {:.4f}".format(heatmap2_processor.compute_contrast()))
