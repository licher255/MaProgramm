# image_processor.py
import cv2
import numpy as np

class ImageProcessor:
    """
    Class to handle image processing and compute metrics such as
    localization (centroid) and RMS contrast.
    """
    # Global variables for image dimensions and physical scale
    PIXEL_DIM = (702, 702)       # Image pixel dimensions: (height, width)
    SCALE = (51, 51)             # Physical dimensions in mm (height, width)

    def __init__(self, image_path):
        """
        Initialize the image processor.
        
        Parameters:
        - image_path: string, path to the image file.
        """
        self.image_path = image_path
        self.amplitude_matrix = None  # To store the normalized amplitude matrix
        self.load_image()

    def load_image(self):
        """
        Load the rainbow heatmap image, convert it to grayscale and fully normalize 
        the pixel values to form the amplitude matrix.
        
        The normalization converts the original pixel values to the range [0,1].
        """
        # Read the image in color mode
        img = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(f"Image at {self.image_path} not found.")
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Fully normalize pixel values to range [0, 1]
        self.amplitude_matrix = gray.astype(np.float32) / 255.0

    def compute_localization_error(self):
        """
        Compute the centroid (localization) of the amplitude distribution using:
        
            x_c = sum(x_ij * I_ij) / sum(I_ij)
            y_c = sum(y_ij * I_ij) / sum(I_ij)
        
        Pixel coordinates are then mapped to physical coordinates using the scale.
        
        Returns:
        A tuple (x_c_mm, y_c_mm) representing the centroid in physical units (mm).
        """
        I = self.amplitude_matrix
        M, N = I.shape  # Image dimensions (rows, columns)
        
        # Create coordinate grid (x corresponds to columns, y to rows)
        x_coords = np.arange(N)
        y_coords = np.arange(M)
        X, Y = np.meshgrid(x_coords, y_coords)
        
        total_intensity = np.sum(I)
        if total_intensity == 0:
            return None, None  # Avoid division by zero
        
        # Compute centroid coordinates in pixel units
        x_c = np.sum(X * I) / total_intensity
        y_c = np.sum(Y * I) / total_intensity
        
        # Convert pixel coordinates to physical coordinates in mm
        scale_x = self.SCALE[1] / self.PIXEL_DIM[1]  # width scaling factor
        scale_y = self.SCALE[0] / self.PIXEL_DIM[0]  # height scaling factor
        x_c_mm = x_c * scale_x
        y_c_mm = y_c * scale_y
        
        return x_c_mm, y_c_mm

    def compute_contrast(self):
        """
        Compute the RMS contrast of the image using:
        
            C_RMS = sqrt( (1/MN) * sum[(I_ij - I_mean)^2] )
        
        Returns:
        A float representing the RMS contrast.
        """
        I = self.amplitude_matrix
        M, N = I.shape
        I_mean = np.mean(I)
        contrast = np.sqrt(np.sum((I - I_mean) ** 2) / (M * N))
        return contrast
