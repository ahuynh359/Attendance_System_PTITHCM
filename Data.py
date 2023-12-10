import os
from datetime import datetime

import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Sequence, BINARY, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

Base = declarative_base()


class User(Base):
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
    images = relationship('Image', back_populates='user')
    attendances = relationship('Attendance', back_populates='user')

    def __init__(self, user_name, hash_password, first_name=None, last_name=None, email=None, phone_number=None,
                 gender=0, role=1):
        self.user_name = user_name
        self.hash_password = hash_password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.gender = gender
        self.role = role


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image = Column(String(50))
    describe = Column(String(50))

    # Relationship with User
    user = relationship('User', back_populates='images')


class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship with User
    user = relationship('User', back_populates='attendances')


class Data:
    def __init__(self):

        self.engine = create_engine('sqlite:///test.db')
        if not os.path.exists('test.db'):
            Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def read_all_users(self):
        try:
            users = self.session.query(User).all()
            print("All users:")
            for user in users:
                print(user.id, user.user_name, user.email, user.hash_password)
        except ValueError as err:
            print('Error when get all users', err)

    def create_user(self, user):
        try:
            new_user = User(user_name=user.user_name, hash_password=user.hash_password, first_name=user.first_name,
                            last_name=user.last_name,
                            email=user.email, phone_number=user.phone_number, gender=user.gender)
            self.session.add(new_user)
            self.session.commit()
        except ValueError as err:
            print('Error when insert user', err)

    def delete_user(self, user_name):
        try:
            user_to_delete = self.session.query(User).filter_by(user_name=user_name)
            if user_to_delete:
                self.session.delete(user_to_delete)
                self.session.commit()
        except ValueError as err:
            print('Error when delete user', err)

    def get_user_by_credentials(self, user_name: str, password: str):
        user = self.session.query(User).filter_by(user_name=user_name).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hash_password.encode('utf-8')):
            print(user.email)
            return user
        else:
            print('None')
            return None

    def close_session(self):
        self.session.close()
