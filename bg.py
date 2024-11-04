#%%
#Commented code 
import os
from io import BytesIO
from PIL import Image
import requests
from rembg import remove

# Function to download an image from a given URL and return it as a PIL Image object
def download_image(img_url):
    response = requests.get(img_url)  # Send a GET request to the image URL
    img = Image.open(BytesIO(response.content))  # Open the image from the response content
    return img  # Return the image object

# Function to save an image to a specified path
def save_image(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # Create the directory if it doesn't exist
    if img.mode == 'RGBA':  # Convert the image to 'RGB' mode if it is 'RGBA'
        img = img.convert('RGB')
        path = os.path.splitext(path)[0] + '.png'  # Save the image as a PNG file if it was RGBA
    img.save(path)  # Save the image to the specified path

# Function to remove the background from an image using the 'rembg' library
def remove_background(img, alpha_matting=True, alpha_matting_foreground_threshold=50):
    img_byte_arr = BytesIO()  # Create a BytesIO object to hold the image data in memory
    img.save(img_byte_arr, format='PNG')  # Save the image to the BytesIO object in PNG format
    img_byte_arr = img_byte_arr.getvalue()  # Get the image data as a byte array
    subject = remove(img_byte_arr, 
                     alpha_matting=alpha_matting, 
                     alpha_matting_foreground_threshold=alpha_matting_foreground_threshold)  # Remove the background
    return Image.open(BytesIO(subject))  # Return the resulting image as a PIL Image object

# Function to change the background of a foreground image with a new background image from a URL
def change_background(foreground_img, background_img_url):
    background_img = download_image(background_img_url)  # Download the background image
    background_img = background_img.resize(foreground_img.size)  # Resize the background to match the foreground
    background_img.paste(foreground_img, (0, 0), foreground_img)  # Paste the foreground onto the background
    return background_img  # Return the combined image

# Function to display an image on the screen
def display_image(img):
    img.show()  # Display the image using the default image viewer

# URLs of the original image and the new background image
img_url = 'https://nationaltoday.com/wp-content/uploads/2020/12/National-Horse-Day-1-1200x834.jpg'
background_img_url = 'https://img.freepik.com/free-photo/digital-lavender-natural-landscape_23-2150538352.jpg'

# Extract the image name from the URL
img_name = img_url.split('/')[-1]

# Download the original image
original_img = download_image(img_url)
# Save the original image to a folder named 'original'
save_image(original_img, 'original/' + img_name)

# Remove the background from the original image
foreground_img = remove_background(original_img)
# Save the image with the background removed to a folder named 'masked'
save_image(foreground_img, 'masked/' + img_name)

# Change the background of the foreground image to the new background
final_img = change_background(foreground_img, background_img_url)
# Save the final image with the new background
save_image(final_img, 'masked/background.jpg')

# Display the final image
display_image(final_img)
