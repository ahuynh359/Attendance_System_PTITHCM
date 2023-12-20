import dlib
import numpy as np
import cv2
import os
import pandas as pd
from datetime import datetime
from tkinter import messagebox as mb

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


class CameraUI:
    def __init__(self, controller):

        self.db = controller.db
        self.count = 0
        self.cap = None
        self.font = cv2.FONT_ITALIC

        self.face_features_known_list = []
        self.face_name_known_list = []

        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []

        self.last_frame_face_name_list = []
        self.current_frame_face_name_list = []

        self.last_frame_face_cnt = 0
        self.current_frame_face_cnt = 0

        self.current_frame_face_X_e_distance_list = []

        self.current_frame_face_position_list = []
        self.current_frame_face_feature_list = []

        self.last_current_frame_centroid_e_distance = 0

        self.reclassify_interval_cnt = 0

    def get_face_database(self):
        if os.path.exists("data/features.csv"):
            path_features_known_csv = "data/features.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                self.face_name_known_list.append(csv_rd.iloc[i][0])
                for j in range(1, 129):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.face_features_known_list.append(features_someone_arr)
            return 1
        else:
            return 0

    @staticmethod
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            e_distance_current_frame_person_x_list = []
            for j in range(len(self.last_frame_face_centroid_list)):
                self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(
                    self.current_frame_face_centroid_list[i], self.last_frame_face_centroid_list[j])

                e_distance_current_frame_person_x_list.append(
                    self.last_current_frame_centroid_e_distance)

            last_frame_num = e_distance_current_frame_person_x_list.index(
                min(e_distance_current_frame_person_x_list))
            self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]

    def draw_note(self, img_rd):

        cv2.putText(img_rd, "Faces:  " + str(self.current_frame_face_cnt), (20, 160), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

        for i in range(len(self.current_frame_face_name_list)):
            img_rd = cv2.putText(img_rd, "Face_" + str(i + 1), tuple(
                [int(self.current_frame_face_centroid_list[i][0]), int(self.current_frame_face_centroid_list[i][1])]),
                                 self.font,
                                 0.8, (255, 190, 0),
                                 1,
                                 cv2.LINE_AA)

    def process(self, stream):
        if self.get_face_database():
            while stream.isOpened():
                flag, img_rd = stream.read()
                kk = cv2.waitKey(1)

                faces = detector(img_rd, 0)

                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)

                self.last_frame_face_name_list = self.current_frame_face_name_list[:]

                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []

                # if cnt not changes
                if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                        self.reclassify_interval_cnt != 10):

                    print('cnt not changes')
                    print(self.reclassify_interval_cnt)

                    self.current_frame_face_position_list = []

                    if "unknown" in self.current_frame_face_name_list:
                        self.reclassify_interval_cnt += 1

                    # save pos of image
                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(faces):
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            img_rd = cv2.rectangle(img_rd,
                                                   tuple([d.left(), d.top()]),
                                                   tuple([d.right(), d.bottom()]),
                                                   (0, 255, 0), 2)

                    # Multi-faces in current frame, use centroid-tracker to track
                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()
                    # write name
                    for i in range(self.current_frame_face_cnt):
                        if self.current_frame_face_name_list[i] != 'unknown':
                            self.count += 1
                            if self.count == 30:
                                self.cap.release()
                                cv2.destroyAllWindows()
                                from Data import Data
                                from Data import AttendanceEntity
                                current_time = datetime.now()

                                attendance = AttendanceEntity(int(self.current_frame_face_name_list[i]), current_time)
                                self.db.create_attendance(attendance)
                                mb.showinfo('Face Name', 'Success ' + str(self.current_frame_face_name_list[i]))

                        img_rd = cv2.putText(img_rd, str(self.current_frame_face_name_list[i]),
                                             self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                             cv2.LINE_AA)

                    self.draw_note(img_rd)

                #   Faces cnt changes in this frame
                else:
                    print('cnt changes')
                    self.current_frame_face_position_list = []
                    self.current_frame_face_X_e_distance_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0

                    #  No faces in this frame
                    if self.current_frame_face_cnt == 0:
                        print('no face detected')
                        self.current_frame_face_name_list = []

                    #  Get faces in this frame and do face recognition
                    else:
                        print('there are faces')
                        self.current_frame_face_name_list = []

                        # Get feature of image
                        for i in range(len(faces)):
                            shape = predictor(img_rd, faces[i])
                            self.current_frame_face_feature_list.append(
                                face_reco_model.compute_face_descriptor(img_rd, shape))
                            self.current_frame_face_name_list.append("unknown")

                        # Save pos of image
                        for k in range(len(faces)):
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            self.current_frame_face_X_e_distance_list = []

                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                            # For every faces detected, compare the faces in the database
                            for i in range(len(self.face_features_known_list)):
                                if str(self.face_features_known_list[i][0]) != '0.0':
                                    e_distance_tmp = self.return_euclidean_distance(
                                        self.current_frame_face_feature_list[k],
                                        self.face_features_known_list[i])
                                    self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                else:
                                    self.current_frame_face_X_e_distance_list.append(999999999)
                            #  Find the one with minimum e distance
                            similar_person_num = self.current_frame_face_X_e_distance_list.index(
                                min(self.current_frame_face_X_e_distance_list))

                            if min(self.current_frame_face_X_e_distance_list) < 0.4:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]

                        self.draw_note(img_rd)

                if kk == ord('q'):
                    break

                cv2.namedWindow("camera", 1)
                cv2.imshow("camera", img_rd)

    def run(self):
        self.cap = cv2.VideoCapture(0)  # Get video stream from camera
        self.process(self.cap)

        self.cap.release()
        cv2.destroyAllWindows()
