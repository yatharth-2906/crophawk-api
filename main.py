import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def load_image(file_path):
    """Load an image and convert it to a numpy array."""
    with Image.open(file_path) as img:
        return np.array(img)

def rgb_to_hsv(rgb):
    """Convert RGB to HSV color space."""
    rgb = rgb.astype('float')
    rgb_max = np.max(rgb, axis=2)
    rgb_min = np.min(rgb, axis=2)
    delta = rgb_max - rgb_min

    v = rgb_max / 255.0
    s = np.where(rgb_max != 0, delta / rgb_max, 0)

    h = np.zeros_like(rgb_max)
    mask = (rgb_max != rgb_min)
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    h[mask & (rgb_max == r)] = (60 * ((g[mask & (rgb_max == r)] - b[mask & (rgb_max == r)]) / delta[mask & (rgb_max == r)]) + 360) % 360
    h[mask & (rgb_max == g)] = (60 * ((b[mask & (rgb_max == g)] - r[mask & (rgb_max == g)]) / delta[mask & (rgb_max == g)]) + 120) % 360
    h[mask & (rgb_max == b)] = (60 * ((r[mask & (rgb_max == b)] - g[mask & (rgb_max == b)]) / delta[mask & (rgb_max == b)]) + 240) % 360

    return np.stack((h, s, v), axis=2)

def create_leaves_mask(hsv_image):
    """Create a binary mask for green-yellow colors (leaves)."""
    h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    # Define color range for green-yellow
    lower_green = 30
    upper_yellow = 180
    
    # Create separate masks for hue, saturation, and value
    hue_mask = (h >= lower_green) & (h <= upper_yellow)
    sat_mask = s > 0.05
    val_mask = v > 0.1
    
    # Combine masks
    mask = hue_mask & sat_mask & val_mask
    
    return mask, hue_mask, sat_mask, val_mask

def calculate_yellowness(hsv_image, leaves_mask):
    """Calculate the yellowness of leaves."""
    h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    # Consider hue values closer to yellow (60 degrees) as more yellow
    # and hue values closer to green (120 degrees) as less yellow
    yellowness = (180 - h[leaves_mask]) / 120  # Normalize to [0, 1]
    yellowness = np.clip(yellowness, 0, 1)  # Ensure values are between 0 and 1
    
    # Adjust yellowness based on saturation and value
    yellowness *= np.sqrt(s[leaves_mask] * v[leaves_mask])  # Reduced influence of saturation and value
    
    return yellowness

def create_yellowness_map(hsv_image, leaves_mask):
    """Create a yellowness map for the entire image."""
    h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    yellowness_map = np.zeros_like(h)
    yellowness_map[leaves_mask] = (180 - h[leaves_mask]) / 120
    yellowness_map = np.clip(yellowness_map, 0, 1)
    
    # Apply Gaussian filter for smoother transitions
    yellowness_map = gaussian_filter(yellowness_map, sigma=1)
    
    return yellowness_map

def display_image(image, title, cmap=None):
    """Display an image using matplotlib."""
    plt.figure(figsize=(10, 8))
    if cmap:
        plt.imshow(image, cmap=cmap)
    else:
        plt.imshow(image)
    plt.title(title)
    plt.colorbar()
    plt.axis('off')
    plt.show()

def analyze_leaf_yellowness(image_path):
    """Analyze the yellowness of leaves in an image."""
    # Load image
    rgb_image = load_image(image_path)
    display_image(rgb_image, "Original Image")
    
    # Convert to HSV
    hsv_image = rgb_to_hsv(rgb_image)
    display_image(hsv_image[:,:,0], "HSV - Hue Channel", cmap='hsv')
    
    # Create leaves mask
    leaves_mask, hue_mask, sat_mask, val_mask = create_leaves_mask(hsv_image)
    
    # Display individual masks for debugging
    display_image(hue_mask, "Hue Mask", cmap='binary')
    display_image(sat_mask, "Saturation Mask", cmap='binary')
    display_image(val_mask, "Value Mask", cmap='binary')
    display_image(leaves_mask, "Combined Leaves Mask", cmap='binary')
    
    # Print mask statistics
    print(f"Percentage of pixels in Hue Mask: {np.mean(hue_mask) * 100:.2f}%")
    print(f"Percentage of pixels in Saturation Mask: {np.mean(sat_mask) * 100:.2f}%")
    print(f"Percentage of pixels in Value Mask: {np.mean(val_mask) * 100:.2f}%")
    print(f"Percentage of pixels in Combined Leaves Mask: {np.mean(leaves_mask) * 100:.2f}%")
    
    # Check if any leaf pixels were detected
    if np.sum(leaves_mask) == 0:
        print("No leaf pixels detected. Please check the individual masks and adjust thresholds.")
        return None
    
    # Calculate yellowness
    yellowness = calculate_yellowness(hsv_image, leaves_mask)
    
    # Create yellowness map
    yellowness_map = create_yellowness_map(hsv_image, leaves_mask)
    display_image(yellowness_map, "Yellowness Map", cmap='YlOrRd')
    
    # Overlay yellowness map on original image
    overlay = rgb_image.copy()
    overlay[leaves_mask] = overlay[leaves_mask] * 0.7 + plt.cm.YlOrRd(yellowness_map[leaves_mask])[:, :3] * 255 * 0.3
    display_image(overlay, "Yellowness Overlay")
    
    return {
        "average_yellowness": np.mean(yellowness),
        "yellowness_distribution": yellowness.tolist()
    }

# Example usage
if __name__ == "__main__":
    image_path = "testplant1.jpeg"  # Replace this with your actual image path
    yellowness_data = analyze_leaf_yellowness(image_path)
    
    if yellowness_data is not None:
        print(f"Average yellowness of the leaves: {yellowness_data['average_yellowness']:.2f}")
        print(f"Number of leaf pixels analyzed: {len(yellowness_data['yellowness_distribution'])}")
        print(f"Yellowness distribution statistics:")
        print(f"  Min: {min(yellowness_data['yellowness_distribution']):.2f}")
        print(f"  Max: {max(yellowness_data['yellowness_distribution']):.2f}")
        print(f"  Median: {np.median(yellowness_data['yellowness_distribution']):.2f}")

        # Plot yellowness distribution
        plt.figure(figsize=(10, 6))
        plt.hist(yellowness_data['yellowness_distribution'], bins=50, edgecolor='black')
        plt.title("Distribution of Leaf Yellowness")
        plt.xlabel("Yellowness (0: Green, 1: Yellow)")
        plt.ylabel("Frequency")
        plt.show()
    else:
        print("Analysis could not be completed due to leaf detection issues.")
        print("Please review the mask images and statistics to adjust detection parameters.")