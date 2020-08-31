import random
import sqlite3

'''
добавить GUI 
'''

# инициализация sqlite3, создание таблицы
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card
            (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)""")
conn.commit()


# генерация контрольной суммы по алгоритму Луна (Luhn algorithm)
def check_sum(acc_id):
    numbers_list = []
    for i in acc_id:
        numbers_list.append(int(i))
    for i in range(0, len(numbers_list)):
        if i % 2 == 0:
            numbers_list[i] = numbers_list[i] * 2
            if numbers_list[i] > 9:
                numbers_list[i] = numbers_list[i] - 9

    remainder = sum(numbers_list) % 10
    checksum = 10 - remainder
    if checksum == 10:
        checksum = 0
    return str(checksum)


# генерация последовательностей (PIN, card number)
def generate_sequence(size):
    numbers_list = []
    for i in range(0, size):
        a = str(random.randint(0, 9))
        numbers_list.append(a)
    sequence = ''.join(numbers_list)
    return sequence


class BankingSystem:

    def __init__(self):
        self.command = None
        self.login_card = None  # № залогиенной карты
        self.balance = None  # баланс
        self.last_generated_card_number = None
        self.last_pin = None
        self.main()

    def main(self):
        # self.get_main_menu()
        pass

    def get_main_menu(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        while True:
            self.command = input()
            if self.command == '1':
                self.create_account()
            elif self.command == '2':
                self.log_into()
            elif self.command == '0':
                self.fin()

    def fin(self):
        print()
        print('Bye!')
        # cur.execute('DROP TABLE card;')
        # conn.commit()
        conn.close()
        exit()

    def get_login_menu(self):
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        self.command = None
        while True:
            self.command = input()
            if self.command == '1':
                self.get_balance()
            elif self.command == '2':
                self.add_income()
            elif self.command == '3':
                self.do_transfer()
            elif self.command == '4':
                self.close_account()
            elif self.command == '5':
                print('You have successfully logged out!')
                self.get_main_menu()
            elif self.command == '0':
                self.fin()

    def get_balance(self):
        cur.execute('SELECT balance FROM card WHERE number =?', (self.login_card,))
        balance = cur.fetchall()[0][0]
        conn.commit()
        print()
        print('Balance:', balance)
        print()
        self.get_login_menu()

    def add_income(self):
        print()
        print('Enter income:')
        funds_to_add = input()
        cur.execute('SELECT balance FROM card WHERE number =?', (self.login_card,))
        self.balance = int(cur.fetchall()[0][0]) + int(funds_to_add)
        cur.execute('UPDATE card SET balance =? WHERE number =?', (self.balance, self.login_card))
        conn.commit()
        print('Income was added!')
        self.get_login_menu()

    # перевод средств на другую карту
    def do_transfer(self):
        print('Enter card number:')
        recipient_number = input()

        # поиск подстроки (проверка по алгоритму Луна) ??? пишет ошибку в тесте
        cur.execute("SELECT number FROM card WHERE instr(number,?)>0 AND number<>?;",
                    (recipient_number[:-1], recipient_number))
        rn_from_db = cur.fetchall()
        conn.commit()
        if rn_from_db:
            print('Probably you made mistake in the card number. Please try again!')
            print()
            self.get_login_menu()
        # поиск строки
        cur.execute('SELECT number FROM card WHERE number =?', (recipient_number,))
        rn_from_db = cur.fetchall()
        conn.commit()

        if not rn_from_db:
            print('Such a card does not exist.')
            print()
            self.get_login_menu()
        elif recipient_number == self.login_card:
            print("You can't transfer money to the same account!")
            print()
            self.get_login_menu()
        else:
            print('Enter how much money you want to transfer:')
            funds_to_transfer = int(input())
            cur.execute('SELECT balance FROM card WHERE number =?', (self.login_card,))
            self.balance = int(cur.fetchall()[0][0])
            conn.commit()
            if funds_to_transfer > self.balance:
                print('Not enough money!')
            else:
                self.balance -= funds_to_transfer
                cur.execute('UPDATE card SET balance =? WHERE number =?', (self.balance, self.login_card))
                cur.execute('SELECT balance FROM card WHERE number =?', (recipient_number,))
                recipient_balance = int(cur.fetchall()[0][0]) + funds_to_transfer
                cur.execute('UPDATE card SET balance =? WHERE number =?', (recipient_balance, recipient_number))
                conn.commit()
                print('Success!')

    def close_account(self):
        cur.execute('DELETE FROM card WHERE number =?', (self.login_card,))
        conn.commit()
        print('The account has been closed!')
        self.get_main_menu()

    def generate_full_number(self, generated_card_number):
        card_number = '400000' + generated_card_number + check_sum(
            '400000' + generated_card_number)
        return card_number

    def create_account(self, event):
        generated_card_number = generate_sequence(9)
        card_number = self.generate_full_number(generated_card_number)
        cur.execute('SELECT number FROM card WHERE number =?', (card_number,))
        cn_from_db = cur.fetchall()
        if not cn_from_db:
            print()
            print('Your card has been created')
            print('Your card number:')
            print(card_number)
            print('Your card PIN:')
            pin = generate_sequence(4)
            print(pin)
            cur.execute('INSERT INTO card (number,pin,balance)VALUES(?,?,?)',  # id - PK
                        (card_number, pin, 0))
            conn.commit()
            print()
            #   self.get_main_menu()
            self.last_generated_card_number = card_number
            self.last_pin = pin
        else:
            self.create_account()  # не оптимально

    def log_into(self, event):
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        pin = input()
        cur.execute('SELECT number FROM card WHERE number =? AND pin=?',
                    (card_number, pin))  # ищем запись в дб с таким номером карты и пином
        card_from_db = cur.fetchall()
        conn.commit()

        if not card_from_db:
            print('Wrong card number or PIN!')  # запись не найдена, нам вывело []
            print()
            self.get_main_menu()
        else:
            print('You have successfully logged in!')  # номер карты и пин нашлись
            print()
            self.login_card = card_number
            self.get_login_menu()


bank = BankingSystem()
