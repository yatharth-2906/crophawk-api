import numpy as np
from PIL import Image
from scipy.spatial import Delaunay
from scipy.signal import convolve2d
from scipy.ndimage import label
import matplotlib.pyplot as plt

def load_image(file_path):
    """Load an image and convert it to a numpy array."""
    with Image.open(file_path) as img:
        return np.array(img)

def rgb_to_hsv(rgb):
    """Convert RGB to HSV color space."""
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    r, g, b = r/255.0, g/255.0, b/255.0
    
    cmax = np.max(rgb, axis=2)
    cmin = np.min(rgb, axis=2)
    diff = cmax - cmin
    
    h = np.zeros_like(cmax)
    s = np.zeros_like(cmax)
    v = cmax
    
    # Hue calculation
    h[cmax == r] = (60 * ((g[cmax == r] - b[cmax == r]) / diff[cmax == r] + 0) + 360) % 360
    h[cmax == g] = (60 * ((b[cmax == g] - r[cmax == g]) / diff[cmax == g] + 2) + 360) % 360
    h[cmax == b] = (60 * ((r[cmax == b] - g[cmax == b]) / diff[cmax == b] + 4) + 360) % 360
    
    # Saturation calculation
    s[cmax != 0] = diff[cmax != 0] / cmax[cmax != 0]
    
    return np.stack((h, s, v), axis=-1)

def create_leaves_mask(hsv_image):
    """Create a binary mask for green-yellow colors (leaves)."""
    h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    # Define color range for green-yellow
    lower_green = 60
    upper_yellow = 90
    
    mask = (h >= lower_green) & (h <= upper_yellow) & (s > 0.1) & (v > 0.1)
    return mask

def create_triangulated_mask(mask, num_points=1000):
    """Create a triangulated mask based on the input binary mask."""
    y, x = np.where(mask)
    points = np.column_stack((x, y))
    
    if len(points) > num_points:
        indices = np.random.choice(len(points), num_points, replace=False)
        points = points[indices]
    
    corners = np.array([[0, 0], [0, mask.shape[0]-1], [mask.shape[1]-1, 0], [mask.shape[1]-1, mask.shape[0]-1]])
    points = np.vstack((points, corners))
    
    tri = Delaunay(points)
    
    y, x = np.indices(mask.shape)
    triangulated_mask = tri.find_simplex(np.column_stack((x.ravel(), y.ravel()))) != -1
    triangulated_mask = triangulated_mask.reshape(mask.shape)
    
    return triangulated_mask

def detect_edges(image):
    """Detect edges using a simple Sobel filter."""
    gray = np.mean(image, axis=2)  # Convert to grayscale
    
    # Sobel filters
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    # Apply filters
    gx = np.abs(convolve2d(gray, sobel_x, mode='same', boundary='symm'))
    gy = np.abs(convolve2d(gray, sobel_y, mode='same', boundary='symm'))
    
    # Combine gradients
    edges = np.sqrt(gx**2 + gy**2)
    
    # Normalize and threshold
    edges = (edges - edges.min()) / (edges.max() - edges.min())
    edge_mask = edges > 0.1  # Adjust threshold as needed
    
    return edge_mask, gray

def calculate_leaves_yellowness(hsv_image, triangulated_mask, edge_mask):
    """Calculate the yellowness of leaves edges."""
    h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    # Combine triangulated and edge masks
    leaf_edges = triangulated_mask & edge_mask
    
    if np.sum(leaf_edges) == 0:
        return {"average": 0, "distribution": []}  # No leaf edges detected
    
    # Consider hue values closer to yellow (60 degrees) as more yellow
    yellowness = 1 - abs(h[leaf_edges] - 60) / 30  # Normalize to [0, 1]
    
    # Increase yellowness for higher saturation and value
    yellowness *= s[leaf_edges] * v[leaf_edges]
    
    return {
        "average": np.mean(yellowness),
        "distribution": yellowness.tolist()
    }

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

def detect_leaves_yellowness(image_path):
    """Detect the yellowness of leaves edges in an image using triangulated masks."""
    # Load image
    rgb_image = load_image(image_path)
    display_image(rgb_image, "Original Image")
    
    # Convert to HSV
    hsv_image = rgb_to_hsv(rgb_image)
    display_image(hsv_image[:,:,0], "HSV - Hue Channel", cmap='hsv')
    
    # Create initial leaves mask
    leaves_mask = create_leaves_mask(hsv_image)
    display_image(leaves_mask, "Leaves Mask", cmap='binary')
    
    # Create triangulated mask
    triangulated_mask = create_triangulated_mask(leaves_mask)
    display_image(triangulated_mask, "Triangulated Mask", cmap='binary')
    
    # Detect edges
    edge_mask, gray_image = detect_edges(rgb_image)
    display_image(gray_image, "Grayscale Image", cmap='gray')
    display_image(edge_mask, "Edge Mask", cmap='binary')
    
    # Calculate leaves yellowness
    yellowness_data = calculate_leaves_yellowness(hsv_image, triangulated_mask, edge_mask)
    
    # Visualize final result
    final_mask = triangulated_mask & edge_mask
    final_result = rgb_image.copy()
    final_result[~final_mask] = [0, 0, 0]  # Set non-leaf-edge pixels to black
    display_image(final_result, "Final Result - Leaf Edges")
    
    return yellowness_data

# Example usage
if __name__ == "__main__":
    image_path = "testplant1.jpeg"  # Replace this with your actual image path
    yellowness_data = detect_leaves_yellowness(image_path)
    print(f"Average yellowness of the leaves edges: {yellowness_data['average']:.2f}")
    print(f"Number of edge pixels analyzed: {len(yellowness_data['distribution'])}")
    print(f"Yellowness distribution statistics:")
    print(f"  Min: {min(yellowness_data['distribution']):.2f}")
    print(f"  Max: {max(yellowness_data['distribution']):.2f}")
    print(f"  Median: {np.median(yellowness_data['distribution']):.2f}")

    # Plot yellowness distribution
    plt.figure(figsize=(10, 6))
    plt.hist(yellowness_data['distribution'], bins=50, edgecolor='black')
    plt.title("Distribution of Leaf Edge Yellowness")
    plt.xlabel("Yellowness")
    plt.ylabel("Frequency")
    plt.show()