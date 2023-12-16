import tkinter as tk
from tkinter import ttk


class LoginUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Back button
        from HomeUI import HomeUI
        self.btn_back = ttk.Button(self, text='< Back', command=lambda: controller.show_frame(HomeUI))
        self.btn_back.pack(padx=30, pady=30, anchor=tk.W)

        # Text login
        self.lb_title = ttk.Label(self, text='Login', font=("Verdana", 35))
        self.lb_title.pack(pady=50)

        # User Entry
        self.lb_user = ttk.Label(self, text='Username')
        self.lb_user.pack()

        self.user_var = tk.StringVar()
        self.et_user = ttk.Entry(self, textvariable=self.user_var, width=35)
        self.et_user.pack()

        # Password Entry

        self.lb_pass = ttk.Label(self, text='Password')
        self.lb_pass.pack()

        self.pass_var = tk.StringVar()
        self.et_name = ttk.Entry(self, show="*", textvariable=self.pass_var, width=35)
        self.et_name.pack()

        # Login Button
        self.btn_login = ttk.Button(self, text='Login', command=lambda: controller.login(self.submit()))
        self.btn_login.pack(pady=10)

    def submit(self):
        user = self.user_var.get()
        password = self.pass_var.get()

        self.user_var.set('')
        self.pass_var.set('')

        return user, password
