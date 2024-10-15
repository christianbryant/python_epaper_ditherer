from PIL import Image, ImageOps, ImageFilter
import numpy as np
import struct
import os
import shutil


rotate = False

# Define the color palette
color_palette = [
    (0, 0, 0),       # Black
    (255, 255, 255),  # White
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 0, 0),   # Red
    (255, 255, 0),   # Yellow
    (255, 128, 0)    # Orange
]

palette = [
    0, 0, 0,       # Black
    255, 255, 255,  # White
    0, 255, 0,   # Green
    0, 0, 255,   # Blue
    255, 0, 0,   # Red
    255, 255, 0,   # Yellow
    255, 128, 0   # Orange
]

colors = [
    "black",
    "white",
    "green",
    "blue",
    "red",
    "yellow",
    "orange"
]

def convert_image_2_dithered(image, rotate):
    # Open the input image
    input_image = Image.open(image).convert('RGB')
    resized_image = input_image.copy()
    if rotate:
            resized_image = resized_image.transpose(Image.ROTATE_90)
    resized_image.thumbnail((600, 448), Image.LANCZOS)
    p_img = Image.new('P', resized_image.size)
    p_img.putpalette(palette)
    quantized_image = resized_image.quantize(palette=p_img)
    dithered_image = quantized_image.convert('P')
    os.chdir(f"../Images/{image.replace('.png', '')}")
    dithered_image.save("dithered.png")
def convert_image_2_7_colors(name, image):
    # Open the input image
    input_image = Image.open(image)
    input_image = input_image.convert('RGB')

    # Find each color in the image, create an new image for only that color and save it
    current_color = 0
    for color in color_palette:
        new_image = Image.new('1', input_image.size)
        for x in range(input_image.size[0]):
            for y in range(input_image.size[1]):
                r, g, b = input_image.getpixel((x,y))
                if (r, g, b) == color:
                    new_image.putpixel((x,y), 0)
                else:
                    new_image.putpixel((x,y), 1)
        os.chdir("jpgs")
        new_image.save(str(colors[current_color]) + ".jpg", dpi=[300,300], quality=95)
        os.chdir("..")
        os.chdir("bmp")
        new_image.save(str(colors[current_color]) + ".bmp")
        os.chdir("..")

        convert_bmp_to_binary("./bmp/" + str(colors[current_color]) + ".bmp", name)
        current_color += 1
    shutil.rmtree("bmp")
    print("Images saved successfully.")

# Binary for the win :)
def convert_bmp_to_binary(bmp_file, name):
    bmp = Image.open(bmp_file).convert('1')

    image_data = list(bmp.getdata())

    with open (name + ".bin", "ab") as file:
        bit_list = []

        bit_index = 8
        byte_counter = 0

        for x in range(0, len(image_data)):
            bit_value = 0 if image_data[x] > 0 else 1

            bit_list.append(bit_value)
            bit_index -= 1

            if bit_index == 0:
                byte = 0
                for bit in bit_list:
                    byte = (byte << 1) | bit
                byte_data = byte.to_bytes(1, byteorder='big')
                file.write(byte_data)
                bit_list = []
                bit_index = 8
                if x+1 == len(image_data):
                    bit_index = 0
                byte_counter += 1
            
            if x + 1 == len(image_data) and bit_index != 0:
                byte = 0
                for index in range(len(bit_list), 8):
                    bit_list.append(0)
                for bit in bit_list:
                    byte = (byte << 1) | bit
                byte_data = byte.to_bytes(1, byteorder='big')
                file.write(byte_data)
                bit_list = []
                bit_index = 7
                byte_counter += 1

def update_image_array(name):
    os.chdir("jpgs")
    img = Image.open("black.jpg")
    os.chdir("..")
    os.chdir("..")
    print(os.getcwd())

    with open ("image_array.txt", "r") as file:
        filedata = file.read()
        file.close()

    with open ("image_array.txt", "a") as file:
        # write information at the end of the file
        file.write(f"{name},\n")
        file.close()



def get_images(dir):
    os.chdir(dir)
    images = []
    for file in os.listdir():
        if file.endswith(".png"):
            file = file.replace(".png", "")
            images.append(file)
    return images


img_list = get_images("./Images_On_ESP")
os.chdir("..")
os.chdir("./Images")
for img in img_list:
    os.makedirs(f"{img}", exist_ok=True)
    os.makedirs(f"{img}/bmp", exist_ok=True)
    os.makedirs(f"{img}/jpgs", exist_ok=True)
    os.chdir("..")
    print(os.getcwd())

    os.chdir("./Images_On_ESP")

    convert_image_2_dithered(f"{img}.png", rotate)

    convert_image_2_7_colors(img, "dithered.png")

    update_image_array(img)

    os.chdir(f"{img}")
    os.remove("dithered.png")

    shutil.rmtree("jpgs")
    os.chdir("..")