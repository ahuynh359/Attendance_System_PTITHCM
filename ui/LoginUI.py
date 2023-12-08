import tkinter as tk
from tkinter import ttk


class LoginUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        self.draw(controller)

    def sumbit(self):
        user = self.user_var
        password = self.pass_var
        print("The name is : " + user)
        print("The password is : " + password)

        self.user_var.set("")
        self.pass_var.set("")

    def draw(self, controller):
        # Back button
        from ui.Home import Home
        btn_back = ttk.Button(self, text='<', command=lambda: controller.show_frame(Home), width=1)
        btn_back.grid(row=0, column=0, pady=5)

        # User Entry
        lb_user = tk.Label(self, text='Username')
        lb_user.grid(row=1, column=0, pady=10)
        et_user = ttk.Entry(self, textvariable=self.user_var)
        et_user.grid(row=1, column=1,pady=10)

        # Password Entry
        lb_pass = tk.Label(self, text='Password')
        lb_pass.grid(row=2, column=0, padx=10, pady=10)
        et_name = ttk.Entry(self, textvariable=self.pass_var)
        et_name.grid(row=2, column=1, padx=10, pady=10)

        # Login Button
        btn_login = ttk.Button(self, text='Login', command=lambda: controller.show_frame(Home))
        btn_login.grid(row=3, column=1, pady=5)
