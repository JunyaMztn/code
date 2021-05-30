#-------------------------------------------------------------------------------------------
# in:   2 images[jpg]
# proc: Read two jpg images and calculate the absolute difference value of each pixel. (processed for each RGB)
#       Then, generate the absolute difference image.
# out:  Save the absolute difference image[jpg]
# constraint: The image size of the input images must be the same.
#-------------------------------------------------------------------------------------------
from PIL import Image
import numpy as np

# read input image1
img_i1 = Image.open('xxx.jpg')
width, height = img_i1.size

# read input image2
img_i2 = Image.open('yyy.jpg')

# generate output image, that is same image_size of input image
img_o = Image.new('RGB', (width, height))

# store the pixel values of input images to numpy arrays
img_i1_pixels = np.array([[img_i1.getpixel((x,y)) for x in range(width)] for y in range(height)])
img_i2_pixels = np.array([[img_i2.getpixel((x,y)) for x in range(width)] for y in range(height)])

# Access each pixel (each element of the array)
for y in range(height):
  for x in range(width):
    # Store the larger value from the elements of the two arrays to a temporary variable (processed for each RGB)
    rmax,gmax,bmax = np.fmax(img_i1_pixels[y][x], img_i2_pixels[y][x])
    # Store the smaller value from the elements of the two arrays to a temporary variable (processed for each RGB)
    rmin,gmin,bmin = np.fmin(img_i1_pixels[y][x], img_i2_pixels[y][x])
    # Calculate the difference between max and min
    rd = rmax - rmin
    gd = gmax - gmin
    bd = bmax - bmin
    # Store in array
    img_o.putpixel((x,y), (rd,gd,bd))

# Display the image
img_o.show()
# Save the image
img_o.save('zzz.jpg')