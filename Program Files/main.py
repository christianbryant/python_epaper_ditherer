import tkinter
from tkinter import filedialog
from settings import ProgramSettings
import customtkinter as ctk
import Frames

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)


        self.grid_columnconfigure(0, weight=1)

        self.input_folder_frame = Frames.FolderSelectFrame(master=self, label_text="Select Input Folder")
        self.input_folder_frame.grid(row=0,column=0,padx=20,pady=(20, 10),sticky="nw")


        self.output_folder_frame = Frames.FolderSelectFrame(master=self, label_text="Select Output Folder")
        self.output_folder_frame.grid(row=1,column=0,padx=20,pady=(10, 10),sticky="nw")

        self.settings_frame = Frames.SettingsFrame(master=self)
        self.settings_frame.grid(row=2,column=0,padx=20,pady=(10, 10),sticky="nw")

        self.button_frame = Frames.ButtonFrame(master=self)
        self.button_frame.grid(row=4,column=0,padx=20,pady=(10, 20),sticky="nw")

    def on_close(self):
        self.quit()
        self.destroy()  # Ensure the application exits



# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()