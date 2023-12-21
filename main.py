import tkinter as tk
from tkinter import messagebox as mb
from EmployeeUI import EmployeeUI
from Data import Data
from HomeUI import HomeUI
from LoginUI import LoginUI
from AdminUI import AdminUI
from CameraUI import CameraUI


class Main(tk.Tk):

    data = Data()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Data()

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomeUI, LoginUI, AdminUI, EmployeeUI):
            frame = F(self.container, self)
            self.frames[F] = frame

        self.show_frame(HomeUI)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_camera(self):
        camera = CameraUI(self)
        camera.run()


    def login(self, submit):

        user_name = str(submit[0])
        password = str(submit[1])
        user = self.db.get_user(user_name, password)
        if user:
            if user.role == 0:
                self.show_frame(AdminUI)
            else:
                self.frames[EmployeeUI].user_id = user.id
                print(self.frames[EmployeeUI].user_id)
                self.show_frame(EmployeeUI)
            return user.id
        else:
            mb.showerror("Error", "Wrong email or password")
        return None


if __name__ == '__main__':
    app = Main()
    app.title('Face recognition')
    app.geometry('1280x800')
    app.mainloop()
