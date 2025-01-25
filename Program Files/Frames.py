import tkinter
from tkinter import filedialog
from settings import ProgramSettings
from Processing import Image_Processing
import customtkinter as ctk
from PIL import Image, ImageOps, ImageFilter
import os
import math

Settings = ProgramSettings()


class FolderSelectFrame(ctk.CTkFrame):
    def __init__(self, master, label_text, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.label = label_text
        if label_text:
            self.text = ctk.CTkLabel(self, text=label_text)
            self.text.grid(row=0,column=0,padx=20,pady=20,sticky="nw")

        self.button = ctk.CTkButton(self, text="Select Folder", command=self.select_folder)
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="w")

        self.entry = ctk.CTkEntry(self, width=300)
        self.entry.grid(row=1,column=0,padx=20, pady=20, sticky="ew") 

    def select_folder(self):
    # Open a directory dialog and store the selected folder path
        self.folder_selected = filedialog.askdirectory()
        if self.folder_selected:
            # Display the selected folder path
            self.entry.delete(0, ctk.END)  # Clear the text box first
            # Sets the users input in our settings
            if "Input" in self.label:
                Settings.set_inputfolder(self.folder_selected)
            elif "Output" in self.label:
                Settings.set_outputfolder(self.folder_selected)
            
            self.entry.insert(0, self.folder_selected)  # Insert the new folder path

#Current Settings Ideas
# Rotate Image
# Preview Dithered Image
# Fit to Size
# Debug Mode
# Debug mode would mean exporting all the different images and outputs during the conversion process (aka no file cleanup)
class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)

        self.check_var = ctk.StringVar(value="RotateOff")
        self.setup_checkboxes()

    def setup_checkboxes(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.rotate_checkbox = ctk.CTkCheckBox(self, text="Auto Rotate", command=self.checkbox_event,
        variable=self.check_var, onvalue="RotateOn", offvalue="RotateOff")
        self.rotate_checkbox.grid(row=0,column=0, padx=20, pady=20, sticky="ew")

        self.preview_checkbox = ctk.CTkCheckBox(self, text="Preview", command=self.checkbox_event,
        variable=self.check_var, onvalue="PreviewOn", offvalue="PreviewOff")
        self.preview_checkbox.grid(row=0,column=2, padx=20, pady=20, sticky="ew")

        self.fit_checkbox = ctk.CTkCheckBox(self, text="Auto Fit", command=self.checkbox_event,
        variable=self.check_var, onvalue="FitOn", offvalue="FitOff")
        self.fit_checkbox.grid(row=0,column=1, padx=20, pady=20, sticky="ew")

        self.debug_checkbox = ctk.CTkCheckBox(self, text="Debug", command=self.checkbox_event,
        variable=self.check_var, onvalue="DebugOn", offvalue="DebugOff")
        self.debug_checkbox.grid(row=0,column=3, padx=20, pady=20, sticky="ew")

    def checkbox_event(self):
        self.val = self.check_var.get()
        if "Rotate" in self.val:
            if "Off" in self.val:
                print("RotateOff")
                Settings.set_rotate(value=False)
            else:
                print("RotateOn")
                Settings.set_rotate(value=True)
                if Settings.get_preview() is True:
                    self.preview_event()
        elif "Preview" in self.val:
            if "Off" in self.val:
                print("PreviewOff")
                Settings.set_preview(value=False)
                self.preview_event()
            else:
                print("PreviewOn")
                Settings.set_preview(value=True)
                self.preview_event()
        elif "Fit" in self.val:
            if "Off" in self.val:
                print("FitOff")
                Settings.set_fit(value=False)
            else:
                print("FitOn")
                Settings.set_fit(value=True)
        elif "Debug" in self.val:
            if "Off" in self.val:
                print("DebugOff")
                Settings.set_debug(value=False)
            else:
                print("DebugOn")
                Settings.set_debug(value=True)

    def preview_event(self):
        processor = Image_Processing()
        if "None" not in Settings.get_inputfolder() and Settings.get_preview() is True:
            Settings.set_dithered_preview(processor.process_preview(Settings))
            self.image_frame = PreviewFrame(master=self.master.master.master, prev_images=Settings.get_dithered_preview())
            self.image_frame.grid(row=0,column=1,padx=(40,5),pady=(20, 100),sticky="nw")


            

class PreviewFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, prev_images, **kwargs):
        super().__init__(master, **kwargs)
        total_images = len(prev_images)
        grid_size = math.ceil(math.sqrt(total_images))  # Find the nearest integer square root
        self.configure(width=600, height=600)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        for img in prev_images:
                self.image_frame = ctk.CTkImage(light_image=img, dark_image=img, size=(600,448))
                self.image_label = ctk.CTkLabel(self, image=self.image_frame, text="")
                self.image_label.pack(padx=10, pady=10)
                
        

