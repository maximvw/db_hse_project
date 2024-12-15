from datetime import date, datetime

from PyQt6.QtWidgets import QDialog, QLabel, \
    QDialogButtonBox
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
)

from app.database import get_db
from app.handlers import add_user, add_schedule, add_service, add_booking, clear_tables, clear_user, clear_service, \
    clear_booking, clear_schedule, get_table_data


class InputDialog(QDialog):
    def __init__(self, strings):
        super().__init__()

        self.setWindowTitle("Введите параметры")
        self.setGeometry(100, 500, 500, 100)
        # Создаем элементы для ввода
        self.label = QLabel("Введите параметры:")
        # self.labels = []
        self.input_lines = []
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Booking")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()
        self.layout = QVBoxLayout()

        self.button_stack = []

        self.button_functions = {
            "Добавить": self.replace_add_button,
            "Очистить таблицы": self.replace_clear_table_button,
            "Вывести содержимое таблиц": self.load_data
        }

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.replace_add_button)
        self.layout.addWidget(self.add_btn)

        # Работа с таблицами
        self.load_data_btn = QPushButton("Вывести содержимое таблиц")
        self.load_data_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_btn)

        self.clear_tables_btn = QPushButton("Очистить таблицы")
        self.clear_tables_btn.clicked.connect(self.replace_clear_table_button)
        self.layout.addWidget(self.clear_tables_btn)

        # self.show_users_btn = QPushButton("Вывести пользователей")
        # self.show_users_btn.clicked.connect(self.show_users)
        # self.layout.addWidget(self.show_users_btn)
        
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
            }

            QLabel {
                color: blue;
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

            QPushButton:hover {
                background-color: #0056a1;
            }
        """)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)  # Сначала отключена
        # Добавляем кнопку "Назад" в layout
        self.layout.addWidget(self.back_button)

    def replace_add_button(self):
        current_buttons = {
            self.layout.itemAt(i).widget().text(): self.button_functions[self.layout.itemAt(i).widget().text()]
            for i in range(self.layout.count())
            if self.layout.itemAt(i).widget() != self.back_button}
        self.button_stack.append(current_buttons)

        self.add_btn.deleteLater()
        self.clear_tables_btn.deleteLater()
        self.load_data_btn.deleteLater()

        self.add_user_btn = QPushButton("Добавить пользователя")
        self.add_user_btn.clicked.connect(self.add_user)
        self.layout.addWidget(self.add_user_btn)

        self.add_service_btn = QPushButton("Добавить услугу")
        self.add_service_btn.clicked.connect(self.add_service)
        self.layout.addWidget(self.add_service_btn)

        self.add_schedule_btn = QPushButton("Добавить расписание")
        self.add_schedule_btn.clicked.connect(self.add_schedule)
        self.layout.addWidget(self.add_schedule_btn)

        self.add_booking_btn = QPushButton("Добавить бронирование")
        self.add_booking_btn.clicked.connect(self.add_booking)
        self.layout.addWidget(self.add_booking_btn)

        self.back_button.setEnabled(True)

    def replace_clear_table_button(self):
        current_buttons = {
            self.layout.itemAt(i).widget().text(): self.button_functions[self.layout.itemAt(i).widget().text()]
            for i in range(self.layout.count())
            if self.layout.itemAt(i).widget() != self.back_button}
        self.button_stack.append(current_buttons)

        self.add_btn.deleteLater()
        self.clear_tables_btn.deleteLater()
        self.load_data_btn.deleteLater()

        self.clear_all_btn = QPushButton("Очистить все таблицы")
        self.clear_all_btn.clicked.connect(self.clear_tables)
        self.layout.addWidget(self.clear_all_btn)

        self.clear_user_btn = QPushButton("Очистить таблицу пользователей")
        self.clear_user_btn.clicked.connect(self.clear_user)
        self.layout.addWidget(self.clear_user_btn)

        self.clear_service_btn = QPushButton("Очистить таблицу услуг")
        self.clear_service_btn.clicked.connect(self.clear_service)
        self.layout.addWidget(self.clear_service_btn)

        self.clear_schedule_btn = QPushButton("Очистить таблицу расписания")
        self.clear_schedule_btn.clicked.connect(self.clear_schedule)
        self.layout.addWidget(self.clear_schedule_btn)

        self.clear_booking_btn = QPushButton("Очистить таблицу бронирования")
        self.clear_booking_btn.clicked.connect(self.clear_booking)
        self.layout.addWidget(self.clear_booking_btn)

        self.back_button.setEnabled(True)

    def go_back(self):
        if self.button_stack:
            # Удаляем текущие кнопки (кроме кнопки "Назад")
            for i in range(self.layout.count()):
                widget = self.layout.itemAt(i).widget()
                if widget and widget != self.back_button:
                    widget.deleteLater()  # Уничтожаем текущие кнопки

            # Восстанавливаем состояние из стека
            previous_buttons = self.button_stack.pop()
            for button_text, action in previous_buttons.items():
                button = QPushButton(button_text)
                button.clicked.connect(action)
                self.layout.addWidget(button)
                if button_text == "Добавить":
                    self.add_btn = button
                if button_text == "Очистить таблицы":
                    self.clear_tables_btn = button
                if button_text == "Вывести содержимое таблиц":
                    self.load_data_btn = button

            # Если стек пуст, отключаем кнопку "Назад", иначе оставляем включенной
            if not self.button_stack:
                self.back_button.setEnabled(False)

    def add_user(self):
        dialog = InputDialog(("Введите имя", "Введите телефон", "Введите роль"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    add_user(db, *user_input)
                    QMessageBox.information(self, "Успех", "Пользователь добавлен!")
                except TypeError:
                    QMessageBox.information(self, "Неудача", "Неправильные аргументы")

    def add_service(self):
        dialog = InputDialog(("Введите название", "Введите цену за час"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    s_name, s_price = user_input[0], int(user_input[1])
                    add_service(db, s_name, s_price)
                    QMessageBox.information(self, "Успех", "Услуга добавлена!")
                except TypeError:
                    QMessageBox.information(self, "Неудача", "Неправильные аргументы")

    def add_schedule(self):
        dialog = InputDialog(
            ("Введите id тренера", "Введите id услуги", "Введите дату", "Введите время начала", "Введите время конца"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    parts = user_input
                    trainer_id = int(parts[0])
                    service_id = int(parts[1])
                    date_str = parts[2].split(".")  # Преобразуем дату в формате "Y.M.D"
                    schedule_date = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
                    start_time_str = parts[3]
                    end_time_str = parts[4]
                    start_time = datetime.strptime(start_time_str,
                                                   "%H:%M").time()  # Преобразуем строку в формат времени
                    end_time = datetime.strptime(end_time_str, "%H:%M").time()
                    add_schedule(db, trainer_id, service_id, schedule_date, start_time, end_time)
                    QMessageBox.information(self, "Успех", "Расписание добавлено!")
                except Exception as e:
                    QMessageBox.information(self, "Неудача", f"Неправильные аргументы {e}")

    def add_booking(self):
        dialog = InputDialog(("Введите id клиента", "Введите id расписания"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    client_id, schedule_id = map(int, user_input)
                    add_booking(db, client_id, schedule_id)
                    QMessageBox.information(self, "Успех", "Бронирование добавлено!")
                except TypeError:
                    QMessageBox.information(self, "Неудача", "Неправильные аргументы")

    def clear_tables(self):
        with next(get_db()) as db:
            clear_tables(db)
            QMessageBox.information(self, "Успех", "Таблицы очищены!")

    def clear_user(self):
        with next(get_db()) as db:
            clear_user(db)
            QMessageBox.information(self, "Успех", "Таблица пользователей очищена!")

    def clear_service(self):
        with next(get_db()) as db:
            clear_service(db)
            QMessageBox.information(self, "Успех", "Таблица услуг очищена!")

    def clear_schedule(self):
        with next(get_db()) as db:
            clear_schedule(db)
            QMessageBox.information(self, "Успех", "Таблица расписания очищена!")

    def clear_booking(self):
        with next(get_db()) as db:
            clear_booking(db)
            QMessageBox.information(self, "Успех", "Таблица бронирования очищена!")

    def load_data(self):
        with next(get_db()) as db:
            try:
                data = get_table_data(db, "users")  # Пример для таблицы "users"
                self.display_table(data, ["id", "name", "phone", "role"])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def display_table(self, data, headers):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                print(row_idx, col_idx, value)
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def load_data(self):
        with next(get_db()) as db:
            try:
                data = get_table_data(db, "users")  # Пример для таблицы "users"
                self.display_table(data, ["id", "name", "phone", "role"])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def display_table(self, data, headers):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                print(row_idx, col_idx, value)
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # def show_users(self):
    #     with next(get_db()) as db:
    #         for row in show_users(db):
    #             QMessageBox.information(self, "Успех", str(row))