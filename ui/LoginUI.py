import tkinter as tk
from tkinter import ttk


class LoginUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.lb_error = None
        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        self.draw(controller)

    def sumbit(self):
        user = self.user_var
        password = self.pass_var
        print("The name is : " + user.get())
        print("The password is : " + password.get())
        return user.get(), password.get()

    def show_label(self, event=None):
        self.lb_error.lift(self)

    def draw(self, controller):
        # Back button
        from ui.Home import Home
        btn_back = ttk.Button(self, text='<', command=lambda: controller.show_frame(Home), width=1)
        btn_back.pack(side='left')

        # Text login
        lb_title = ttk.Label(self, text='Login', font=("Verdana", 35))
        lb_title.pack(pady=100)

        # User Entry
        lb_user = ttk.Label(self, text='Username')
        lb_user.pack()
        et_user = ttk.Entry(self, textvariable=self.user_var)
        et_user.pack()

        # Password Entry
        lb_pass = ttk.Label(self, text='Password')
        lb_pass.pack()
        et_name = ttk.Entry(self, show="*", textvariable=self.pass_var)
        et_name.pack()

        # Text error
        # self.lb_error = ttk.Label(self, text='Error ',foreground='red')
        # self.lb_error.lower(self)
        # self.lb_error.pack()

        # Login Button
        btn_login = ttk.Button(self, text='Login', command=lambda: controller.login(self.sumbit()))
        btn_login.pack()
