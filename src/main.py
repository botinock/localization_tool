import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit, QPlainTextEdit, QLabel
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Localization Tool")

        layout = QVBoxLayout()

        self.plain_text = QPlainTextEdit(f'''[JP:1]"　食後はテレビを見る気力もなく、…部屋で布団に潜りながら…陰鬱な考えに頭をめぐらせていた…。"
[EN:1]"After dinner, without the energy to watch TV... I climbed into the futon in my bedroom... and let my head be overtaken by gloomy thoughts..."
[UA:1]"After dinner, without the energy to watch TV... I climbed into the futon in my bedroom... and let my head be overtaken by gloomy thoughts..."
[JP:2]"　梨花ちゃんに洗いざらいの全てを話した。"
[EN:2]"I told Rika-chan anything and everything."
[UA:2]"I told Rika-chan anything and everything."

[JP]"詩音"
[EN]"Shion"
[UA]"Shion"
[JP:3]"「では……昨日の続きを話します。"
[EN:3]"\"Then... let's continue from where we left off."
[UA:3]"\"Then... let's continue from where we left off."
[JP:4]"……もう怒らないで聞いてくれますよね？」"
[EN:4]" ...You'll listen without getting angry this time, right?\""
[UA:4]" ...You'll listen without getting angry this time, right?\""''')
        self.jp_line = QLineEdit("……もう怒らないで聞いてくれますよね？」")
        self.en_line = QLineEdit("...You'll listen without getting angry this time, right?")
        self.ua_line = QLineEdit("...Тепер послухай будь ласка спокійно, добре?")

        jp_flag = QLabel('🇯🇵')
        en_flag = QLabel('🇬🇧')
        ua_flag = QLabel('🇺🇦')

        jp_layout = QHBoxLayout()
        en_layout = QHBoxLayout()
        ua_layout = QHBoxLayout()

        jp_layout.addWidget(jp_flag)
        jp_layout.addWidget(self.jp_line)
        en_layout.addWidget(en_flag)
        en_layout.addWidget(self.en_line)
        ua_layout.addWidget(ua_flag)
        ua_layout.addWidget(self.ua_line)

        self.plain_text.setReadOnly(True)
        self.jp_line.setReadOnly(True)
        self.en_line.setReadOnly(True)

        # layout.addStretch()
        layout.addWidget(self.plain_text)
        layout.addLayout(jp_layout)
        layout.addLayout(en_layout)
        layout.addLayout(ua_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()