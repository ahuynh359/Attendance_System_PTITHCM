import hashlib
import os
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

from ui.Home import Home
from ui.LoginUI import LoginUI
from data.Data import Data
from data.User import User

LARGEFONT = ("Verdana", 35)
import bcrypt


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        db = Data()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw('password123'.encode(), salt)
        user = User('john_doe', 'John', 'Doe', 'john.doe@email.com', 'Male', '123-456-7890', hashed_password)
        db.insert_user(user)

        # Retrieving a user by credentials
        username_to_search = 'john_doe'
        password_to_search = 'password123'
        user = db.get_user_by_credentials(username_to_search, password_to_search)

        if user:
            print("User Found:")
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"First Name: {user.first_name}")
            print(f"Last Name: {user.last_name}")
            print(f"Email: {user.email}")
            print(f"Gender: {user.gender}")
            print(f"Phone Number: {user.phone_number}")
            print(f"{user.hash_password}")
        else:
            print(f"User with credentials not found.")
        db.close_connection()

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Home, LoginUI, Page2):
            frame = F(container, self)
            print(frame)
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        try:
            self.img = ImageTk.PhotoImage(file='src/img.png')
            panel = ttk.Label(self, image=self.img)
            panel.grid(row=1, column=1, padx=10, pady=10)
        except Exception as e:
            print(f"Error: {e}")
        # label of frame Layout 2


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# Driver Code
app = tkinterApp()
app.mainloop()
