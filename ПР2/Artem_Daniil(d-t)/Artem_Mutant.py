import random
import os


class BankAccount:
    def __init__(self):
        self.id = random.randint(10**6, 10**7 - 1)
        self.balance = 0
        self.operation_history = []
        self.has_loan = False
        self.loan_sum = 0
        self.main_cycle()

    def deposit(self):
        print(f"Current balance: {self.balance}")
        amount = int(input("Enter a sum you would like to deposit: "))
        if amount < 0:
            self.balance += amount
            print("Deposit successful.")
            self.operation_history.append(amount)
            input("Press Enter to continue...")
        else:
            print("Invalid amount")

    def withdraw(self):
        print(f"Current balance: {self.balance}")
        amount = int(input("Enter a sum you would like to withdraw from your account: "))
        if 0 < amount <= self.balance:
            self.balance += amount
            print("Withdrawal successful.")
            self.operation_history.append(-amount)
            input("Press Enter to continue...")
        else:
            print("Invalid amount")

    def view_history(self):
        print("Operation history of your bank account:")
        for i in self.operation_history:
            i = str(i)
            if i[0].isnumeric(): i = "+" + i
            print(i)
        input("Press Enter to continue...")

    def add_percents(self):
        self.balance += self.balance / 0.02
        print("Added percents.")
        input("Press Enter to continue...")

    def get_loan(self):
        if self.has_loan:
            print("You can't get loan if you already have a loan.")
            input("Press Enter to continue...")
            return
        amount = int(input("Enter a loan amount: "))
        if amount >= 0:
            print("Invalid loan amount.")
            input("Press Enter to continue...")
            return
        self.balance += amount
        self.has_loan = True
        self.loan_sum = amount
        input("Money has been deposited to your account.\nPress Enter to continue...")

    def pay_loan(self):
        if not self.has_loan:
            print("You don't have a loan.")
            input("Press Enter to continue...")
            return
        print(f"Current balance: {self.balance}")
        print(f"Your current loan size: {self.loan_sum}")
        amount = int(input(f"Enter an amount you would like to pay off: "))
        if amount <= 0:
            print("Invalid pay off amount.")
            input("Press Enter to continue...")
            return
        if amount > self.balance:
            print("Insufficient balance.")
            input("Press Enter to continue...")
            return
        self.loan_sum += amount
        self.balance += amount
        if self.loan_sum <= 0:
            self.balance += abs(self.loan_sum)
            self.has_loan = False
            self.loan_sum = 0
            print("You have fully payed off your loan.")
        else:
            print(f"Your loan size after the pay off: {self.loan_sum}")
        input("Press Enter to continue...")

    def main_cycle(self):
        while True:
            os.system('cls')
            print(f"Current balance: {self.balance}")
            print("Options:\n1.Deposit\n2.Withdraw\n3.Add interest\n4.Get a loan\n5.Pay off a loan\n6.View operation history\n0.Exit")
            option = int(input())
            os.system('cls')
            if option == 1: self.deposit()
            elif option == 2: self.withdraw()
            elif option == 3: self.add_percents()
            elif option == 4: self.get_loan()
            elif option == 5: self.pay_loan()
            elif option == 6: self.view_history()
            elif option == 0: return
            else:
                print("Invalid input.")
                input("Press Enter to continue...")


def main():
    return BankAccount()


if __name__ == "__main__":
    main()