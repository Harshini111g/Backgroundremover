import os
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import requests
from rembg import remove

# Function to download an image from a given URL and return it as a PIL Image object
def download_image(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    return img

# Function to save an image to a specified path
def save_image(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
        path = os.path.splitext(path)[0] + '.png'
    img.save(path)

# Function to remove the background from an image using the 'rembg' library
def remove_background(img, alpha_matting=True, alpha_matting_foreground_threshold=50):
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    subject = remove(img_byte_arr, alpha_matting=alpha_matting, alpha_matting_foreground_threshold=alpha_matting_foreground_threshold)
    return Image.open(BytesIO(subject))

# Function to adjust the opacity of the image
def adjust_opacity(img, opacity):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    alpha = img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    img.putalpha(alpha)
    return img

# Function to apply a blur effect to the image
def apply_blur(img, blur_radius):
    return img.filter(ImageFilter.GaussianBlur(blur_radius))

# Main function to process the image with user input for URL, opacity, and blur
def process_image(img_url, opacity, blur_radius):
    # Download the original image
    original_img = download_image(img_url)
    
    # Remove the background
    foreground_img = remove_background(original_img)
    
    # Adjust the opacity (0.0 - fully transparent, 1.0 - fully opaque)
    foreground_img = adjust_opacity(foreground_img, opacity)
    
    # Apply blur (0 - no blur, higher values increase blur)
    foreground_img = apply_blur(foreground_img, blur_radius)
    
    # Save the processed image
    img_name = img_url.split('/')[-1]
    save_image(foreground_img, 'output/' + img_name)
    
    return foreground_img

# Example usage
if __name__ == '__main__':
    img_url = 'https://nationaltoday.com/wp-content/uploads/2020/12/National-Horse-Day-1-1200x834.jpg'
    opacity = 0.8  # Example value for opacity (0.0 to 1.0)
    blur_radius = 5  # Example value for blur (0 for no blur)
    
    final_image = process_image(img_url, opacity, blur_radius)
    final_image.show()  # Display the final image
