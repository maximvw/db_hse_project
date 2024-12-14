from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
)
from app.handlers import (
    create_database, delete_database, get_table_data, clear_table, add_user, search_by_field, update_row, delete_by_field, delete_by_id
)
from app.database import get_db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Booking")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Введите значение для поиска")

        layout = QVBoxLayout()

        # Кнопки управления базой данных
        self.create_db_btn = QPushButton("Создать базу данных")
        self.create_db_btn.clicked.connect(self.create_database)
        layout.addWidget(self.create_db_btn)

        self.delete_db_btn = QPushButton("Удалить базу данных")
        self.delete_db_btn.clicked.connect(self.delete_database)
        layout.addWidget(self.delete_db_btn)

        # Работа с таблицами
        self.load_data_btn = QPushButton("Вывести содержимое таблиц")
        self.load_data_btn.clicked.connect(self.load_data)
        layout.addWidget(self.load_data_btn)

        self.clear_table_btn = QPushButton("Очистить таблицы")
        self.clear_table_btn.clicked.connect(self.clear_all_tables)
        layout.addWidget(self.clear_table_btn)

        # Добавление данных
        self.add_user_btn = QPushButton("Добавить пользователя")
        self.add_user_btn.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_btn)

        # Поиск данных
        self.search_btn = QPushButton("Поиск по текстовому полю")
        self.search_btn.clicked.connect(self.search_data)
        layout.addWidget(self.search_field)
        layout.addWidget(self.search_btn)

        # Обновление данных
        self.update_btn = QPushButton("Обновить запись")
        self.update_btn.clicked.connect(self.update_record)
        layout.addWidget(self.update_btn)

        # Удаление данных
        self.delete_by_field_btn = QPushButton("Удалить по текстовому полю")
        self.delete_by_field_btn.clicked.connect(self.delete_by_field)
        layout.addWidget(self.delete_by_field_btn)

        self.delete_by_id_btn = QPushButton("Удалить запись по ID")
        self.delete_by_id_btn.clicked.connect(self.delete_by_id)
        layout.addWidget(self.delete_by_id_btn)

        # Вывод таблицы
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Обработчики кнопок
    def create_database(self):
        try:
            create_database()
            QMessageBox.information(self, "Успех", "База данных успешно создана.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_database(self):
        try:
            delete_database()
            QMessageBox.information(self, "Успех", "База данных успешно удалена.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def load_data(self):
        with next(get_db()) as db:
            try:
                data = get_table_data(db, "users")  # Пример для таблицы "users"
                self.display_table(data, ["ID", "Имя", "Телефон", "Роль"])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def clear_all_tables(self):
        with next(get_db()) as db:
            try:
                clear_table(db, "users")  # Очистка таблицы "users"
                QMessageBox.information(self, "Успех", "Таблицы успешно очищены.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def add_user(self):
        with next(get_db()) as db:
            try:
                add_user(db, "Иван Иванов", "89001234567", "клиент")
                QMessageBox.information(self, "Успех", "Пользователь успешно добавлен.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def search_data(self):
        with next(get_db()) as db:
            try:
                value = self.search_field.text()
                data = search_by_field(db, "users", "name", value)
                self.display_table(data, ["ID", "Имя", "Телефон", "Роль"])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def update_record(self):
        with next(get_db()) as db:
            try:
                update_row(db, "users", 1, {"name": "Пётр Петров"})  # Пример обновления
                QMessageBox.information(self, "Успех", "Запись успешно обновлена.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def delete_by_field(self):
        with next(get_db()) as db:
            try:
                delete_by_field(db, "users", "name", "Иван Иванов")
                QMessageBox.information(self, "Успех", "Запись успешно удалена.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def delete_by_id(self):
        with next(get_db()) as db:
            try:
                delete_by_id(db, "users", 1)  # Пример удаления по ID
                QMessageBox.information(self, "Успех", "Запись успешно удалена.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def display_table(self, data, headers):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
