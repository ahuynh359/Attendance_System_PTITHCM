import tkinter as tk
from tkinter import ttk
import bcrypt
from tkinter import messagebox as mb
from Data import UserEntity


class ManageUserUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.data = controller.data

        # Input frame
        self.new_user_frame_left = tk.Frame(self)

        self.lb_user_name = ttk.Label(self.new_user_frame_left, text='User Name')
        self.lb_user_name.grid(row=0, column=0, padx=15, pady=5)

        self.text_user_name = tk.StringVar()
        self.et_user_name = ttk.Entry(self.new_user_frame_left, width=25, textvariable=self.text_user_name)
        self.et_user_name.grid(row=1, column=0, padx=10, pady=5)

        self.lb_password = ttk.Label(self.new_user_frame_left, text='Password')
        self.lb_password.grid(row=2, column=0, padx=15, pady=5)

        self.btn_reset_pass = ttk.Button(self.new_user_frame_left, text='Reset Password', command=self.reset_password)
        self.btn_reset_pass.grid(row=3, column=0, padx=10, pady=5)

        self.lb_first_name = ttk.Label(self.new_user_frame_left, text='First Name')
        self.lb_first_name.grid(row=4, column=0, padx=15, pady=5)

        self.text_first_name = tk.StringVar()
        self.et_first_name = ttk.Entry(self.new_user_frame_left, width=25, textvariable=self.text_first_name)
        self.et_first_name.grid(row=5, column=0, padx=10, pady=5)

        self.lb_last_name = ttk.Label(self.new_user_frame_left, text='Last Name')
        self.lb_last_name.grid(row=6, column=0, padx=15, pady=5)

        self.text_last_name = tk.StringVar()
        self.et_last_name = ttk.Entry(self.new_user_frame_left, width=25, textvariable=self.text_last_name)
        self.et_last_name.grid(row=7, column=0, padx=10, pady=5)

        self.lb_email = ttk.Label(self.new_user_frame_left, text='Email')
        self.lb_email.grid(row=0, column=1, padx=15, pady=5)

        self.text_email = tk.StringVar()
        self.et_email = ttk.Entry(self.new_user_frame_left, width=25, textvariable=self.text_email)
        self.et_email.grid(row=1, column=1, padx=10, pady=5)

        self.lb_phone = ttk.Label(self.new_user_frame_left, text='Phone Number')
        self.lb_phone.grid(row=2, column=1, padx=15, pady=5)

        self.text_phone = tk.StringVar()
        self.et_phone = ttk.Entry(self.new_user_frame_left, width=25, textvariable=self.text_phone)
        self.et_phone.grid(row=3, column=1, padx=10, pady=5)

        self.lb_gender = ttk.Label(self.new_user_frame_left, text='Gender')
        self.lb_gender.grid(row=4, column=1, padx=15, pady=5)

        self.var1 = tk.StringVar()
        self.cmb_gender = ttk.Combobox(self.new_user_frame_left, width=20, textvariable=self.var1)
        self.cmb_gender.grid(row=5, column=1, padx=10, pady=5)
        self.cmb_gender['values'] = ('Male', 'Female')
        self.cmb_gender.current(0)

        self.btn_update = ttk.Button(
            self.new_user_frame_left, text="Update", command=self.update_data)
        self.btn_update.grid(row=8, column=0, padx=10, pady=15)

        self.btn_delete = ttk.Button(
            self.new_user_frame_left, text="Delete", command=self.delete_data)
        self.btn_delete.grid(row=8, column=1, padx=10, pady=15)

        self.new_user_frame_left.pack(side=tk.LEFT)

        # Table frame
        self.table_frame = ttk.Frame(self)
        self.btn_clear_selection = ttk.Button(
            self.table_frame, text="Double click to clear selection", command=self.disable_selection)
        self.btn_clear_selection.pack(side=tk.TOP, pady=5)
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
        self.table_frame.pack(side=tk.RIGHT)

    def disable_selection(self):
        self.my_tree.selection_remove(self.my_tree.selection())
        self.clear_data()

    def reset_password(self):
        if self.my_tree.selection():
            selected_item = self.my_tree.selection()[0]
            id = str(self.my_tree.item(selected_item)['values'][0])

            res = self.data.reset_password(int(id))
            if res == 1:
                mb.showinfo('Success', 'Update password for user ' + id + ' successfully')
            else:
                mb.showerror('Failed', 'Update password for user failed')

        else:
            mb.showerror("Error", "No Item Selected")

    def delete_data(self):
        if self.my_tree.selection():
            selected_item = self.my_tree.selection()[0]
            id = str(self.my_tree.item(selected_item)['values'][0])
            res = self.data.delete_user(int(id))
            if res == 1:
                mb.showinfo('Success', 'Delete user ' + id + ' successfully')
            else:
                mb.showerror('Failed', 'Delete user failed because this user has images or attendances')

        else:
            mb.showerror("Error", "No Item Selected")
        self.refresh_data()
        self.clear_data()

    def check_data(self):
        if str(self.et_user_name.get()).strip() == '':
            mb.showwarning("Empty", "Do not leave user name empty")
            return 0
        if str(self.et_first_name.get()).strip() == '':
            mb.showwarning("Empty", "Do not leave first name empty")
            return 0
        if str(self.et_last_name.get()).strip() == '':
            mb.showwarning("Empty", "Do not leave last name empty")
            return 0
        if str(self.et_email.get()).strip() == '':
            mb.showwarning("Empty", "Do not leave email empty")
            return 0
        if str(self.et_phone.get()).strip() == '':
            mb.showwarning("Empty", "Do not phone empty")
            return 0
        return 1

    def update_data(self):
        if self.my_tree.selection():
            selected_item = self.my_tree.selection()[0]
            id = str(self.my_tree.item(selected_item)['values'][0])

            res = self.check_data()
            if res == 1:
                user_name = self.text_user_name.get()
                first_name = self.text_first_name.get()
                last_name = self.text_last_name.get()
                email = self.text_email.get()
                phone = self.text_phone.get()
                gender = str(self.cmb_gender.get())
                if gender == 'Female':
                    gender = 1
                else:
                    gender = 0

                ress = self.data.update_user(id, user_name, first_name, last_name, email, phone, gender)
                if ress == 1:
                    mb.showinfo("Success", "Update user successfully")
                else:
                    mb.showerror("Failed", "Update user failed")
        else:
            mb.showerror("Error", "No Item Selected")
        self.refresh_data()
        self.clear_data()

    def clear_data(self):
        self.et_user_name.delete(0, tk.END)
        self.et_first_name.delete(0, tk.END)
        self.et_last_name.delete(0, tk.END)
        self.et_email.delete(0, tk.END)
        self.et_phone.delete(0, tk.END)
        self.cmb_gender.current(0)

    def item_selected(self, event):
        global item
        for selected_item in self.my_tree.selection():
            item = self.my_tree.item(selected_item)

        record = item['values']

        self.text_user_name.set(record[1])
        self.text_first_name.set(record[3])
        self.text_last_name.set(record[4])
        self.text_email.set(record[5])
        self.text_phone.set(record[6])
        gender = record[7]
        if gender == 0:
            self.cmb_gender.current(0)
        else:
            self.cmb_gender.current(1)

    def refresh_data(self):
        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.data.read_all_users():
            self.my_tree.insert(parent='', index='end', values=(
                result.id, result.user_name, result.hash_password, result.first_name, result.last_name,
                result.email,
                result.phone_number, result.gender, result.role), tags='orow')
