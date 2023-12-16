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


class AdminUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.data = controller.db
        self.detector = dlib.get_frontal_face_detector()

        self.predictor = dlib.shape_predictor(
            'data/data_dlib/shape_predictor_68_face_landmarks.dat')
        self.face_reco_model = dlib.face_recognition_model_v1(
            'data/data_dlib/dlib_face_recognition_resnet_model_v1.dat')

        # Back button
        from LoginUI import LoginUI
        self.btn_back = ttk.Button(self, text='< Logout', command=lambda: controller.show_frame(LoginUI))
        self.btn_back.pack(padx=30, pady=30, anchor=tk.W)

        # Input frame
        self.input_frame = tk.Frame(self)

        self.lb_user_name = ttk.Label(self.input_frame, text='User Name')
        self.lb_user_name.grid(column=0, row=0, pady=5, padx=15)

        self.text_user_name = tk.StringVar()
        self.et_user_name = ttk.Entry(self.input_frame, width=25, textvariable=self.text_user_name)
        self.et_user_name.grid(column=1, row=0, pady=5)

        self.lb_password = ttk.Label(self.input_frame, text='Password')
        self.lb_password.grid(column=0, row=1, pady=5, padx=15)

        self.text_password = tk.StringVar()
        self.et_password = ttk.Entry(self.input_frame, width=25, show='*', textvariable=self.text_password)
        self.et_password.grid(column=1, row=1, pady=5)

        self.lb_first_name = ttk.Label(self.input_frame, text='First Name')
        self.lb_first_name.grid(column=2, row=0, pady=5, padx=15)

        self.text_first_name = tk.StringVar()
        self.et_first_name = ttk.Entry(self.input_frame, width=25, textvariable=self.text_first_name)
        self.et_first_name.grid(column=3, row=0, pady=5)

        self.lb_last_name = ttk.Label(self.input_frame, text='Last Name')
        self.lb_last_name.grid(column=2, row=1, pady=5, padx=15)

        self.text_last_name = tk.StringVar()
        self.et_last_name = ttk.Entry(self.input_frame, width=25, textvariable=self.text_last_name)
        self.et_last_name.grid(column=3, row=1, pady=5)

        self.lb_email = ttk.Label(self.input_frame, text='Email')
        self.lb_email.grid(column=4, row=0, pady=5, padx=15)

        self.text_email = tk.StringVar()
        self.et_email = ttk.Entry(self.input_frame, width=25, textvariable=self.text_email)
        self.et_email.grid(column=5, row=0, pady=5)

        self.lb_phone = ttk.Label(self.input_frame, text='Phone Number')
        self.lb_phone.grid(column=4, row=1, pady=5, padx=15)

        self.text_phone = tk.StringVar()
        self.et_phone = ttk.Entry(self.input_frame, width=25, textvariable=self.text_phone)
        self.et_phone.grid(column=5, row=1, pady=5)

        self.lb_gender = ttk.Label(self.input_frame, text='Gender')
        self.lb_gender.grid(column=6, row=0, pady=5, padx=15)

        self.var1 = tk.StringVar()
        self.cmb_gender = ttk.Combobox(self.input_frame, width=20, textvariable=self.var1)
        self.cmb_gender.grid(column=7, row=0, pady=5)
        self.cmb_gender['values'] = ('Male', 'Female')
        self.cmb_gender.current(0)

        self.lb_image = ttk.Label(self.input_frame, text='Image')
        self.lb_image.grid(column=6, row=1, pady=5, padx=15)

        self.text_image_folder = tk.StringVar()
        self.et_image_folder = ttk.Entry(self.input_frame, width=25, textvariable=self.text_image_folder)
        self.et_image_folder.grid(column=7, row=1)

        self.btn_create_folder = ttk.Button(
            self.input_frame, text="Create Folder", command=self.mk_dir)
        self.btn_create_folder.grid(column=8, row=1)

        self.btn_take_image = ttk.Button(
            self.input_frame, text="Take Image", command=self.take_image)
        self.btn_take_image.grid(column=9, row=1)

        self.lb_info = ttk.Label(self.input_frame, foreground='red')
        self.lb_info.grid(column=7, row=2, pady=5, padx=15)

        self.btn_insert = ttk.Button(
            self.input_frame, text="Enter", command=self.insert_data)
        self.btn_insert.grid(column=3, row=3, pady=10)

        self.btn_extract_feature = ttk.Button(
            self.input_frame, text="Extract image feature", command=self.write_feature)
        self.btn_extract_feature.grid(column=4, row=3, pady=10)

        self.btn_delete = ttk.Button(
            self.input_frame, text="Delete", command=self.delete_data)
        self.btn_delete.grid(column=5, row=3, pady=10)

        self.input_frame.pack(side=tk.TOP)

        # Camera frame
        self.camera_frame = tk.Frame(self)
        self.btn_open_camera = ttk.Button(self.camera_frame, text='Open', command=self.start_capture)
        self.btn_open_camera.pack(side=tk.TOP)
        self.btn_close_camera = ttk.Button(self.camera_frame, text='Close', command=self.stop_capture)
        self.btn_close_camera.pack(side=tk.TOP)
        self.lb_warning = tk.Label(self.camera_frame, text='OK', fg='green')
        self.lb_warning.pack(pady=5)
        self.lb_camera = ttk.Label(self.camera_frame)
        self.lb_camera.pack()
        self.camera_frame.pack(side=tk.LEFT)

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
        self.table_frame.pack(side=tk.RIGHT)

        self.cap = cv2.VideoCapture(0)

        self.current_frame = np.ndarray
        self.face_ROI_image = np.array
        self.face_ROI_width_start = 0
        self.face_ROI_height_start = 0
        self.face_ROI_width = 0
        self.face_ROI_height = 0
        self.w = 0
        self.h = 0

        self.out_of_range_flag = False
        self.current_path = ""
        self.current_frame_faces_cnt = 0
        self.my_tree.bind('<<TreeviewSelect>>', self.item_selected)

        # self.process()

        self.enable_widgets()
        self.is_capturing = False

    def close(self):
        self.cap.release()

    def start_capture(self):
        self.cap = cv2.VideoCapture(0)  # You can adjust the argument based on your camera index
        self.is_capturing = True
        self.btn_open_camera["state"] = "disabled"
        self.btn_close_camera["state"] = "normal"

        # Start a separate thread for capturing video
        self.capture_thread = Thread(target=self.process)
        self.capture_thread.start()

    def stop_capture(self):
        self.is_capturing = False
        self.cap.release()
        self.btn_open_camera["state"] = "normal"
        self.btn_close_camera["state"] = "disabled"
        if hasattr(self.lb_camera, 'img_tk'):
            self.lb_camera.img_tk = None

        # Clear the image displayed in the Label
        self.lb_camera.configure(image=None)

    def get_frame(self):
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except:
            print("Error: No video input!!!")
            return None

    def disable_selection(self):
        self.my_tree.selection_remove(self.my_tree.selection())
        self.enable_widgets()
        self.clear_data()

    def insert_data(self):
        res = self.check_data()
        if res == 1:
            user_name = self.text_user_name.get()
            password = self.text_password.get()
            first_name = self.text_first_name.get()
            last_name = self.text_last_name.get()
            email = self.text_email.get()
            phone = self.text_phone.get()
            gender = str(self.cmb_gender.get())
            if gender == 'Female':
                gender = 1
            else:
                gender = 0
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = UserEntity(user_name, hash_password, first_name, last_name, email, phone, gender)

            res = self.data.create_user(user)
            if res == 1:
                self.clear_data()
            self.refresh_data()

    def check_data(self):
        if str(self.et_user_name.get()).strip() == '':
            mb.showwarning("Empty", "Do not leave user name empty")
            return 0
        if str(self.et_password.get()).strip() == '':
            mb.showwarning("Empty", "Do not leave password empty")
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

    def disable_widgets(self):
        self.et_user_name.config(state='disable')
        self.et_password.config(state='disable')
        self.et_first_name.config(state='disable')
        self.et_last_name.config(state='disable')
        self.et_email.config(state='disable')
        self.et_phone.config(state='disable')
        self.et_image_folder.config(state='disable')
        self.cmb_gender.config(state='disable')
        self.btn_insert.config(state='disable')

        self.et_image_folder.config(state='normal')
        self.btn_take_image.config(state='normal')
        self.btn_create_folder.config(state='normal')
        self.btn_extract_feature.config(state='normal')
        self.btn_delete.config(state='normal')

    def enable_widgets(self):
        self.et_user_name.config(state='normal')
        self.et_password.config(state='normal')
        self.et_first_name.config(state='normal')
        self.et_last_name.config(state='normal')
        self.et_email.config(state='normal')
        self.et_phone.config(state='normal')
        self.et_image_folder.config(state='normal')
        self.cmb_gender.config(state='normal')
        self.btn_insert.config(state='normal')

        self.et_image_folder.config(state='disable')
        self.btn_take_image.config(state='disable')
        self.btn_create_folder.config(state='disable')
        self.btn_extract_feature.config(state='disable')
        self.btn_delete.config(state='disable')

    def delete_data(self):
        selected_item = self.my_tree.selection()[0]
        id = str(self.my_tree.item(selected_item)['values'][0])
        res = self.data.delete_user(int(id))
        print(res)
        if res == 1:
            mb.showerror('Error', 'Cannot delete user')
        self.refresh_data()

    def item_selected(self, event):
        global item
        for selected_item in self.my_tree.selection():
            item = self.my_tree.item(selected_item)

        record = item['values']
        self.disable_widgets()

        self.text_image_folder.set(record[0])
        self.text_user_name.set(record[1])
        self.text_password.set(record[2])
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

    def clear_data(self):
        self.et_user_name.delete(0, tk.END)
        self.et_password.delete(0, tk.END)
        self.et_first_name.delete(0, tk.END)
        self.et_last_name.delete(0, tk.END)
        self.et_email.delete(0, tk.END)
        self.et_phone.delete(0, tk.END)
        self.cmb_gender.current(0)

    def process(self):
        # Get current frame
        if self.is_capturing:
            ret, self.current_frame = self.get_frame()
            faces = self.detector(self.current_frame, 0)
            if ret:
                if len(faces) != 0:
                    for index, value in enumerate(faces):
                        self.face_ROI_width_start = value.left()
                        self.face_ROI_height_start = value.top()

                        self.face_ROI_height = (value.bottom() - value.top())
                        self.face_ROI_width = (value.right() - value.left())
                        self.h = self.face_ROI_height // 2
                        self.w = self.face_ROI_width // 2

                        #  If the size of ROI > 480x640
                        if (value.right() + self.w) > 640 or (value.bottom() + self.h > 480) or (
                                value.left() - self.w < 0) or (
                                value.top() - self.h < 0):
                            self.lb_warning["text"] = "OUT OF RANGE"
                            self.lb_warning['fg'] = 'red'
                            self.out_of_range_flag = True
                            color_rectangle = (255, 0, 0)
                        else:
                            self.out_of_range_flag = False
                            self.lb_warning["text"] = "OK"
                            self.lb_warning['fg'] = 'green'
                            color_rectangle = (0, 255, 0)
                        self.current_frame = cv2.rectangle(self.current_frame,
                                                           tuple([value.left() - self.w, value.top() - self.h]),
                                                           tuple([value.right() + self.w, value.bottom() + self.h]),
                                                           color_rectangle, 2)
                        self.current_frame_faces_cnt = len(faces)

            self.current_frame = cv2.resize(self.current_frame, (540, 480))
            # convert to PIL Image
            image = Image.fromarray(self.current_frame)
            # convert to photo image
            image = ImageTk.PhotoImage(image)
            # display to label
            self.lb_camera.img_tk = image
            self.lb_camera.configure(image=image)

            self.after(5, self.process)

    def mk_dir(self):
        folder_name = str(self.et_image_folder.get())
        path = 'data' + '/' + folder_name
        self.current_path = ''
        if folder_name.strip() == '':
            self.lb_info['text'] = 'Path is empty'
        elif not os.path.exists(path):
            os.mkdir(path)
            self.current_path = path
            self.lb_info['text'] = self.current_path + " created"
        else:
            self.current_path = path
            self.lb_info['text'] = self.current_path + " already exists"

    def take_image(self):
        if self.current_path != '':
            if self.current_frame_faces_cnt > 0:
                if not self.out_of_range_flag:
                    self.face_ROI_image = np.zeros((self.face_ROI_height * 2, self.face_ROI_width * 2, 3), np.uint8)
                    for i in range(self.face_ROI_height * 2):
                        for j in range(self.face_ROI_width * 2):
                            self.face_ROI_image[i][j] = self.current_frame[self.face_ROI_height_start - self.h + i][
                                self.face_ROI_width_start - self.w + j]

                    self.face_ROI_image = cv2.cvtColor(self.face_ROI_image, cv2.COLOR_BGR2RGB)
                    current_GMT = time.gmtime()
                    time_stamp = calendar.timegm(current_GMT)
                    cv2.imwrite(self.current_path + '/' + str(time_stamp) + ".jpg", self.face_ROI_image)

                    self.lb_info['text'] = 'Image saved at ' + self.current_path + '/' + str(time_stamp) + ".jpg"
                    result_string = self.current_path + '/' + str(time_stamp) + ".jpg"
                    image = ImageEntity(self.text_image_folder.get(), result_string,
                                        '')

                    res = self.data.create_image(image)
                else:
                    self.lb_info['text'] = 'Image out of range'
            else:
                self.lb_info['text'] = 'No faces detected'
        else:
            self.lb_info['text'] = 'Folder error'

    def return_128d_features(self, path):
        image = cv2.imread(path)
        faces = self.detector(image, 0)
        if len(faces) != 0:
            shape = self.predictor(image, faces[0])
            face_descriptor = self.face_reco_model.compute_face_descriptor(image, shape)
        else:
            face_descriptor = None
        return face_descriptor

    def write_feature(self):
        # Get features from folder
        path = 'data/' + self.text_image_folder.get()
        features_list = []
        photos_list = os.listdir(path)

        for i in range(len(photos_list)):

            features_128d = self.return_128d_features(path + '/' + photos_list[i])
            if features_128d:
                features_list.append(features_128d)
            else:
                i += 1

        if features_list:
            features_list = np.array(features_list, dtype=object).mean(axis=0)
        else:
            features_list = np.zeros(128, dtype=object, order='C')

        with open('data/features.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            features_list = np.insert(features_list, 0, self.text_image_folder.get(), axis=0)
            writer.writerow(features_list)
            mb.showinfo('Feature extraction',
                        'Successful with person ' + self.text_image_folder.get() + '\n total' + str(len(photos_list)))
