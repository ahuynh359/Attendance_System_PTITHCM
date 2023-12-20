import tkinter as tk
from tkinter import ttk

from ManageUserUI import ManageUserUI
from NewUserUI import NewUser
from ReportUI import ReportUI


class AdminUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.data = controller.db

        # Back button
        from LoginUI import LoginUI
        self.btn_back = ttk.Button(self, text='< Logout', command=lambda: controller.show_frame(LoginUI))
        self.btn_back.pack(padx=30, pady=30, anchor=tk.W)

        # Tab control
        self.tab_control = ttk.Notebook(self)
        self.parent_new_user_frame = ttk.Frame(self.tab_control)
        self.parent_manage_user_frame = ttk.Frame(self.tab_control)
        self.parent_report_frame = ttk.Frame(self.tab_control)

        # Tab new user
        self.new_user_ui = NewUser(self.parent_new_user_frame, self)
        self.new_user_ui.pack(fill=tk.BOTH, expand=1)

        # Tab manage user
        self.manage_user_ui = ManageUserUI(self.parent_manage_user_frame, self)
        self.manage_user_ui.pack(fill=tk.BOTH, expand=1)

        # Tab report
        self.report_ui = ReportUI(self.parent_report_frame, self)
        self.report_ui.pack(fill=tk.BOTH, expand=1)

        self.tab_control.add(self.parent_new_user_frame, text='New User')
        self.tab_control.add(self.parent_manage_user_frame, text='Manage User')
        self.tab_control.add(self.parent_report_frame, text='Report')
        self.tab_control.pack(expand=1, fill="both")
