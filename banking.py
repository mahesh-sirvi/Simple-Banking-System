import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
#cur.execute("DROP TABLE card;")
# conn.commit()
try:
    cur.execute("""
    CREATE TABLE card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );
    """)
    conn.commit()
except Exception:
    pass
records = {}
balance_dict = {}
user_input = ""
while user_input != "0":

    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    user_input = input()

    if user_input == "1":

        while True:
            pin = random.randrange(0000, 10000)
            str_pin = str(pin)
            if len(str_pin) == 4:
                break

        while True:
            ac_no = random.randrange(000000000, 999999999)
            str_ac_no = str(ac_no)

            if len(str_ac_no) == 9:
                break
        d = {}
        iin = "400000"
        card_user = iin + str_ac_no

        odd_digits = []
        even_digits = []
        d = {1: card_user[0], 2: card_user[2], 3: card_user[4], 4: card_user[6], 5: card_user[8], 6: card_user[10],
             7: card_user[12],
             8: card_user[14]}
        d2 = {1: card_user[1], 2: card_user[3], 3: card_user[5], 4: card_user[7], 5: card_user[9], 6: card_user[11],
              7: card_user[13]}
        for x, y in d2.items():
            even_digits.append(int(y))
        for x, y in d.items():
            odd_digits.append(int(y))
        multiplied_odd_digits = []
        for each in odd_digits:
            multiplied_odd_digits.append(each * 2)
        final_d = {1: str(multiplied_odd_digits[0]), 2: str(even_digits[0]), 3: str(multiplied_odd_digits[1]),
                   4: str(even_digits[1]),
                   5: str(multiplied_odd_digits[2]), 6: str(even_digits[2]), 7: str(multiplied_odd_digits[3]),
                   8: str(even_digits[3]),
                   9: str(multiplied_odd_digits[4]), 10: str(even_digits[4]), 11: str(multiplied_odd_digits[5]),
                   12: str(even_digits[5]),
                   13: str(multiplied_odd_digits[6]), 14: str(even_digits[6]), 15: str(multiplied_odd_digits[7])}
        final_list = (final_d.values())
        empty = []
        for x in final_list:
            empty.append(x)
        empty2 = []
        for y in empty:
            empty2.append(int(y))
        subtract_9 = [a - 9 if a > 9 else a for a in empty2]
        add_elements = sum(subtract_9)

        remainder = add_elements % 10

        last_number = ''
        if add_elements % 10 != 0:
            last_number = 10 - remainder
        else:
            last_number = 0
        last_digit = str(last_number)

        card = card_user + last_digit
        print("Your card has been created")
        print("Your card number: ")
        print(card)
        card_number_int = int(card)
        print("Your card PIN:\n{}\n".format(str_pin))
        pin_int = int(pin)
        records.update({card: str_pin})
        balance_dict.update({card: 0})
        new_list = list(records.keys()).index(card)
        index_position = new_list + 1
        cur.execute("INSERT INTO card (id, number, pin) VALUES (?, ?, ?)", (index_position, card, str_pin))
        conn.commit()

    elif user_input == "2":
        user_id = input("Enter your card number: ")
        password = input("Enter your PIN: ")
        if records.get(user_id) == password:
            print("You have successfully logged in!\n")

            new_balance = 0
            while True:
                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")
                user_input = input()

                balance = 0
                if user_input == '1':
                    cur.execute("SELECT balance FROM card WHERE number = (?);", (user_id,))
                    balance = cur.fetchall()
                    print(balance[0][0])
                    conn.commit()


                    #if len(balance_dict) == 0:
                        #print("Balance: {}\n".format(balance))
                   # elif user_id not in balance_dict:
                        #print("Balance: {}\n".format(balance))
                    #elif user_id in balance_dict:
                        #print("Balance: {}\n".format(balance_dict[user_id]))

                elif user_input == '2':
                    income = int(input("Enter income: "))
                    new_balance = new_balance + income
                    balance_dict.update({user_id: new_balance})
                    cur.execute("UPDATE card SET balance = (?) WHERE number = (?);", (new_balance, user_id))
                    conn.commit()
                    print("Income was added!\n")

                elif user_input == '3':
                    print('Enter card number: ')

                    transfer_account = input()
                    original_card = ''
                    for x, y in records.items():
                        if transfer_account[:15] == x[:15]:
                            original_card = x
                    if transfer_account in records and transfer_account != user_id:
                        print("Enter how much money you want to transfer: ")
                        money_transfer = int(input())
                        if money_transfer <= balance_dict[user_id]:
                            current_balance = balance_dict[transfer_account]
                            current_balance_payer = balance_dict[user_id]
                            new_balance = current_balance + money_transfer
                            new_balance_payer = current_balance_payer - money_transfer
                            balance_dict.update({transfer_account: new_balance})
                            cur.execute("UPDATE card SET balance = (?) WHERE number = (?);",
                                        (new_balance, transfer_account))
                            conn.commit()
                            balance_dict.update({user_id: new_balance_payer})
                            cur.execute("UPDATE card SET balance = (?) WHERE number = (?);",
                                        (new_balance_payer, user_id))
                            conn.commit()
                            print('Success!\n')
                        else:
                            print('Not enough money!\n')
                    elif transfer_account == user_id:
                        print("You can't transfer money to the same account!\n")

                    elif len(transfer_account) == 16 and transfer_account[0] == '4':
                        first_half = transfer_account[:15]
                        last_num = transfer_account[-1]
                        last_number = int(last_num)
                        digits = int(first_half)
                        odd_digits = []
                        even_digits = []
                        d = {1: first_half[0], 2: first_half[2], 3: first_half[4], 4: first_half[6], 5: first_half[8],
                             6: first_half[10],
                             7: first_half[12],
                             8: first_half[14]}
                        d2 = {1: first_half[1], 2: first_half[3], 3: first_half[5], 4: first_half[7], 5: first_half[9],
                              6: first_half[11],
                              7: first_half[13]}
                        for x, y in d2.items():
                            even_digits.append(int(y))
                        for x, y in d.items():
                            odd_digits.append(int(y))
                        multiplied_odd_digits = []
                        for each in odd_digits:
                            multiplied_odd_digits.append(each * 2)
                        final_d = {1: str(multiplied_odd_digits[0]), 2: str(even_digits[0]),
                                   3: str(multiplied_odd_digits[1]),
                                   4: str(even_digits[1]),
                                   5: str(multiplied_odd_digits[2]), 6: str(even_digits[2]),
                                   7: str(multiplied_odd_digits[3]),
                                   8: str(even_digits[3]),
                                   9: str(multiplied_odd_digits[4]), 10: str(even_digits[4]),
                                   11: str(multiplied_odd_digits[5]),
                                   12: str(even_digits[5]),
                                   13: str(multiplied_odd_digits[6]), 14: str(even_digits[6]),
                                   15: str(multiplied_odd_digits[7])}
                        final_list = (final_d.values())
                        empty = []
                        for x in final_list:
                            empty.append(x)
                        empty2 = []
                        for y in empty:
                            empty2.append(int(y))
                        subtract_9 = [a - 9 if a > 9 else a for a in empty2]
                        add_elements = sum(subtract_9)
                        remainder = add_elements % 10
                        total_sum = add_elements + last_number
                        if total_sum % 10 != 0:
                            print("Probably you made a mistake in the card number. Please try again!\n")

                    elif transfer_account not in records:
                        print("Such a card does not exist.\n")

                elif user_input == '4':
                    del records[user_id]
                    del balance_dict[user_id]
                    cur.execute("DELETE FROM card WHERE number = (?);", (user_id,))
                    conn.commit()
                    print('The account has been closed!\n')
                    break

                elif user_input == '5':
                    break

                elif user_input == '0':
                    print('Bye!')
                    break
        else:
            print("Wrong card number or PIN!\n")

    elif user_input == "0":
        print('Bye!')
        break





