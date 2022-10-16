import sys
import os
import re

class TextProcessing:
    def __init__(self) -> None:
        self.jp_list: list[str] = []
        self.en_list: list[str] = []
        self.ua_list: list[str] = []
        self.regex = re.compile(r"\"\s?(.*)\"")
        self.file = ''

        self.display_jp = True
        self.display_en = True
    
    def read(self, file: str = ''):
        text_list = []
        if os.path.exists(file) and file != '':
            with open(file, 'r', encoding='UTF-8') as f:
                    text_list = f.readlines()
                    file_correct = False
                    for line in text_list:
                        if line[1:3] == 'EN':
                            file_correct = True
                            break
                    if file_correct == False:   
                        raise Exception("Wrong file format!")
                    self.file = file
        else:
            self.file = ''
        self.jp_list = []
        self.en_list = []
        self.ua_list = []
        for line in text_list:
            match line[1:3]:
                case "JP":
                    self.jp_list.append(line)
                case "EN":
                    self.en_list.append(line)
                case "UA":
                    self.ua_list.append(line)
        return self.make_text()

    def save(self):
        if self.file != '':
            with open(self.file, 'w', encoding='UTF-8') as f:
                f.write(''.join([''.join(line) for line in self.text_save]))

    def make_text(self):
        lang_list = []
        if self.display_jp:
            lang_list.append(self.jp_list)
        if self.display_en:
            lang_list.append(self.en_list)
        lang_list.append(self.ua_list)
        self.text = list(zip(*lang_list))
        self.text_save = list(zip(self.jp_list, self.en_list, self.ua_list))
        self.save()
        return self.text

    def update_ua(self, line: str, idx: int):
        self.ua_list[idx] = self.ua_list[idx].replace(
            self.parse_string(self.ua_list[idx]), line)
        return self.make_text()

    def parse_string(self, line: str) -> str:
        return self.regex.search(line).group(1).strip('\n')
        

if __name__ == '__main__':
    try:
        file = sys.argv[1]
        tp = TextProcessing()
        print(tp.read(file))
        print(tp.update_ua("ЦЕ ПЕРЕКЛАД ЦЕ ПЕРЕКЛАД ЦЕ ПЕРЕКЛАД", -1))
    except Exception as e:
        print(e)

