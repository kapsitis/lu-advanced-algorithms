from PIL import Image
import numpy as np

def getPixelData(filename):
    image = Image.open(filename)   
    image = image.convert('RGB') 
    width, height = image.size 

    pixel_values = []

    for y in range(height):          # For each pixel in image
        row = []
        for x in range(width):
            RGB = image.getpixel((x,y))  # Get RGB values for pixel
            row.append(RGB)
        pixel_values.append(row)     # Add row to pixel_values

    return pixel_values              # Return list of pixel RGB values


# The YIQ color model is used in the NTSC (National Television System Committee) 
# color TV system. In this system, Y ranges between 0 and 1, I ranges between 
# -0.5957 and 0.5957 and Q ranges between -0.5226 and 0.5226.
def RGBtoYIQ(rgb):
    r, g, b = rgb
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    y = 0.299 * r + 0.587 * g + 0.114 * b
    i = 0.5959 * r - 0.2746 * g - 0.3213 * b
    q = 0.2115 * r - 0.5227 * g + 0.3112 * b
    i = max(min(i, 0.5957), -0.5957)
    q = max(min(q, 0.5226), -0.5226)
    return (y, i, q)


def projectYIQ(yiq, pos): 
    y, i, q = yiq
    if pos == 0: 
        return (y, 0, 0)
    elif pos == 1: 
        return (0.5, 1*i, 0)
    else: 
        return (0.5, 0, q)

def YIQtoRGB(yiq):
    y, i, q = yiq
    r = y + 0.956*i + 0.619*q
    g = y - 0.272*i - 0.647*q
    b = y - 1.106*i + 1.703*q 
    r = max(min(round(r*255.0), 255), 0)
    g = max(min(round(g*255.0), 255), 0)
    b = max(min(round(b*255.0), 255), 0)
    return (r, g, b)

def writeAsPNG(matrix):
    imageArray = np.random.rand(100,100)
    # Izmaina mērogu uz [0;255] melnbaltā attēlā "255" ir balts
    img = Image.fromarray(imageArray * 255)
    # Eksportē uz PNG failu
    img.convert('RGB').save('raster_output.png')


def createPNG(arr, fileName):
    flat_list = [item for sublist in arr for item in sublist]
    width = len(arr[0])
    height = len(arr)
    img = Image.new('RGB', (width, height))
    img.putdata(flat_list)
    img.save(fileName, compress_level=9)


def main(): 
    arr = getPixelData('kuldiga.png')
    for j in range(len(arr)):
        for i in range(len(arr[0])):
            triple = arr[j][i]
            arr[j][i] = YIQtoRGB(projectYIQ(RGBtoYIQ(triple), 0))

    for j in range(6):
        for i in range(8):
            print(arr[50*j][50*i], end=', ')
        print() 
    
    createPNG(arr, 'kuldiga1.png')


if __name__ == '__main__':
    main()