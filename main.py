import tkinter as tk
from tkinter import messagebox as mb

from Data import Data, User
from ui.Home import Home
from ui.LoginUI import LoginUI
from ui.AdminUI import AdminUI

window_width = 1500
window_height = 900



class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = tk.Frame(self, width=window_width, height=window_height)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.b = False
        self.frames = {}

        for F in (Home, LoginUI, AdminUI):
            frame = F(self.container, self)
            self.frames[F] = frame


        # self.show_frame(Home)
        self.show_frame(AdminUI)
        self.db = Data()

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.grid(row=0, column=0,sticky="nsew")
        frame.tkraise()



    def login(self, submit):

        user_name = str(submit[0])
        password = str(submit[1])

        # hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # user = User(user_name, hash_password,'Tuyet','Nhi','tuyetnhi@gmail.com','1234554566',1)
        user = self.db.get_user_by_credentials(user_name, password)
        if user:
            self.show_frame(AdminUI)
        else:
            mb.showerror("Error", "Wrong email or password")
            print('Wrong email or password')


if __name__ == '__main__':
    app = Main()
    app.title('Face recognition')
    app.resizable(False, False)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_cordinate = (screen_width - window_width) // 2
    y_cordinate = (screen_height - window_height) // 2
    # comment geometry to use this
    # app.eval('tk::PlaceWindow . center')
    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    app.mainloop()
