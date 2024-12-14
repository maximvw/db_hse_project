from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QApplication, QDialog, QLineEdit, QLabel, QDialogButtonBox
from app.handlers import add_user, clear_tables
from app.database import get_db


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Введите параметры")
        
        # Создаем элементы для ввода
        self.label = QLabel("Введите параметры:")
        self.input_line = QLineEdit(self)

        # Кнопки OK и Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Устанавливаем layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_line)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_input(self):
        return self.input_line.text()
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Booking")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.add_user_btn = QPushButton("Добавить пользователя")
        self.add_user_btn.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_btn)

        self.clear_tables_btn = QPushButton("Очистить таблицы")
        self.clear_tables_btn.clicked.connect(self.clear_tables)
        layout.addWidget(self.clear_tables_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_user(self):
        dialog = InputDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    add_user(db, *user_input.split(' '))
                    QMessageBox.information(self, "Успех", "Пользователь добавлен!")
                except TypeError:
                    QMessageBox.information(self, "Неудача", "Неправильные аргументы")

    def clear_tables(self):
        with next(get_db()) as db:
            clear_tables(db)
            QMessageBox.information(self, "Успех", "Таблицы очищены!")
