import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from LoginUI import LoginUI


class HomeUI(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.img = None
        self.draw(controller)

    def draw(self, controller):
        # Image
        self.img = ImageTk.PhotoImage(Image.open('src/img.png'))
        panel = ttk.Label(self, image=self.img)
        panel.pack(pady=50)

        # Title
        lb_title = ttk.Label(self, text='Face Recognition', font=("Verdana", 35))
        lb_title.pack()

        # Button login
        btn_login = ttk.Button(self, text='Login', command=lambda: controller.show_frame(LoginUI))
        btn_login.pack(pady=5)

        # Button camera
        btn_camera = ttk.Button(self, text='Camera', command=lambda: controller.show_camera())
        btn_camera.pack()
