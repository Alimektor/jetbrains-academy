import requests
import bs4
import argparse
import sys
from requests.exceptions import ConnectionError


class Translator:
    def __init__(self):
        self.languages = {
            "1": "Arabic",
            "2": "German",
            "3": "English",
            "4": "Spanish",
            "5": "French",
            "6": "Hebrew",
            "7": "Japanese",
            "8": "Dutch",
            "9": "Polish",
            "10": "Portuguese",
            "11": "Romanian",
            "12": "Russian",
            "13": "Turkish"
        }
        self.url = "https://context.reverso.net/translation"
        self.session = requests.Session()
        self.language_from = None
        self.language_to = None
        self.word = None
        self.soup = None
        self.args = None

    def main(self):
        try:
            print(self.args)
            if len(sys.argv) > 1:
                self.cmd()
            else:
                self.cui()
        except ValueError as ve:
            print(ve)
        except AttributeError as ae:
            print(f"Sorry, unable to find {self.word}")
        except ConnectionError:
            print("Something wrong with your internet connection")

    def cmd(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("langfrom", type=str)
        parser.add_argument("langto", type=str)
        parser.add_argument("word", type=str)
        self.args = parser.parse_args()
        self.language_from = self.args.langfrom
        self.word = self.args.word
        if self.args.langto == "all":
            self.multitranslate()
            return
        self.check_languages()
        self.language_to = self.args.langto
        self.check_status()
        self.print_translations()

    def cui(self):
        print("Hello, you're welcome to the translator. Translator supports:")
        for language in self.languages:
            print(f"{language}. {self.languages[language]}")
        print("Type the number of your language:")
        your_language_choice = input()
        self.language_from = self.languages[your_language_choice]
        print("Type the number of a language you want to translate to or '0' to translate to all languages:")
        choice = input()
        print('Type the word you want to translate:')
        self.word = input()
        if choice == "0":
            self.multitranslate()
            return
        self.language_to = self.languages[choice]
        self.check_status()
        self.print_translations()

    def print_translations(self):
        print(f"\n{self.language_to} Translations:")
        for translation in self.get_translations()[:5]:
            print(translation)
        print(f"\n{self.language_to} Examples:")
        for example in self.get_context()[:10]:
            print(example)

    def check_status(self):
        address = f"{self.url}/{self.language_from.lower()}-{self.language_to.lower()}/{self.word}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        self.response = self.session.get(address, headers=headers)
        if self.response.ok:
            self.soup = bs4.BeautifulSoup(self.response.text, "html.parser")
            return "200 OK"
        return "Something bad happened."

    def get_translations(self):
        translations = []
        for translation in self.soup.find_all(class_="dict"):
            translations.append(self.get_clean_text(translation.text))
        return translations

    def get_context(self):
        source = []
        target = []
        for src in self.soup.find_all(class_="src"):
            source.append(self.get_clean_text(src.text))
        for trg in self.soup.find_all(class_="trg"):
            target.append(self.get_clean_text(trg.text))
        contexts = []
        for src, trg in zip(source, target):
            contexts.append(src)
            contexts.append(trg)

        return contexts

    def get_clean_text(self, text):
        return text.replace("\n", "").replace("  ", " ").strip()

    def multitranslate(self):
        filename = self.word + ".txt"
        with open(filename, "w+") as output:
            for language_id in self.languages:
                self.language_to = self.languages[language_id]
                self.check_status()
                print(f"{self.language_to} Translations:", file=output)
                print(f"{self.language_to} Translations:")
                for translation in self.get_translations()[:1]:
                    print(translation, file=output)
                    print(translation)
                print(f"\n{self.language_to} Examples:", file=output)
                print(f"\n{self.language_to} Examples:")
                for example in self.get_context()[:2]:
                    print(example, file=output)
                    print(example)
                print("\n", file=output)
                print("\n")

    def check_languages(self):
        languages = [s.lower() for s in self.languages.values()]
        if self.args.langfrom not in languages:
            raise ValueError(f"Sorry, the program doesn't support {self.args.langfrom}")
        if self.args.langto not in languages:
            raise ValueError(f"Sorry, the program doesn't support {self.args.langto}")


if __name__ == '__main__':
    translator = Translator()
    translator.main()
