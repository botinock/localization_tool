import sys, os

from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, QEvent
from PyQt6.QtGui import QAction, QFont, QIcon, QSyntaxHighlighter, QTextCharFormat, QFontMetrics, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit, QTextEdit, QLabel, QPushButton, QMenuBar, QFileDialog
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout
from PyQt6.QtWidgets import QErrorMessage
import qdarktheme

from text_processing import TextProcessing
from spellcheck import SpellChecker

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
        self.ua_line = QLineTextEdit()
        self.plain_text_list.currentRowChanged.connect(self.list_item_activated)
        

        self.is_spellchecker = True

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
        self.ua_line.installEventFilter(self)
        # self.ua_line.returnPressed.connect(self.next_clicked)

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

        self.spch = SpellCheckHighlighter(self.ua_line.document())
        try:
            self.spch_init()
        except:
            self.is_spellchecker = False

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
                self.ua_line.document().toRawText(),
                self.plain_text_list.currentRow()
            )
            item = self.plain_text_list.currentItem()
            item.setText(''.join(self.tp.text[self.plain_text_list.currentRow()]).strip('\n'))

    def file_clicked(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Text files (*READABLE.txt)')
        if file[0] != '':
            self.file_opened(file[0])

    def file_opened(self, file):
        try:
            text = self.tp.read(file)
            print(text)
            self.plain_text_list.clear()
            self.plain_text_list.addItems([''.join(line).strip('\n') for line in text])
        except Exception as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(e.__str__())
            error_dialog.exec()

    def night_mode_clicked(self):
        if self.is_dark:
            QApplication.instance().setStyleSheet(self.light_style_sheet)
            self.is_dark = False
            self.ua_line.set_one_row_style()
            self.spch.misspelledFormat.setUnderlineColor(Qt.GlobalColor.red)
        else:
            stylesheet = qdarktheme.load_stylesheet('dark')
            QApplication.instance().setStyleSheet(stylesheet)
            self.is_dark = True
            self.ua_line.set_one_row_style()
            self.spch.misspelledFormat.setUnderlineColor(Qt.GlobalColor.white)

    def spch_init(self):
        self.spch_thread = QThread()
        self.spch_worker = Worker()
        self.spch_worker.moveToThread(self.spch_thread)
        self.spch_thread.started.connect(self.spch_worker.create_spch)
        self.spch_worker.spch_is_ready_signal.connect(self.spch_is_ready)
        self.spch_worker.spch_is_ready_signal.connect(self.spch_thread.quit)
        self.spch_worker.spch_is_ready_signal.connect(self.spch_worker.deleteLater)
        self.spch_thread.finished.connect(self.spch_thread.deleteLater)
        self.spch_thread.start(QThread.Priority.LowestPriority)

    def spch_is_ready(self, spch: SpellChecker):
        if isinstance(spch, SpellChecker):
            self.spch.setSpeller(spch)
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("SpellChecker is failed to load!")
            error_dialog.exec()
    
    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.KeyPress and obj is self.ua_line:
            if event.key() == Qt.Key.Key_Return and self.ua_line.hasFocus():
                self.next_clicked()
        return super().eventFilter(obj, event)


class Worker(QObject):
    spch_is_ready_signal = pyqtSignal(SpellChecker)

    def create_spch(self):
        try:
            spch = SpellChecker()
            self.spch_is_ready_signal.emit(spch)
        except:
            pass
            # self.spch_is_ready_signal.emit(None)
        


class SpellCheckHighlighter(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)  # Platform and theme dependent
        self.misspelledFormat.setUnderlineColor(Qt.GlobalColor.red)

    def highlightBlock(self, text: str) -> None:
        if not hasattr(self, "speller"):
            return

        for word_object in self.speller.regex.finditer(text):
            if not self.speller.check_word(word_object.group()):
                self.setFormat(
                    word_object.start(),
                    word_object.end() - word_object.start(),
                    self.misspelledFormat,
                )

    def setSpeller(self, speller: SpellChecker):
        self.speller = speller


class QLineTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_one_row_style()

    def set_one_row_style(self):
        pdoc = self.document()
        fm = QFontMetrics(pdoc.defaultFont())
        margins = self.contentsMargins()
        nHeight = fm.lineSpacing() + (pdoc.documentMargin() + self.frameWidth()) * 2 + margins.top() + margins.bottom()
        self.setFixedHeight(int(nHeight))

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            return
        super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    try:
        file = sys.argv[1]
    except:
        file = ''
    window = MainWindow(file)
    window.show()
    app.exec()
