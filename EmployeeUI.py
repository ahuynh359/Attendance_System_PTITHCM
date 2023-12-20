import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from datetime import datetime

import bcrypt
from tkcalendar import Calendar


class EmployeeUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.data = controller.db
        self.user_id = None

        # Back button
        from LoginUI import LoginUI
        self.btn_back = ttk.Button(self, text='< Logout', command=lambda: controller.show_frame(LoginUI))
        self.btn_back.pack(padx=30, pady=30, anchor=tk.W)

        # Tab control
        self.tab_control = ttk.Notebook(self)

        # Tab report
        self.report_frame = ttk.Frame(self.tab_control)

        self.date = tk.StringVar()
        self.date.set(datetime.now().strftime("%d/%m/%Y"))
        self.et_date = ttk.Entry(self.report_frame, width=27, textvariable=self.date)
        self.et_date.pack(side=tk.TOP)

        self.btn_open_calendar = ttk.Button(self.report_frame, text="Pick a Date", command=self.calendar_view)
        self.btn_open_calendar.pack(side=tk.TOP)
        self.report_frame.pack(fill=tk.BOTH, expand=1)

        self.btn_gen = ttk.Button(
            self.report_frame, text="Gen Report", command=self.gen_report)
        self.btn_gen.pack(side=tk.TOP)

        # Report table
        self.report_table = ttk.Treeview(self.report_frame, selectmode='browse')
        name = ["Id", "User ID", "Time Attendance", "First Check In", "Last Check Out", "CI", "CO"]
        self.report_table['columns'] = name
        self.report_table.column("#0", width=0)
        for i in name:
            self.report_table.column(i, anchor='w', width=150)
        for i in name:
            self.report_table.heading(i, text=i, anchor='w')

        self.report_table.pack(side=tk.TOP, pady=15)

        # Tab change password
        self.change_password_frame = ttk.Frame(self.tab_control)
        self.change_password_frame.pack(fill=tk.BOTH, expand=1)

        self.lb_old_pass = ttk.Label(self.change_password_frame, text="Old Password")
        self.lb_old_pass.pack()

        self.text_old_pass = tk.StringVar()
        self.et_old_pass = ttk.Entry(self.change_password_frame, textvariable=self.text_old_pass, width=35, show='*')
        self.et_old_pass.pack()

        self.lb_new_pass = ttk.Label(self.change_password_frame, text="New Password")
        self.lb_new_pass.pack()

        self.text_new_pass = tk.StringVar()
        self.et_new_pass = ttk.Entry(self.change_password_frame, textvariable=self.text_new_pass, width=35, show='*')
        self.et_new_pass.pack()

        self.lb_confirm_pass = ttk.Label(self.change_password_frame, text="Confirm Password")
        self.lb_confirm_pass.pack()

        self.text_confirm_pass = tk.StringVar()
        self.et_confirm_pass = ttk.Entry(self.change_password_frame, textvariable=self.text_confirm_pass, width=35,
                                         show='*')
        self.et_confirm_pass.pack()

        self.btn_confirm = ttk.Button(self.change_password_frame, text='OK', command=self.change_pass)
        self.btn_confirm.pack()

        self.tab_control.add(self.report_frame, text='Report')
        self.tab_control.add(self.change_password_frame, text='Change Password')
        self.tab_control.pack(expand=1, fill="both")

    def change_pass(self):
        old_pass = self.data.get_user_with_id(self.user_id).hash_password
        if not bcrypt.checkpw(self.text_old_pass.get().encode('utf-8'), old_pass):
            mb.showerror('Error', 'Old password dont match')
            return
        if self.text_new_pass.get() != self.text_confirm_pass.get():
            mb.showerror('Error', 'Confirm password dont match')
            return
        self.data.change_pass(self.user_id,
                              bcrypt.hashpw(self.text_confirm_pass.get().encode('utf-8'), bcrypt.gensalt()))
        mb.showinfo('Success', 'Password has changed for ' + str(self.user_id))
        self.clear_data()

    def clear_data(self):
        self.et_new_pass.delete(0, tk.END)
        self.et_old_pass.delete(0, tk.END)
        self.et_confirm_pass.delete(0, tk.END)

    def gen_report(self):
        for data in self.report_table.get_children():
            self.report_table.delete(data)
        print(self.user_id)
        attendance = self.data.get_attendance_by_user_id(self.user_id, self.date.get())
        if attendance is None:
            mb.showinfo("None", "user has no attendance")
        else:
            for data in attendance:
                check_in = attendance[0].timestamp
                check_out = attendance[len(attendance) - 1].timestamp
                compare_time_check_int = check_in.replace(hour=8, minute=30, second=0)
                compare_time_check_out = check_out.replace(hour=17, minute=30, second=0)
                if check_in < compare_time_check_int:
                    flag_check_in = "On Time"
                else:
                    flag_check_in = "Late"
                if check_out > compare_time_check_out:
                    flag_check_out = "On Time"
                else:
                    flag_check_out = "Early"
                self.report_table.insert(parent='', index='end', values=(data.id, data.user_id,
                                                                         data.timestamp.strftime("%H:%M:%S %d/%m/%Y"),
                                                                         check_in.strftime("%H:%M:%S %d/%m/%Y"),
                                                                         check_out.strftime("%H:%M:%S %d/%m/%Y"),
                                                                         flag_check_in,
                                                                         flag_check_out
                                                                         ), tags='orow')

    def calendar_view(self):
        def print_sel():
            self.date.set(str(cal.get_date()))
            print(cal.get_date())
            top.destroy()

        top = tk.Toplevel(self)

        cal = Calendar(top, date_pattern="dd/mm/yyyy",
                       selectmode='day',
                       cursor="hand1")
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()
