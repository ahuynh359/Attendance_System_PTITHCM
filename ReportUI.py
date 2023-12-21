from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkcalendar import Calendar


class ReportUI(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.text_gender = tk.StringVar()
        self.text_phone = tk.StringVar()
        self.text_email = tk.StringVar()
        self.text_last_name = tk.StringVar()
        self.text_first_name = tk.StringVar()
        self.text_password = tk.StringVar()
        self.text_user_name = tk.StringVar()
        self.data = controller.data

        self.table_frame = ttk.Frame(self)

        self.date = tk.StringVar()
        self.date.set(datetime.now().strftime("%d/%m/%Y"))
        self.et_date = ttk.Entry(self.table_frame, width=27, textvariable=self.date)
        self.et_date.pack(side=tk.TOP)

        self.btn_open_calendar = ttk.Button(self.table_frame, text="Pick a Date", command=self.calendar_view)
        self.btn_open_calendar.pack(side=tk.TOP)

        # Table frame

        style = ttk.Style()
        style.configure("Treeview.Heading")

        self.my_tree = ttk.Treeview(self.table_frame, selectmode='browse')
        name = ["ID", "User", "Pass", "FirstN", "LastN", "Email", "Phone", "Gender"]

        self.my_tree['columns'] = name
        self.my_tree.column("#0", width=0)
        for i in name:
            self.my_tree.column(i, anchor='w', width=80)
        for i in name:
            self.my_tree.heading(i, text=i, anchor='w')
        self.refresh_data()
        self.my_tree.pack()
        self.my_tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.table_frame.pack(side=tk.TOP)

        self.btn_gen = ttk.Button(
            self.table_frame, text="Gen Report", command=self.gen_report)
        self.btn_gen.pack(side=tk.TOP)

        # Report table
        self.report_table = ttk.Treeview(self.table_frame, selectmode='browse')
        name = ["Id", "User ID", "Time Attendance", "First Check In", "Last Check Out", "CI", "CO"]
        self.report_table['columns'] = name
        self.report_table.column("#0", width=0)
        for i in name:
            self.report_table.column(i, anchor='w', width=150)
        for i in name:
            self.report_table.heading(i, text=i, anchor='w')

        self.report_table.pack(side=tk.BOTTOM, pady=15)

    def refresh_report_data(self, user_id):
        for data in self.report_table.get_children():
            self.report_table.delete(data)

        attendance = self.data.get_attendance_by_user_id(user_id, self.date.get())
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

    def gen_report(self):
        if self.my_tree.selection():
            record = item['values']
            self.refresh_report_data(record[0])
        else:
            mb.showerror("Error", "No Item Selected")

    def item_selected(self, event):
        global item
        for selected_item in self.my_tree.selection():
            item = self.my_tree.item(selected_item)

    def refresh_data(self):
        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.data.read_all_users():
            self.my_tree.insert(parent='', index='end', values=(
                result.id, result.user_name, result.hash_password, result.first_name, result.last_name,
                result.email,
                result.phone_number, result.gender, result.role), tags='orow')

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
