from tkinter import *
from banking import bank


class DesktopInterface:
    def __init__(self):
        self.b1 = Button(root, text="Создать аккаунт",).place(relx=0.1, rely=0.1)
        self.b2 = Button(root, text="Войти в аккаунт").place(relx=0.1, rely=0.2)
        self.b3 = Button(root, text='Выход', command=self.close).place(relx=0.9, rely=0.9)
        self.l1 = Label(root, width=50)
        self.l2 = Label(root)
        # self.b1.pack()
        #self.b2.pack()
        #self.b3.pack()
        self.l1.pack()
        self.login_field = Entry(root, width=50)
        self.pin_field = Entry(root, width=50)
        #self.b1.bind('<Button-1>', self.print_generated_card)
        #self.b2.bind('<Button-1>', self.login_try)

    def print_generated_card(self, event):
        bank.create_account(1)
        self.l1['text'] = 'Ваш номер карты:', bank.last_generated_card_number
        self.l2['text'] = 'Ваш PIN:', bank.last_pin
        self.l2.pack()

    def login_try(self, event):
        self.l1['text'] = "Введите номер карты"
        self.login_field.pack()
        self.l2['text'] = "Введите PIN"
        self.l2.pack()
        self.pin_field.pack()

    def close(self):
        root.destroy()
        root.quit()


root = Tk()
root.title('Банкинг')
root.geometry('640x480')
first_window = DesktopInterface()
root.mainloop()
