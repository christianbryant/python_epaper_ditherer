from PIL import Image, ImageOps, ImageFilter
import numpy as np
import os
import shutil
from settings import ProgramSettings
import customtkinter as ctk

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

class Image_Processing:
    def __init__(self):
        super().__init__()
        self.images = []

    def process_images(self, settings):
        self.get_images(settings=settings)
        os.chdir(settings.get_outputfolder())
        total_img = len(self.images)
        each_percent = 1/total_img
        total_percent = 0
        for img in self.images:
            total_percent += each_percent
            if settings.get_debug():
                print(f"Folders created: {img}")
            os.makedirs(f"{img}", exist_ok=True)
            os.makedirs(f"{img}/bmp", exist_ok=True)
            os.makedirs(f"{img}/jpgs", exist_ok=True)
            os.chdir(settings.get_outputfolder())
            print(os.getcwd())

            os.chdir(settings.get_inputfolder())

            self.dithered_img = self.convert_image_2_dithered(f"{img}.png", settings=settings)

            self.convert_image_2_7_colors(img, self.dithered_img, settings=settings)

            self.update_image_array(img)

            os.chdir(f"{img}")
            if settings.get_debug() is False:
                shutil.rmtree("jpgs")
            os.chdir("..")

    def process_preview(self, settings):
        self.get_images(settings=settings)
        self.dithered_img = []
        total_img = len(self.images)
        for img in self.images:

            os.chdir(settings.get_inputfolder())

            dithered_result = self.convert_image_2_dithered(f"{img}.png", settings)

            # Ensure that dithered_result is a PIL Image (or iterable of images) and extend the list
            if isinstance(dithered_result, list):
                self.dithered_img.extend(dithered_result)  # Append multiple images if a list
            else:
                self.dithered_img.append(dithered_result)  # Append a single image

        return self.dithered_img


    def get_images(self, settings):
        os.chdir(settings.get_inputfolder())
        for file in os.listdir():
            if file.endswith(".png"):
                file = file.replace(".png", "")
                self.images.append(file)
    
    def update_image_array(self, name):
        os.chdir("jpgs")
        img = Image.open("black.jpg")
        os.chdir("..")
        os.chdir("..")
        print(os.getcwd())
        
        # Fix the folder/file requirements
        try:
            with open ("image_array.txt", "r") as file:
                filedata = file.read()
                file.close()
        except OSError as e:
            with open ("image_array.txt", "x") as file:
                file.close()
        #TODO Make it check to see if the file names are already on the list or not
        with open ("image_array.txt", "a") as file:
            # write information at the end of the file
            file.write(f"{name},\n")
            file.close()

    def convert_bmp_to_binary(self, bmp_file, name):
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

    def convert_image_2_dithered(self, image, settings):
        # Open the input image
        input_image = Image.open(image).convert('RGB')
        resized_image = input_image.copy()
        if settings.get_rotate():
            if(resized_image.size[1] > resized_image.size[0]):
                resized_image = resized_image.transpose(Image.ROTATE_90)

        resized_image.thumbnail((600, 448), Image.LANCZOS)
        p_img = Image.new('P', resized_image.size)
        p_img.putpalette(palette)
        quantized_image = resized_image.quantize(palette=p_img)
        dithered_image = quantized_image.convert('P')
        if "None" not in settings.get_outputfolder():
            output_folder = settings.get_outputfolder()
            os.chdir(f"{output_folder}/{image.replace('.png', '')}")
        if settings.get_debug() is True:
            settings.get_debugframe().textbox.insert(ctk.END,f"Output images at: {settings.get_outputfolder()}\n")
            # print(f"Output folder: {settings.get_outputfolder()}")
            dithered_image.save("dithered.png")
        return dithered_image

    def convert_image_2_7_colors(self, name, image, settings):
        # Open the input image
        input_image = image

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

            self.convert_bmp_to_binary("./bmp/" + str(colors[current_color]) + ".bmp", name)
            current_color += 1
        if settings.get_debug() is False:
            shutil.rmtree("bmp")
        print("Images saved successfully.")