import tkinter
from .banking import bank

#class DesktopInterface:
#    def __init__(self):
#        pass

#    def gui_creation(self, imported_class):
root = tkinter.Tk()
        # e = tkinter.Entry(root, width=200)
b1 = tkinter.Button(root, text="Создать аккаунт")
b2 = tkinter.Button(root, text="Войти в аккаунт")
l1 = tkinter.Label(root, text='123', width=20)
b1.bind('<Button-1>', bank.create_account())
l1['text'] = bank.last_generated_card_number
        # e.pack()


b1.pack()
b2.pack()
l1.pack()
root.mainloop()
