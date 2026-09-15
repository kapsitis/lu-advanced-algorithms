from PIL import Image, ImageDraw
import imageio

# Create a white square image
image_size = 256
white_image = Image.new("RGB", (image_size, image_size), "white")

# Draw a red circle in the middle
draw = ImageDraw.Draw(white_image)
circle_radius = 50
circle_center = (image_size // 2, image_size // 2)
draw.ellipse(
    [
        (circle_center[0] - circle_radius, circle_center[1] - circle_radius), 
        (circle_center[0] + circle_radius, circle_center[1] + circle_radius)
    ], 
    fill="red"
)

import pillow_avif
white_image.save("output.avif", format="AVIF")
print("Image saved as output.avif")