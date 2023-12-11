import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import cv2


class AdminUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Back button
        from ui.LoginUI import LoginUI
        self.btn_back = ttk.Button(self, text='Logout', command=lambda: controller.show_frame(LoginUI))
        self.btn_back.pack(side=tk.LEFT)

        # Camera frame
        self.frame_camera = tk.Frame(self)
        self.lb_camera = tk.Label(self.frame_camera)
        self.lb_camera.pack(side=tk.LEFT)
        self.frame_camera.pack(side=tk.LEFT)

        # Input frame
        self.input_frame = tk.Frame(self)

        self.lb_title = ttk.Label(self.input_frame, text='Input', font=("Verdana", 35))
        self.lb_title.pack(pady=50)

        self.lb_id = ttk.Label(self.input_frame, text='Id')
        self.lb_id.pack()

        self.et_id = ttk.Entry(self.input_frame, width=25)
        self.et_id.pack()

        self.lb_user_name = ttk.Label(self.input_frame, text='User Name')
        self.lb_user_name.pack()

        self.et_user_name = ttk.Entry(self.input_frame, width=25)
        self.et_user_name.pack()

        self.lb_password = ttk.Label(self.input_frame, text='Password')
        self.lb_password.pack()

        self.et_password = ttk.Entry(self.input_frame, width=25)
        self.et_password.pack()

        self.lb_first_name = ttk.Label(self.input_frame, text='First Name')
        self.lb_first_name.pack()

        self.et_first_name = ttk.Entry(self.input_frame, width=25)
        self.et_first_name.pack()

        self.lb_email = ttk.Label(self.input_frame, text='Email')
        self.lb_email.pack()

        self.et_email = ttk.Entry(self.input_frame, width=25)
        self.et_email.pack()

        self.lb_phone = ttk.Label(self.input_frame, text='Phone Number')
        self.lb_phone.pack()

        self.et_phone = ttk.Entry(self.input_frame, width=25)
        self.et_phone.pack()

        self.lb_gender = ttk.Label(self.input_frame, text='Gender')
        self.lb_gender.pack()

        var1 = tk.IntVar()
        self.cb_gender = tk.Checkbutton(self.input_frame, text='Male', variable=var1, onvalue=1, offvalue=0, command='')
        self.cb_gender.pack()

        self.btn_enter = ttk.Button(
            self.input_frame, text="Enter", command='')
        self.btn_enter.pack(side=tk.LEFT)

        self.btn_update = ttk.Button(
            self.input_frame, text="Update", command='')
        self.btn_update.pack(side=tk.LEFT)

        self.btn_delete = ttk.Button(
            self.input_frame, text="Delete", command='')
        self.btn_delete.pack(side=tk.LEFT)

        self.input_frame.pack(side=tk.LEFT)

        # Table frame
        self.table_frame = ttk.Frame(self)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 15))

        my_tree = ttk.Treeview(self.table_frame)
        my_tree['columns'] = ("ID", "Name", "Price", "Quantity")
        my_tree.column("#0", width=0)
        my_tree.column("ID", anchor='w', width=100)
        my_tree.column("Name", anchor='w', width=200)
        my_tree.column("Price", anchor='w', width=150)
        my_tree.column("Quantity", anchor='w', width=150)
        my_tree.heading("ID", text="ID", anchor='w')
        my_tree.heading("Name", text="Name", anchor='w')
        my_tree.heading("Price", text="Price", anchor='w')
        my_tree.heading("Quantity", text="Quantity", anchor='w')
        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
        my_tree.pack()
        self.table_frame.pack(side=tk.LEFT)

        self.cap = cv2.VideoCapture(0)
        self.proccess()

    def get_frame(self):
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except:
            print("Error: No video input!!!")

    def proccess(self):
        # Get current frame
        ret, self.current_frame = self.get_frame()
        image = Image.fromarray(self.current_frame)
        image = ImageTk.PhotoImage(image)
        self.lb_camera.img_tk = image
        self.lb_camera.configure(image=image)
