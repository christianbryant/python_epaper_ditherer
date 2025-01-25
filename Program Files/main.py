import tkinter
import os
from PIL import Image, ImageOps, ImageFilter
from tkinter import filedialog
from settings import ProgramSettings
import customtkinter as ctk
import Frames

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # self.geometry("1080x720")

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.frame_setup()

    def frame_setup(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)


        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.AllItemsFrame = Frames.TitleAndSettingsFrame(master=self)
        self.AllItemsFrame.grid(row=0,column=0,padx=5,pady=(20, 100),sticky="nw")

        # if Frames.Settings.get_preview() is True:
        #     print("Preview True")
        #     self.previewframe = Frames.PreviewFrame(master=self)
        #     self.previewframe.grid(row=0,column=1,padx=5,pady=(20, 100),sticky="nw")


    def on_close(self):
        self.quit()
        self.destroy()  # Ensure the application exits



# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()