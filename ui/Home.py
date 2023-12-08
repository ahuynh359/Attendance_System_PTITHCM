import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os

from ui.LoginUI import LoginUI


class Home(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.img = None
        self.draw(controller)

    def draw(self, controller):
        # Image in left
        path = os.getcwd()
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(path, 'src/img.png')))
        panel = ttk.Label(self, image=self.img)
        panel.grid(row=0, column=0)

        # Title
        lb_title = ttk.Label(self, text='Face Recognition', font=("Verdana", 35))
        lb_title.grid(row=1, column=0, padx=10, pady=10)

        # Button login
        btn_login = ttk.Button(self, text='Login', command=lambda: controller.show_frame(LoginUI))
        btn_login.grid(row=2, column=0)

        # Button camera
        btn_camera = ttk.Button(self, text='Camera', command=lambda: controller.show_frame())
        btn_camera.grid(row=3, column=0)
