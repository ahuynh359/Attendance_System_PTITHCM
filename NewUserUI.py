import csv
import os
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


class NewUser(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        # Input frame - New User Frame Left
        self.new_user_frame_left = tk.Frame(self)

        self.lb_user_name = ttk.Label(self.new_user_frame_left, text='User Name')
        self.lb_user_name.grid(row=0, column=0, padx=15, pady=5)

        self.text_user_name = tk.StringVar()
        self.et_user_name = ttk.Entry(self.new_user_frame_left, width=25, textvariable=self.text_user_name)
        self.et_user_name.grid(row=1, column=0, padx=10, pady=5)

        self.lb_password = ttk.Label(self.new_user_frame_left, text='Password')
        self.lb_password.grid(row=2, column=0, padx=15, pady=5)

        self.text_password = tk.StringVar()
        self.et_password = ttk.Entry(self.new_user_frame_left, width=25, show='*', textvariable=self.text_password)
        self.et_password.grid(row=3, column=0, padx=10, pady=5)

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

        self.lb_image = ttk.Label(self.new_user_frame_left, text='Image')
        self.lb_image.grid(row=6, column=1, padx=15, pady=5)

        self.btn_take_image = ttk.Button(
            self.new_user_frame_left, text="Take Image", command=self.take_image)
        self.btn_take_image.grid(row=7, column=1, padx=10, pady=5)

        self.lb_info = ttk.Label(self.new_user_frame_left, foreground='red')
        self.lb_info.grid(row=8, column=0, pady=5, padx=15, columnspan=2)

        self.btn_insert = ttk.Button(
            self.new_user_frame_left, text="Add New User", command=self.insert_data)
        self.btn_insert.grid(row=10, column=0, columnspan=2, padx=10, pady=15)

        self.new_user_frame_left.pack(side=tk.LEFT)

        # Camera frame - New User Frame Right
        self.new_user_frame_right = tk.Frame(self)
        self.btn_open_camera = ttk.Button(self.new_user_frame_right, text='Open Camera', compound=tk.LEFT,
                                          command=self.start_capture)
        self.btn_open_camera.pack(side=tk.TOP)

        self.btn_close_camera = ttk.Button(self.new_user_frame_right, text='Close Camera', compound=tk.LEFT,
                                           command=self.stop_capture)
        self.btn_close_camera.pack(side=tk.TOP)

        self.lb_warning = tk.Label(self.new_user_frame_right, text='OK', fg='green')
        self.lb_warning.pack(side=tk.TOP, pady=5)

        self.lb_camera = ttk.Label(self.new_user_frame_right)
        self.image_lb_camera = ImageTk.PhotoImage(Image.open('src/camera.png'))
        self.lb_camera.img_tk = self.image_lb_camera
        self.lb_camera.configure(image=self.image_lb_camera)
        self.lb_camera.pack(side=tk.TOP)

        self.new_user_frame_right.pack(expand=1, fill=tk.BOTH)
        self.capture_thread = None

        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()

        self.current_frame = np.ndarray
        self.face_ROI_image = np.array
        self.face_ROI_width_start = 0
        self.face_ROI_height_start = 0
        self.face_ROI_width = 0
        self.face_ROI_height = 0
        self.face_ROI_half_width = 0
        self.face_ROI_half_height = 0

        self.out_of_range_flag = False
        self.current_path = "data/image_data"
        self.current_frame_faces_cnt = 0

        self.predictor = dlib.shape_predictor(
            'data/data_dlib/shape_predictor_68_face_landmarks.dat')
        self.face_reco_model = dlib.face_recognition_model_v1(
            'data/data_dlib/dlib_face_recognition_resnet_model_v1.dat')

        self.data = controller.data

        self.is_capturing = False

    def take_image(self):
        if self.current_frame_faces_cnt > 0:
            if self.current_frame_faces_cnt == 1:
                if not self.out_of_range_flag:

                    # create matrix filled with 0
                    self.face_ROI_image = np.zeros((self.face_ROI_height * 2, self.face_ROI_width * 2, 3), np.uint8)

                    # get every cell of image
                    for i in range(self.face_ROI_height * 2):
                        for j in range(self.face_ROI_width * 2):
                            self.face_ROI_image[i][j] = \
                                self.current_frame[self.face_ROI_height_start - self.face_ROI_half_height + i][
                                    self.face_ROI_width_start - self.face_ROI_half_width + j]

                    self.face_ROI_image = cv2.cvtColor(self.face_ROI_image, cv2.COLOR_BGR2RGB)

                    current_gmt = time.gmtime()
                    time_stamp = calendar.timegm(current_gmt)
                    path = self.current_path + '/' + self.data.get_next_id_user() + '_' + str(time_stamp) + ".jpg"
                    print(path)
                    cv2.imwrite(path, self.face_ROI_image)

                    self.lb_info['text'] = 'Image saved at ' + path
                    image = ImageEntity(self.data.get_next_id_user(), path, '')
                    self.data.create_image(image)
                else:
                    self.lb_info['text'] = 'Image out of range'
            else:
                self.lb_info['text'] = 'There is more than one person in the frame'
        else:
            self.lb_info['text'] = 'No faces detected'

    def start_capture(self):
        self.cap = cv2.VideoCapture(0)
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
        self.lb_camera.img_tk = self.image_lb_camera
        self.lb_camera.configure(image=self.image_lb_camera)

    def get_frame(self):
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception as err:
            print("Error: No video input!!! " + str(err))
            return None

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

    def clear_data(self):
        self.et_user_name.delete(0, tk.END)
        self.et_password.delete(0, tk.END)
        self.et_first_name.delete(0, tk.END)
        self.et_last_name.delete(0, tk.END)
        self.et_email.delete(0, tk.END)
        self.et_phone.delete(0, tk.END)
        self.cmb_gender.current(0)

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

            ress = self.data.create_user(user)
            if ress == 1:
                self.write_feature(str(self.data.get_user_id(self.text_user_name.get())))
                mb.showinfo("Success", "Create new user successfully")
                self.clear_data()
            else:
                mb.showerror("Failed", "Create new user failed")

    def process(self):

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
                        self.face_ROI_half_height = self.face_ROI_height // 2
                        self.face_ROI_half_width = self.face_ROI_width // 2

                        #  If the size of ROI > 480x640
                        if (value.right() + self.face_ROI_half_width) > 640 or (
                                value.bottom() + self.face_ROI_half_height > 480) or (
                                value.left() - self.face_ROI_half_width < 0) or (
                                value.top() - self.face_ROI_half_height < 0):
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
                                                           tuple([value.left() - self.face_ROI_half_width,
                                                                  value.top() - self.face_ROI_half_height]),
                                                           tuple([value.right() + self.face_ROI_half_width,
                                                                  value.bottom() + self.face_ROI_half_height]),
                                                           color_rectangle, 2)

                self.current_frame_faces_cnt = len(faces)

                image = Image.fromarray(self.current_frame)
                image = ImageTk.PhotoImage(image)
                self.lb_camera.img_tk = image
                self.lb_camera.configure(image=image)

            self.after(5, self.process)

    def return_128d_features(self, path):
        image = cv2.imread(path)
        faces = self.detector(image, 0)
        if len(faces) != 0:
            shape = self.predictor(image, faces[0])
            face_descriptor = self.face_reco_model.compute_face_descriptor(image, shape)
        else:
            face_descriptor = None
        return face_descriptor

    def write_feature(self, id):
        # Get all files in path
        path = [f for f in os.listdir(self.current_path) if f.startswith(id)]
        print(path)
        features_list = []

        for i in range(len(path)):

            features_128d = self.return_128d_features(self.current_path + '/' + path[i])
            if features_128d:
                features_list.append(features_128d)
            else:
                i += 1

        if features_list:
            features_list = np.array(features_list, dtype=object).mean(axis=0)
        else:
            features_list = np.zeros(128, dtype=object, order='C')

        with open('data/features.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            features_list = np.insert(features_list, 0, id, axis=0)
            writer.writerow(features_list)
            mb.showinfo('Feature extraction',
                        'Successful with person ' + id + '\n total' + str(len(path)))
