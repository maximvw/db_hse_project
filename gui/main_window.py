from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from app.handlers import add_user, clear_tables
from app.database import get_db


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
        with next(get_db()) as db:
            add_user(db, "Иван Иванов", "89001234567", "клиент")
            QMessageBox.information(self, "Успех", "Пользователь добавлен!")

    def clear_tables(self):
        with next(get_db()) as db:
            clear_tables(db)
            QMessageBox.information(self, "Успех", "Таблицы очищены!")
