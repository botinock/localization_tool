import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit, QLabel, QPushButton, QMenuBar
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from text_processing import TextProcessing

class MainWindow(QMainWindow):
    def __init__(self, file):
        super().__init__()
        self.setWindowTitle("Localization Tool")
        menu = QMenuBar()
        menu.addAction("File")
        menu.addAction("Font")
        menu.addAction("Night Mode")
        self.setMenuBar(menu)

        layout = QVBoxLayout()

        self.plain_text_list = QListWidget()

        self.tp = TextProcessing()
        text = self.tp.read(file)
        self.plain_text_list.addItems([''.join(line).strip('\n') for line in text])
        self.plain_text_list.currentRowChanged.connect(self.list_item_activated)

        self.jp_line = QLineEdit("……もう怒らないで聞いてくれますよね？」")
        self.en_line = QLineEdit("...You'll listen without getting angry this time, right?")
        self.ua_line = QLineEdit("...Тепер послухай будь ласка спокійно, добре?")

        jp_flag = QLabel('🇯🇵')
        en_flag = QLabel('🇬🇧')
        ua_flag = QLabel('🇺🇦')

        jp_layout = QHBoxLayout()
        en_layout = QHBoxLayout()
        ua_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Back")
        self.save_button = QPushButton("Save")
        self.next_button = QPushButton("Next")
        
        self.back_button.clicked.connect(self.back_clicked)
        self.save_button.clicked.connect(self.save)
        self.next_button.clicked.connect(self.next_clicked)
        self.ua_line.returnPressed.connect(self.next_clicked)

        jp_layout.addWidget(jp_flag)
        jp_layout.addWidget(self.jp_line)
        jp_layout.addWidget(self.back_button)

        en_layout.addWidget(en_flag)
        en_layout.addWidget(self.en_line)
        en_layout.addWidget(self.save_button)

        ua_layout.addWidget(ua_flag)
        ua_layout.addWidget(self.ua_line)
        ua_layout.addWidget(self.next_button)

        self.jp_line.setReadOnly(True)
        self.en_line.setReadOnly(True)

        layout.addWidget(self.plain_text_list)
        layout.addLayout(jp_layout)
        layout.addLayout(en_layout)
        layout.addLayout(ua_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def list_item_activated(self, row_idx: int):
        self.jp_line.setText(self.tp.parse_string(self.tp.jp_list[row_idx]))
        self.en_line.setText(self.tp.parse_string(self.tp.en_list[row_idx]))
        self.ua_line.setText(self.tp.parse_string(self.tp.ua_list[row_idx]))

    def next_clicked(self):
        self.save()
        if self.plain_text_list.currentRow() == self.plain_text_list.count() - 1:    
            self.plain_text_list.setCurrentRow(0)
        else:
            self.plain_text_list.setCurrentRow(self.plain_text_list.currentRow() + 1)

    def back_clicked(self):
        self.save()
        if self.plain_text_list.currentRow() == 0:    
            self.plain_text_list.setCurrentRow(self.plain_text_list.count() - 1)
        else:
            self.plain_text_list.setCurrentRow(self.plain_text_list.currentRow() - 1)

    def save(self):
        self.tp.update_ua(
            self.ua_line.text(),
            self.plain_text_list.currentRow()
        )
        item = self.plain_text_list.currentItem()
        item.setText(''.join(self.tp.text[self.plain_text_list.currentRow()]).strip('\n'))


if __name__ == '__main__':
    app = QApplication([])
    try:
        file = sys.argv[1]
    except:
        file = ''
    window = MainWindow(file)
    window.show()
    app.exec()
