from enum import Enum
from math import ceil
from math import log
from math import floor
import argparse


class MenuOptions(Enum):
    COUNT_OF_MONTH = "n"
    ANNUITY_MONTHLY_PAYMENT = "a"
    CREDIT_PRINCIPAL = "p"


class TypeOption(Enum):
    DIFF = "diff"
    ANNUITY = "annuity"


class CreditCalculator:
    def __init__(self):
        self.__menu_option = None
        self.__credit_principal = None
        self.__monthly_payment = None
        self.__count_of_months = None
        self.__annuity_payment = None
        parser = argparse.ArgumentParser()
        parser.add_argument("--type", type=str)
        parser.add_argument("--payment", type=int)
        parser.add_argument("--principal", type=int)
        parser.add_argument("--periods", type=int)
        parser.add_argument("--interest", type=float)
        self.__args = vars(parser.parse_args())

    def __menu(self):
        print("What do you want to calculate?")
        print('type "n" for the count of months,')
        print('type "a" for the annuity monthly payment,')
        print('type "p" for the credit principal:')
        self.__menu_option = MenuOptions(input())

    def __calcucalate_number_of_month(self):
        number = round(self.__credit_principal / self.__monthly_payment)
        s = ""
        if number > 1:
            s = "s"
        return f"\nIt take {number} month{s} to repay the credit"

    def __calcucalate_monthly_payment(self):
        payment = ceil(self.__credit_principal / self.__count_of_months)
        last_payment = ceil(self.__credit_principal - (self.__count_of_months - 1) * payment)
        if payment == last_payment:
            return f"Your monthly payment = {payment}"
        return f"Your monthly payment = {payment} with last monthly payment = {last_payment}"

    def __get_count_of_months(self):
        self.__set_credit_principal()
        self.__set_monthly_payment()
        self.__set_credit_interest()
        self.__calculate_nominal_interest()
        value = self.__monthly_payment / (
                self.__monthly_payment - self.__nominal_interest_rate * self.__credit_principal)
        base = 1 + self.__nominal_interest_rate
        self.__count_of_months = log(value, base)
        self.__count_of_months = ceil(self.__count_of_months)
        months = self.__count_of_months % 12
        years = self.__count_of_months // 12
        result = "You need "
        if years > 0:
            s = ""
            if years > 1:
                s = "s"
            result += f"{years} year{s} "
        if months > 0:
            if years > 0:
                result += "and "
            s = ""
            if months > 1:
                s = "s"
            result += f"{months} month{s} "
        result += "to repay this credit!"
        return result

    def __get_credit_principal(self):
        self.__set_annuity_payment()
        self.__set_count_of_periods()
        self.__set_credit_interest()
        self.__calculate_nominal_interest()
        i = self.__nominal_interest_rate
        n = self.__count_of_months
        down = (i * (1 + i) ** n) / ((1 + i) ** n - 1)
        self.__credit_principal = round(self.__annuity_payment / down)
        return f"Your credit principal = {self.__credit_principal}!"

    def get_annuity_monthly_payment(self):
        self.__set_credit_principal()
        self.__set_count_of_periods()
        self.__set_credit_interest()
        self.__calculate_nominal_interest()
        p = self.__credit_principal
        i = self.__nominal_interest_rate
        n = self.__count_of_months
        up = i * (1 + i) ** n
        down = (1 + i) ** n - 1
        self.__annuity_payment = ceil(p * up / down)
        return f"Your annuity payment = {self.__annuity_payment}"

    def __calculate_nominal_interest(self):
        self.__nominal_interest_rate = self.__credit_interest / 12

    def __set_count_of_periods(self):
        print("Enter the count of periods:")
        self.__count_of_months = int(input())

    def __set_annuity_payment(self):
        print("Enter the annuity payment:")
        self.__annuity_payment = float(input())

    def __set_credit_principal(self):
        print("Enter the credit principal:")
        self.__credit_principal = float(input())

    def __set_monthly_payment(self):
        print("Enter the monthly payment:")
        self.__monthly_payment = float(input())

    def __set_credit_interest(self):
        print("Enter the credit interest:")
        self.__credit_interest = float(input()) / 100

    def __tui(self):
        self.__menu()
        if self.__menu_option == MenuOptions.COUNT_OF_MONTH:
            print(self.__get_count_of_months())
        if self.__menu_option == MenuOptions.CREDIT_PRINCIPAL:
            print(self.__get_credit_principal())
        if self.__menu_option == MenuOptions.ANNUITY_MONTHLY_PAYMENT:
            print(self.get_annuity_monthly_payment())

    def __cmd(self):
        try:
            self.__args["type"] = TypeOption(self.__args["type"])
        except ValueError:
            return self.__print_error_cmd()
        if self.__args["interest"] is None:
            return self.__print_error_cmd()
        if self.__args["type"] == TypeOption.DIFF:
            if self.__args["payment"] is not None:
                return self.__print_error_cmd()
            self.__diff()
        if self.__args["type"] == TypeOption.ANNUITY:
            self.__annuity()

    def __print_error_cmd(self):
        print("Incorrect parameters")
        return False

    def main(self):
        if not any(self.__args.values()):
            self.__tui()
        else:
            self.__cmd()

    def __diff(self):
        if self.__args["principal"] < 0:
            return self.__print_error_cmd()
        if self.__args["periods"] < 0:
            return self.__print_error_cmd()
        if self.__args["interest"] < 0:
            return self.__print_error_cmd()
        self.__calc_diff()

    def __check(self, what):
        assert what is not None
        assert what > 0

    def __annuity(self):
        try:
            interest = self.__args["interest"]
            self.__check(interest)
            payment = self.__args["payment"]
            principal = self.__args["principal"]
            periods = self.__args["periods"]
            if payment is None:
                self.__check(principal)
                self.__check(periods)
            if principal is None:
                self.__check(payment)
                self.__check(periods)
            if periods is None:
                self.__check(payment)
                self.__check(principal)
            self.__calc_annuity_payment(interest, payment, periods, principal)
        except AssertionError:
            return self.__print_error_cmd()

    def __calc_monthly_payment(self, p, i, m, n):
        return p / n + i * (p - p * (m - 1) / n)

    def __calc_diff(self):
        p = self.__args["principal"]
        i = self.__args["interest"] / 12 / 100
        n = self.__args["periods"]
        summation = 0
        for m in range(1, n + 1):
            annuity = ceil(self.__calc_monthly_payment(p, i, m, n))
            summation += annuity
            print(f"Month {m}: payment is {annuity}")
        print()
        print(f"Overpayment = {summation - p}")

    def __calc_annuity_payment(self, interest, payment=None, periods=None, principal=None):
        interest = interest / 12 / 100
        if payment is None and periods is not None and principal is not None:
            up = interest * (1 + interest) ** periods
            down = (1 + interest) ** periods - 1
            payment = ceil(principal * up / down)
            print(f"Your annuity payment = {payment}")
            summation = payment * periods
            print(f"Overpayment = {summation - principal}")
        if principal is None and periods is not None and payment is not None:
            down = (interest * (1 + interest) ** periods) / ((1 + interest) ** periods - 1)
            principal = floor(payment / down)
            summation = payment * periods
            print(f"Your credit principal = {principal}!")
            print(f"Overpayment = {summation - principal}")
        elif periods is None and principal is not None and payment is not None:
            value = payment / (payment - interest * principal)
            base = 1 + interest
            periods = log(value, base)
            periods = ceil(periods)
            summation = periods * payment
            months = periods % 12
            years = periods // 12
            result = "It will take "
            if years > 0:
                s = ""
                if years > 1:
                    s = "s"
                result += f"{years} year{s} "
            if months > 0:
                if years > 0:
                    result += "and "
                s = ""
                if months > 1:
                    s = "s"
                result += f"{months} month{s} "
            result += "to repay this loan!"
            print(result)
            print(f"Overpayment = {summation - principal}")


if __name__ == '__main__':
    calc = CreditCalculator()
    calc.main()
