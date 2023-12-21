import os
from datetime import datetime

import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

Base = declarative_base()


class UserEntity(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True, nullable=False)
    hash_password = Column(String(64))
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone_number = Column(String(11))
    gender = Column(Integer, default=0)
    role = Column(Integer, default=1)

    # Foreign
    images = relationship('ImageEntity', back_populates='user')
    attendances = relationship('AttendanceEntity', back_populates='user')

    def __init__(self, user_name, hash_password, first_name, last_name, email, phone_number,
                 gender=0, role=1):
        self.user_name = user_name
        self.hash_password = hash_password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.gender = gender
        self.role = role


class ImageEntity(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image = Column(String(50))
    describe = Column(String(50))

    # Relationship with User
    user = relationship('UserEntity', back_populates='images')

    def __init__(self, user_id, image, describe=''):
        self.user_id = user_id
        self.image = image
        self.describe = describe


class AttendanceEntity(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime)

    # Relationship with User
    user = relationship('UserEntity', back_populates='attendances')

    def __init__(self, user_id, timestamp):
        self.user_id = user_id
        self.timestamp = timestamp


class Data:
    def __init__(self):

        self.engine = create_engine('sqlite:///test.db')
        if not os.path.exists('test.db'):
            Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def read_all_users(self):
        try:
            users = self.session.query(UserEntity).all()
            return users
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            return None

    def create_image(self, image):
        try:
            new_image = ImageEntity(image.user_id, image.image, image.describe)
            self.session.add(new_image)
            self.session.commit()
            return 1
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            return 0

    def get_image(self, user_id):
        image = self.session.query(ImageEntity).filter_by(user_id=user_id)
        if image:
            return image
        else:
            return None

    def get_attendance_by_user_id(self, user_id, date):
        current_date = datetime.strptime(date, "%d/%m/%Y").date()
        result = (self.session.query(AttendanceEntity).filter_by(user_id=user_id)
                  .filter(func.date(AttendanceEntity.timestamp) == current_date).order_by(
            AttendanceEntity.timestamp).all())
        if result:
            return result
        else:
            return None

    def create_user(self, user):
        try:
            self.session.add(user)
            self.session.commit()
            return 1
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            return 0

    def delete_user(self, id):
        try:
            user_to_delete = self.session.query(UserEntity).filter_by(id=id).first()
            if user_to_delete:
                self.session.delete(user_to_delete)
                self.session.commit()
                return 1
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            return 0


    def get_user(self, user_name: str, password: str):
        user = self.session.query(UserEntity).filter_by(user_name=user_name).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hash_password):
            return user
        else:
            return None

    def get_next_id_user(self):
        id = self.session.query(func.max(UserEntity.id)).first()
        return str(id[0] + 1)

    def get_user_id(self, user_name):
        user = self.session.query(UserEntity).filter_by(user_name=user_name).first()
        return user.id

    def create_attendance(self, attendance):
        try:
            self.session.add(attendance)
            self.session.commit()
            return 1
        except Exception as e:
            print(f"An error occurred: {e}")
            self.session.rollback()
            return 0

    def reset_password(self, id):
        try:
            self.session.query(UserEntity).filter_by(id=id).update({
                "hash_password": bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt()),
            })

            self.session.commit()
            return 1

        except NoResultFound:
            print(f"User with ID {id} not found.")
            return 0

        except Exception as e:
            print('Error when updating user:', e)
            self.session.rollback()
            return 0

    def update_user(self, id, user_name, first_name, last_name, email, phone_number, gender):
        try:
            self.session.query(UserEntity).filter_by(id=id).update({
                "user_name": user_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "gender": gender
            })

            self.session.commit()
            return 1

        except NoResultFound:
            print(f"User with ID {id} not found.")
            return 0

        except Exception as e:
            print('Error when updating user:', e)
            self.session.rollback()
            return 0

    def get_user_with_id(self, id):
        user = self.session.query(UserEntity).filter_by(id=id).first()
        return user

    def change_pass(self,id, password):
        try:
            self.session.query(UserEntity).filter_by(id=id).update({
                "hash_password": password,
            })

            self.session.commit()
            return 1

        except NoResultFound:
            print(f"User with ID {id} not found.")
            return 0

        except Exception as e:
            print('Error when updating user:', e)
            self.session.rollback()
            return 0

    def get_all_user_id(self):
        id_values = self.session.query(UserEntity.id).all()
        id_list = [item[0] for item in id_values]
        return id_list

    def close_session(self):
        self.session.close()
