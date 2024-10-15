import tkinter
from tkinter import filedialog
from settings import ProgramSettings
from Processing import Image_Processing
import customtkinter as ctk


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
        settings = ProgramSettings()
        if self.folder_selected:
            # Display the selected folder path
            self.entry.delete(0, ctk.END)  # Clear the text box first
            # Sets the users input in our settings
            if "Input" in self.label:
                settings.set_inputfolder(self.folder_selected)
            elif "Output" in self.label:
                settings.set_outputfolder(self.folder_selected)
            
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
        settings = ProgramSettings()
        if "Rotate" in self.val:
            if "Off" in self.val:
                print("RotateOff")
                settings.set_rotate(value=False)
            else:
                print("RotateOn")
                settings.set_rotate(value=True)
        elif "Preview" in self.val:
            if "Off" in self.val:
                print("PreviewOff")
                settings.set_preview(value=False)
            else:
                print("PreviewOn")
                settings.set_preview(value=True)
        elif "Fit" in self.val:
            if "Off" in self.val:
                print("FitOff")
                settings.set_fit(value=False)
            else:
                print("FitOn")
                settings.set_fit(value=True)
        elif "Debug" in self.val:
            if "Off" in self.val:
                print("DebugOff")
                settings.set_debug(value=False)
            else:
                print("DebugOn")
                settings.set_debug(value=True)
        

#TODO Setup Image Previews
class ImagesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


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
        settings = ProgramSettings()
        processor = Image_Processing()
        if "None" in settings.get_inputfolder() or "None" in settings.get_outputfolder():
            self.error_text = "Please select both folder locations!"
            self.error_window()
        else:
            processor.process_images()
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