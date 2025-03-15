import numpy as np
import matplotlib.pyplot as plt

def create_saturation_mask(hsv_image, lower_threshold=0.05, upper_threshold=1.0, visualize=False):
    """
    Create a saturation mask for leaf detection.
    
    Parameters:
    hsv_image (numpy.ndarray): The input image in HSV color space.
    lower_threshold (float): The lower saturation threshold (default: 0.05).
    upper_threshold (float): The upper saturation threshold (default: 1.0).
    visualize (bool): If True, displays visualizations of the mask (default: False).
    
    Returns:
    numpy.ndarray: The saturation mask.
    """
    # Extract the saturation channel
    saturation = hsv_image[:,:,1]
    
    # Create the mask
    sat_mask = (saturation >= lower_threshold) & (saturation <= upper_threshold)
    
    if visualize:
        # Visualize the original saturation channel
        plt.figure(figsize=(15, 5))
        plt.subplot(131)
        plt.imshow(saturation, cmap='viridis')
        plt.title('Saturation Channel')
        plt.colorbar()
        
        # Visualize the histogram of saturation values
        plt.subplot(132)
        plt.hist(saturation.ravel(), bins=50, range=(0, 1))
        plt.title('Saturation Histogram')
        plt.xlabel('Saturation Value')
        plt.ylabel('Frequency')
        plt.axvline(lower_threshold, color='r', linestyle='dashed', linewidth=2)
        plt.axvline(upper_threshold, color='r', linestyle='dashed', linewidth=2)
        
        # Visualize the saturation mask
        plt.subplot(133)
        plt.imshow(sat_mask, cmap='gray')
        plt.title('Saturation Mask')
        
        plt.tight_layout()
        plt.show()
    
    return sat_mask

# Example usage
if __name__ == "__main__":
    # Assuming we have an HSV image loaded as 'hsv_image'
    # For demonstration, let's create a sample HSV image
    sample_hsv = np.random.rand(100, 100, 3)
    sample_hsv[:,:,1] = np.linspace(0, 1, 100)[:, np.newaxis]  # Create a gradient for saturation
    
    # Create the saturation mask
    mask = create_saturation_mask(sample_hsv, lower_threshold=0.3, upper_threshold=0.8, visualize=True)
    
    print(f"Percentage of pixels in saturation mask: {np.mean(mask) * 100:.2f}%")