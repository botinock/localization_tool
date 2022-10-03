from spylls.hunspell import Dictionary
import pickle
import re
import time
from serializator import serialize_dict

class SpellChecker:
    def __init__(self) -> None:
        try:
            with open('assets/dictionary', 'rb') as file:
                self.dictionary: Dictionary = pickle.load(file) #Dictionary.from_files('../assets/uk_UA')
        except:
            with open('assets/dictionary', 'rb') as file:
                self.dictionary: Dictionary = Dictionary.from_files('assets/uk_UA')
                serialize_dict()
        self.regex = re.compile(r"([А-ЩЬЮЯҐЄІЇа-щьюяґєії'`’ʼ]+)")

    def check_word(self, word: str) -> bool:
        return self.dictionary.lookup(word)

    def find_suggestions(self, word: str, n: int = None) -> list[str]:
        sugs = []
        if isinstance(n, int):
            i = 0
            for sug in self.dictionary.suggest(word):
                sugs.append(sug)
                if i == n:
                    break
                else:
                    i += 1
        else:
            sugs = [sug for sug in self.dictionary.suggest(word)]
        return sugs

    def check_sentence(self, sentence: str) -> dict[str, bool]:
        word_list = self.regex.findall(sentence)
        check_dict = {word : self.check_word(word) for word in word_list}
        return check_dict

    def suggest_sentence(self, check_dict: dict[str, bool]) -> dict[str, list[str]]:
        sug_dict = {k : self.find_suggestions(k) for k, v in check_dict.items() if not v}
        return sug_dict


if __name__ == "__main__":
    time_1 = time.time()
    sch = SpellChecker()
    time_2 = time.time()
    print(f"Load time = {time_2 - time_1}")
    ua_sentence = "...Український текст тут... полум'я, плам'я"
    time_1 = time.time()
    check_dict = sch.check_sentence(ua_sentence)
    time_2 = time.time()
    print(check_dict)
    print(f"Check time = {time_2 - time_1}")
    time_1 = time.time()
    sug_dict = sch.suggest_sentence(check_dict)
    time_2 = time.time()
    print(sug_dict)
    print(f"Sug time = {time_2 - time_1}")
