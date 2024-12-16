from PyQt6.QtWidgets import QDialog, QLabel, \
    QDialogButtonBox
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit
)

class TableWindow(QMainWindow):
    def __init__(self, data, headers):
        super().__init__()
        self.setWindowTitle("Таблица данных")
        self.setGeometry(100, 100, 800, 600)  # Установка начального размера окна

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)
        self.display_table(data, headers)

    def display_table(self, data, headers):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            # row_data = [col for col in row_data[0][1:-1].split(',')]
            for col_idx, value in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


class InputDialog(QDialog):
    def __init__(self, strings):
        super().__init__()

        self.setWindowTitle("Введите параметры")
        self.setGeometry(100, 500, 500, 100)
        # Создаем элементы для ввода
        self.label = QLabel("Введите параметры:")
        # self.labels = []
        self.input_lines = []
        if isinstance(strings, str):
            strings = [strings]
        for string in strings:
            # self.labels.append(QLabel(''))
            input_line = QLineEdit(self)
            input_line.setPlaceholderText(string)
            self.input_lines.append(input_line)

        # Кнопки OK и Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Устанавливаем self.layout
        self.layout = QVBoxLayout()
        # for label in self.labels:
        #     self.layout.addWidget(label)
        for input_line in self.input_lines:
            self.layout.addWidget(input_line)
            self.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e;
            }

            QLabel {
                color: white;
                font-size: 18px;
                margin: 10px;
            }

            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }

            QLineEdit {
                color: black;
            }
            
            QPushButton:hover {
                background-color: #0056a1;
            }
        """)

        self.layout.addWidget(button_box)
        self.setLayout(self.layout)

    def get_input(self):
        return [input_line.text() for input_line in self.input_lines]
