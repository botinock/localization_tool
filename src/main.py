import sys, os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit, QLabel, QPushButton, QMenuBar, QFileDialog
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout
from PyQt6.QtWidgets import QErrorMessage
import qdarktheme

from text_processing import TextProcessing

class MainWindow(QMainWindow):
    def __init__(self, file):
        super().__init__()
        self.setWindowTitle("Localization Tool")
        self.setAcceptDrops(True)

        menu = QMenuBar()
        file_button = menu.addAction("File")
        menu.addAction("Font")
        night_button = menu.addAction("Night Mode")
        self.setMenuBar(menu)

        file_button.triggered.connect(self.file_clicked)
        self.light_style_sheet = QApplication.instance().styleSheet()
        self.is_dark = False
        night_button.triggered.connect(self.night_mode_clicked)

        v_layout = QVBoxLayout()
        grid_layout = QGridLayout()


        self.plain_text_list = QListWidget()
        self.tp = TextProcessing()
        if file != '':
            self.file_opened(file)

        self.jp_line = QLineEdit()
        self.en_line = QLineEdit()
        self.ua_line = QLineEdit()

        self.jp_line.setPlaceholderText("日本語のテキストはここにある")
        self.en_line.setPlaceholderText("English text is here")
        self.ua_line.setPlaceholderText("Український текст тут")

        jp_flag = QLabel('🇯🇵')
        en_flag = QLabel('🇬🇧')
        ua_flag = QLabel('🇺🇦')
        
        self.back_button = QPushButton("Back")
        self.save_button = QPushButton("Save")
        self.next_button = QPushButton("Next")
        
        self.back_button.clicked.connect(self.back_clicked)
        self.save_button.clicked.connect(self.save)
        self.next_button.clicked.connect(self.next_clicked)
        self.ua_line.returnPressed.connect(self.next_clicked)

        grid_layout.addWidget(jp_flag, 0, 0)
        grid_layout.addWidget(self.jp_line, 0, 1)
        grid_layout.addWidget(self.back_button, 0, 2)

        grid_layout.addWidget(en_flag, 1, 0)
        grid_layout.addWidget(self.en_line, 1, 1)
        grid_layout.addWidget(self.save_button, 1, 2)

        grid_layout.addWidget(ua_flag, 2, 0)
        grid_layout.addWidget(self.ua_line, 2, 1)
        grid_layout.addWidget(self.next_button, 2, 2)

        self.jp_line.setReadOnly(True)
        self.en_line.setReadOnly(True)

        v_layout.addWidget(self.plain_text_list)
        v_layout.addLayout(grid_layout)

        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

    def dragEnterEvent(self, e):
        if e.mimeData().text()[:4] == 'file' and e.mimeData().text()[-4:] == '.txt':
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        file = e.mimeData().text()[8:]        
        self.file_opened(file)

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
        if self.tp.file != '':
            self.tp.update_ua(
                self.ua_line.text(),
                self.plain_text_list.currentRow()
            )
            item = self.plain_text_list.currentItem()
            item.setText(''.join(self.tp.text[self.plain_text_list.currentRow()]).strip('\n'))

    def file_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Text files (*READABLE.txt)')
        self.file_opened(file[0])

    def file_opened(self, file):
        try:
            text = self.tp.read(file)
            self.plain_text_list.addItems([''.join(line).strip('\n') for line in text])
            self.plain_text_list.currentRowChanged.connect(self.list_item_activated)
        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(e.__str__())
            error_dialog.exec()

    def night_mode_clicked(self):
        if self.is_dark:
            QApplication.instance().setStyleSheet(self.light_style_sheet)
            self.is_dark = False
        else:
            stylesheet = qdarktheme.load_stylesheet('dark')
            QApplication.instance().setStyleSheet(stylesheet)
            self.is_dark = True



if __name__ == '__main__':
    app = QApplication([])
    try:
        file = sys.argv[1]
    except:
        file = ''
    window = MainWindow(file)
    window.show()
    app.exec()
