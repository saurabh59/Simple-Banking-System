import sqlite3
import random
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS card;')
cur.execute('CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()


def bin_number():
    rand0 = random.randrange(100000000, 1000000000)
    return "400000" + str(rand0)


def checksum(j):
    k = list(j)
    i = 0
    for _x in k:
        if i <= 15:
            k[i] = 2 * int(k[i])
        i += 2
    for y in k:
        if int(y) > 9:
            k[k.index(y)] = y - 9
        else:
            k[k.index(y)] = y
    sumk = 0
    for z in k:
        sumk += int(z)
    if sumk % 10 == 0:
        return "0"
    else:
        return str((10 - sumk % 10))


def card_pin():
    rand1 = random.randrange(0, 10)
    rand2 = random.randrange(0, 10)
    rand3 = random.randrange(0, 10)
    rand4 = random.randrange(0, 10)
    return str(rand1) + str(rand2) + str(rand3) + str(rand4)


def main_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")


def card_menu(card):
    while(1):
        print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Logout
0. Exit""")
        card_op = int(input())
        if card_op == 1:
            cur.execute(f"Select balance from card where number = {card}")
            balance = cur.fetchone()[0]
            print(f"Balance: {balance}")
            print()
            continue
        elif card_op == 2:
            print("")
            print("Enter income:")
            income = int(input())
            cur.execute(f"Select balance from card where number = {card}")
            previous_balance = cur.fetchone()[0]
            cur.execute(f"UPDATE card SET balance = {income} + {previous_balance} where number = {card}")
            conn.commit()
            print("Income was added!")
            print()
            continue
        elif card_op == 3:
            print()
            print("Transfer")
            card_t = input("Enter card number:")
            cur.execute(f"SELECT number,balance FROM card where number = {card_t}")
            s = cur.fetchone()
            k = checksum(card_t)
            j = len(card_t)
            if k == '0' and j == 16:
                if s:
                    if card != s[0]:
                        print("Enter how much money you want to transfer:")
                        transfer = input()
                        cur.execute(f"select balance from card where number = {card}")
                        v = cur.fetchone()
                        if v[0] < int(transfer):
                            print("Not enough money!")
                        else:
                            cur.execute(f"UPDATE card SET balance = {int(v[0])} - {int(transfer)} where number = {card}")
                            conn.commit()
                            cur.execute(f"UPDATE card SET balance = {int(s[1])}  + {int(transfer)} where number = {int(card_t)}")
                            conn.commit()
                            print("Success!")
                    else:
                        print("You can't transfer money to the same account!")
                else:
                    print("Such a card does not exist.")
            else:
                print("Probably you made a mistake in the card number. Please try again!")
        elif card_op == 4:
            cur.execute(f"DElETE FROM card WHERE number = {card}")
            print()
            print("The account has been closed!")
            conn.commit()
            print()
            break
        elif card_op == 5:
            break
        elif card_op == 0:
            quit()
a = 0
vault = {}
while True:
    main_menu()
    user_input = input()
    if user_input == "1":
        print()
        print("Your card has been created")
        bin = bin_number()
        cardnumber = bin + checksum(bin)
        cardpin = card_pin()
        vault[cardnumber] = cardpin
        print("Your card number:")
        print(f"{cardnumber}")
        print("Your card PIN:")
        print(f"{cardpin}")
        print()
        cur.execute("insert into card values(?, ?, ?, ?)", (a, cardnumber, cardpin, 0))
        conn.commit()
        a += 1
    elif user_input == "2":
        print()
        card = input("Enter your card number:")
        pin = input("Enter you PIN:")
        cur.execute(f"SELECT number,pin FROM card where pin ={pin}")
        card_fetch = cur.fetchone()
        if card_fetch and card_fetch[0] == card:
            print()
            print("You have successfully logged in!")
            print()
            card_menu(card)
        else:
            print()
            print("Wrong card number or PIN!")
    elif user_input == "0":
        print()
        print("Bye!")
        break