class TitleFrame(ctk.CTkFrame):
    def __init__(self, master, title_text,title_text2, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text=title_text, font=("Roboto", 42, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.line = ctk.CTkLabel(self, text="-"*75, font=("Roboto", 16))
        self.line.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        self.label2 = ctk.CTkLabel(self, text=title_text2, font=("Roboto", 16))
        self.label2.grid(row=2, column=0, padx=20, pady=5, sticky="w")

#TODO Setup Image Previews
class ImagesFrame(ctk.CTkFrame):
    def __init__(self, master, app_image, **kwargs):
        super().__init__(master, **kwargs)

        self.image_frame = ctk.CTkImage(light_image=app_image, dark_image=app_image, size=(105,105))
        self.image_label = ctk.CTkLabel(self, image=self.image_frame, text="")
        self.image_label.pack(padx=10, pady=10)



class TitleAndImageFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        self.title_frame = TitleFrame(master=self, title_text="Image2Display", title_text2="Helper application to convert images for display use")
        self.title_frame.grid(row=0,column=0,padx=10,pady=(10, 10),sticky="nw")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images")
        self.image_frame = ImagesFrame(master=self, app_image=Image.open(os.path.join(image_path, "vector_image_white_256.png")))
        self.image_frame.grid(row=0,column=1,padx=(40,10),pady=(10, 10),sticky="nw")


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, error_text, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text=error_text)
        self.label.pack(padx=20, pady=20)

class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.error = None

        self.button = ctk.CTkButton(self, text="Begin Processing", command=self.processing_button)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    def processing_button(self):
        processor = Image_Processing()
        if "None" in Settings.get_inputfolder() or "None" in Settings.get_outputfolder():
            self.error_text = "Please select both folder locations!"
            self.error_window()
        else:
            processor.process_images(Settings)
            self.success = None
            if self.success is None or not self.error.winfo_exists():
                self.success = ToplevelWindow(self, error_text="All Images have been processed!")
                self.success.focus()
            else:
                self.success.focus()


    def error_window(self):
        if self.error is None or not self.error.winfo_exists():
            self.error = ToplevelWindow(self, error_text=self.error_text)
        else:
            self.error.focus()


class AllSettingsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        self.input_folder_frame = FolderSelectFrame(master=self, label_text="Select Input Folder")
        self.input_folder_frame.grid(row=0,column=0,padx=20,pady=(10, 10),sticky="nw")

        self.output_folder_frame = FolderSelectFrame(master=self, label_text="Select Output Folder")
        self.output_folder_frame.grid(row=1,column=0,padx=20,pady=(10, 10),sticky="nw")

        self.settings_frame = SettingsFrame(master=self)
        self.settings_frame.grid(row=2,column=0,padx=20,pady=(10, 10),sticky="nw")

        self.button_frame = ButtonFrame(master=self)
        self.button_frame.grid(row=3,column=0,padx=20,pady=(10, 20),sticky="nw")

class TitleAndSettingsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        self.titleandimageframe = TitleAndImageFrame(master=self)
        self.titleandimageframe.grid(row=0,column=0,padx=10,pady=(10, 5),sticky="nw")

        self.allsettings_frame = AllSettingsFrame(master=self)
        self.allsettings_frame.grid(row=1,column=0,padx=10,pady=(5, 10),sticky="nw")

        self.pack()
        

class TitleSettingsAndPreviewFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        self.allsettings_frame = TitleAndSettingsFrame(master=self)
        self.allsettings_frame.grid(row=0,column=0,padx=5,pady=(20, 100),sticky="nw")
        
        self.image_frame = PreviewFrame(master=self, prev_images=Settings.get_dithered_preview())
        self.image_frame.grid(row=0,column=0,padx=(40,10),pady=(10, 10),sticky="nw")

class AllItemsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        self.titlepreview = TitleSettingsAndPreviewFrame(master=self)
        self.titlepreview.grid(row=0,column=0,padx=5,pady=(20, 100),sticky="nw")