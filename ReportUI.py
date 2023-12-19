import csv
import os.path
import tkinter as tk
import calendar
import time
from threading import Thread
from tkinter import ttk
import bcrypt
import numpy as np
from PIL import Image, ImageTk
from tkinter import messagebox as mb
import cv2
from Data import UserEntity, ImageEntity
import dlib

from ManageUserUI import ManageUserUI
from NewUserUI import NewUser
from tkcalendar import Calendar


class ReportUI(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.cal = None
        self.data = controller.data
        self.id_list = self.data.get_all_user_id()

        self.input_frame = tk.Frame(self)
        self.lb_id = ttk.Label(self.input_frame, text="Choose ID")
        self.lb_id.pack()

        self.id = tk.StringVar()
        self.cmb_id = ttk.Combobox(self.input_frame, width=27, textvariable=self.id, values=self.id_list)
        self.cmb_id.pack(padx=5, pady=5)

        self.lb_date = ttk.Label(self.input_frame, text="Choose Date")
        self.lb_date.pack()

        self.date = tk.StringVar()
        self.et_date = ttk.Entry(self.input_frame, width=27, textvariable=self.date)
        self.et_date.pack(padx=5, pady=5)

        self.open_calendar_button = ttk.Button(self.input_frame, text="Pick a Date", command=self.calendar_view)
        self.open_calendar_button.pack(pady=10)

        self.input_frame.pack(side=tk.TOP)

        self.table_frame = tk.Frame(self)

        self.table_frame.pack(side=tk.BOTTOM)

    def calendar_view(self):
        def print_sel():
            self.date.set(str(cal.get_date()))
            print(cal.get_date())
            top.destroy()

        top = tk.Toplevel(self)

        cal = Calendar(top, date_pattern="dd/mm/yyy",
                       selectmode='day',
                       cursor="hand1")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()
