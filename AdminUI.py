import csv
import os.path
import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter import messagebox as mb
import cv2
import dlib

from ManageUserUI import ManageUserUI
from NewUserUI import NewUser
from ReportUI import ReportUI


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
        path = self.current_path
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
