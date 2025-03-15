
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from flask import Flask, request, jsonify, render_template
import io
import base64

app = Flask(__name__)

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
    
    lower_green = 30
    upper_yellow = 180
    
    hue_mask = (h >= lower_green) & (h <= upper_yellow)
    sat_mask = s > 0.05
    val_mask = v > 0.1
    
    mask = hue_mask & sat_mask & val_mask
    
    return mask

def calculate_yellowness(hsv_image, leaves_mask):
    """Calculate the yellowness of leaves."""
    h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    yellowness = (180 - h[leaves_mask]) / 120
    yellowness = np.clip(yellowness, 0, 1)
    
    yellowness *= np.sqrt(s[leaves_mask] * v[leaves_mask])
    
    return yellowness

def create_yellowness_map(hsv_image, leaves_mask):
    """Create a yellowness map for the entire image."""
    h, s, v = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    
    yellowness_map = np.zeros_like(h)
    yellowness_map[leaves_mask] = (180 - h[leaves_mask]) / 120
    yellowness_map = np.clip(yellowness_map, 0, 1)
    
    yellowness_map = gaussian_filter(yellowness_map, sigma=1)
    
    return yellowness_map

def analyze_leaf_yellowness(image):
    """Analyze the yellowness of leaves in an image."""
    rgb_image = np.array(image)
    
    hsv_image = rgb_to_hsv(rgb_image)
    
    leaves_mask = create_leaves_mask(hsv_image)
    
    yellowness = calculate_yellowness(hsv_image, leaves_mask)
    
    yellowness_map = create_yellowness_map(hsv_image, leaves_mask)
    
    overlay = rgb_image.copy()
    overlay[leaves_mask] = overlay[leaves_mask] * 0.7 + plt.cm.YlOrRd(yellowness_map[leaves_mask])[:, :3] * 255 * 0.3
    
    original_base64 = image_to_base64(rgb_image)
    overlay_base64 = image_to_base64(overlay)
    
    return {
        "average_yellowness": float(np.mean(yellowness)),
        "min_yellowness": float(np.min(yellowness)),
        "max_yellowness": float(np.max(yellowness)),
        "median_yellowness": float(np.median(yellowness)),
        "original_image": original_base64,
        "overlay_image": overlay_base64
    }

def image_to_base64(image_array):
    img = Image.fromarray(image_array.astype('uint8'))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def analyze_leaf_yellowness(image):
    """Analyze the yellowness of leaves in an image and suggest possible nutrient deficiencies."""
    rgb_image = np.array(image)
    
    hsv_image = rgb_to_hsv(rgb_image)
    
    leaves_mask = create_leaves_mask(hsv_image)
    
    yellowness = calculate_yellowness(hsv_image, leaves_mask)
    
    yellowness_map = create_yellowness_map(hsv_image, leaves_mask)
    
    overlay = rgb_image.copy()
    overlay[leaves_mask] = overlay[leaves_mask] * 0.7 + plt.cm.YlOrRd(yellowness_map[leaves_mask])[:, :3] * 255 * 0.3
    
    original_base64 = image_to_base64(rgb_image)
    overlay_base64 = image_to_base64(overlay)
    
    avg_yellowness = float(np.mean(yellowness))
    
    # Determine possible nutrient deficiencies based on yellowness
    deficiencies = determine_deficiencies(avg_yellowness)
    
    return {
        "average_yellowness": avg_yellowness,
        "min_yellowness": float(np.min(yellowness)),
        "max_yellowness": float(np.max(yellowness)),
        "median_yellowness": float(np.median(yellowness)),
        "original_image": original_base64,
        "overlay_image": overlay_base64,
        "possible_deficiencies": deficiencies
    }

def determine_deficiencies(yellowness):
    """Determine possible nutrient deficiencies based on yellowness level."""
    deficiencies = []
    
    if yellowness < 0.3:
        deficiencies.append({
            "nutrient": "None",
            "description": "The leaves appear healthy with no significant yellowing.",
            "recommendation": "Continue with current nutrient management practices."
        })
    elif 0.3 <= yellowness < 0.5:
        deficiencies.append({
            "nutrient": "Nitrogen",
            "description": "Mild yellowing may indicate early stages of nitrogen deficiency.",
            "recommendation": "Consider applying a balanced fertilizer with higher nitrogen content."
        })
    elif 0.5 <= yellowness < 0.7:
        deficiencies.extend([
            {
                "nutrient": "Iron",
                "description": "Moderate yellowing with green veins may suggest iron deficiency.",
                "recommendation": "Apply iron chelates or iron sulfate to the soil or as a foliar spray."
            },
            {
                "nutrient": "Magnesium",
                "description": "Yellowing between leaf veins could indicate magnesium deficiency.",
                "recommendation": "Apply Epsom salts (magnesium sulfate) to the soil or as a foliar spray."
            }
        ])
    else:
        deficiencies.extend([
            {
                "nutrient": "Sulfur",
                "description": "Severe yellowing throughout the leaf may indicate sulfur deficiency.",
                "recommendation": "Apply sulfur-containing fertilizers or elemental sulfur to the soil."
            },
            {
                "nutrient": "Severe Nitrogen Deficiency",
                "description": "Extreme yellowing and stunted growth suggest severe nitrogen deficiency.",
                "recommendation": "Immediately apply high-nitrogen fertilizer and consider soil testing for a comprehensive nutrient analysis."
            }
        ])
    
    return deficiencies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        image = Image.open(file.stream)
        result = analyze_leaf_yellowness(image)
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


