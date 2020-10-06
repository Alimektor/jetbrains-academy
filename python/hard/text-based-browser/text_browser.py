import argparse
import os
import requests
from collections import deque
from enum import Enum
from bs4 import BeautifulSoup
import colorama

from colorama import Fore


class MenuCommand(Enum):
    EXIT = "exit"
    BACK = "back"


class Browser:
    def __init__(self):
        cmd_parser = argparse.ArgumentParser()
        cmd_parser.add_argument("folder", type=str)
        self.args = cmd_parser.parse_args()
        os.makedirs(os.path.join(os.curdir, self.args.folder), exist_ok=True)
        self.__files = []
        self.__current_webpages = deque()
        self.__current = None
        self.__tags = [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "ul",
            "ol",
            "li",
        ]
        colorama.init()

    def __get_content_of_cash(self, filename):
        result = ""
        with open(os.path.join(os.curdir, self.args.folder, filename), "r", encoding='utf-8') as webpage:
            for line in webpage.readlines():
                result += line
        return result

    def __check_response(self, url):
        if "http://" not in url and "https://" not in url:
            url = "http://" + url
        try:
            self.__current = self.__beautify(url)
        except requests.exceptions.ConnectionError:
            return False
        if not self.__current:
            return False
        self.__add_website_to_cash(url)
        return True

    def __get_response_text(self):
        return self.__current

    def __add_website_to_cash(self, url):
        filename = url.rstrip(".com").lstrip("http://").lstrip("https://")
        self.__files.append(filename)
        with open(os.path.join(os.curdir, self.args.folder, filename), "w", encoding='utf-8') as webpage:
            print(self.__get_response_text(), file=webpage)

    def __check_in_cash(self, url):
        filename = url.rstrip(".com").rstrip("com").lstrip("http://").lstrip("https://")
        return filename in self.__files

    def __add_to_current_webpages(self, webpage):
        self.__current_webpages.append(webpage)

    def __get_previous_page(self):
        self.__current_webpages.pop()
        return self.__current_webpages[-1]

    def main(self):
        while True:
            website = input()
            if website == MenuCommand.EXIT.value:
                break
            elif website == MenuCommand.BACK.value:
                print(self.__get_previous_page())
            elif self.__check_in_cash(website):
                webpage = self.__get_content_of_cash(website)
                self.__add_to_current_webpages(webpage)
                print(webpage)
            elif self.__check_response(website):
                webpage = self.__get_response_text()
                self.__add_to_current_webpages(webpage)
                print(webpage)
            else:
                print("Error: Incorrect URL")

    def __beautify(self, url):
        r = requests.get(url)
        if r.ok:
            print("OK")
        soup = BeautifulSoup(r.text, "html.parser")
        result = ""
        for tag in soup.find_all():
            if tag.name == "a":
                result += Fore.BLUE + tag.text + Fore.RESET
            if tag.name in self.__tags:
                result += tag.text
        return result


if __name__ == '__main__':
    browser = Browser()
    browser.main()
