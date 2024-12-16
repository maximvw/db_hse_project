from datetime import date, datetime

from PyQt6.QtWidgets import QDialog, QLabel, \
    QDialogButtonBox
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
)

from app.database import get_db
from app.handlers import add_user, add_schedule, add_service, add_booking, clear_tables, clear_user, clear_service, \
    clear_booking, clear_schedule, get_table_data, search_by_field, update_row, delete_by_field

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
            row_data = [col for col in row_data[0][1:-1].split(',')]
            for col_idx, value in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(value))
    

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

        #self.table_widget = QTableWidget()
        self.search_field = QLineEdit()
        self.layout = QVBoxLayout()

        self.button_stack = []
        self.tables = []

        self.button_functions = {
            "Добавить": lambda x: self.ultimative_replace_button({"Добавить пользователя": self.add_user, "Добавить услугу": self.add_service, \
                "Добавить расписание": self.add_schedule, "Добавить бронирование": self.add_booking}),
            "Очистить таблицы": lambda x: self.ultimative_replace_button({
                "Очистить все таблицы": self.clear_tables,
                "Очистить таблицу пользователей": self.clear_user,
                "Очистить таблицу услуг": self.clear_service,
                "Очистить таблицу расписания": self.clear_schedule,
                "Очистить таблицу бронирования": self.clear_booking
                }),
            "Вывести содержимое таблиц": lambda x: self.ultimative_replace_button({
                "Вывести таблицу пользователей": lambda x: self.load_data("users"),
                "Вывести таблицу услуг": lambda x: self.load_data("services"),
                "Вывести таблицу расписания": lambda x: self.load_data("schedule"),
                "Вывести таблицу бронирования": lambda x: self.load_data("bookings")
                }),
            "Поиск по текстовому полю": self.search_data,
            "Обновить запись": self.update_record,
            "Удалить по текстовому полю": self.delete_by_field
        }

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(lambda x: self.ultimative_replace_button({"Добавить пользователя": self.add_user, "Добавить услугу": self.add_service, \
                "Добавить расписание": self.add_schedule, "Добавить бронирование": self.add_booking}))
        self.layout.addWidget(self.add_btn)

        self.clear_tables_btn = QPushButton("Очистить таблицы")
        self.clear_tables_btn.clicked.connect(lambda x: self.ultimative_replace_button({
            "Очистить все таблицы": self.clear_tables,
            "Очистить таблицу пользователей": self.clear_user,
            "Очистить таблицу услуг": self.clear_service,
            "Очистить таблицу расписания": self.clear_schedule,
            "Очистить таблицу бронирования": self.clear_booking
            }))
        self.layout.addWidget(self.clear_tables_btn)

        # Поиск данных
        self.search_btn = QPushButton("Поиск по текстовому полю")
        self.search_btn.clicked.connect(self.search_data)
        self.layout.addWidget(self.search_btn)

        # Обновление данных
        self.update_btn = QPushButton("Обновить запись")
        self.update_btn.clicked.connect(self.update_record)
        self.layout.addWidget(self.update_btn)

        # Удаление данных
        self.delete_by_field_btn = QPushButton("Удалить по текстовому полю")
        self.delete_by_field_btn.clicked.connect(self.delete_by_field)
        self.layout.addWidget(self.delete_by_field_btn)

        # Работа с таблицами
        self.load_data_btn = QPushButton("Вывести содержимое таблиц")
        self.load_data_btn.clicked.connect(lambda x: self.ultimative_replace_button({
                "Вывести таблицу пользователей": lambda x: self.load_data("users"),
                "Вывести таблицу услуг": lambda x: self.load_data("services"),
                "Вывести таблицу расписания": lambda x: self.load_data("schedule"),
                "Вывести таблицу бронирования": lambda x: self.load_data("bookings")
                }))
        self.layout.addWidget(self.load_data_btn)

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

    def ultimative_replace_button(self, buttons):
        current_buttons = {
            self.layout.itemAt(i).widget().text(): self.button_functions[self.layout.itemAt(i).widget().text()]
            for i in range(self.layout.count())
            if self.layout.itemAt(i).widget() != self.back_button}
        self.button_stack.append(current_buttons)

        self.add_btn.deleteLater()
        self.clear_tables_btn.deleteLater()
        self.load_data_btn.deleteLater()
        self.search_btn.deleteLater()
        self.update_btn.deleteLater()
        self.delete_by_field_btn.deleteLater()
        
        for button_name in buttons:
            current_btn = QPushButton(button_name)
            current_btn.clicked.connect(buttons[button_name])
            self.layout.addWidget(current_btn)

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
                    self.table_widget = QTableWidget()
                if button_text == "Поиск по текстовому полю":
                    self.search_btn = button
                if button_text == "Обновить запись":
                    self.update_btn = button
                if button_text == "Удалить по текстовому полю":
                    self.delete_by_field_btn = button
                

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

    def load_data(self, table_name):
        with next(get_db()) as db:
            try:
                data, header = get_table_data(db, table_name)
                self.tables.append(TableWindow(data, header))
                self.tables[-1].show()
                # table_winow.display_table(data, header)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))


    def display_table(self, data, headers):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            row_data = [col for col in row_data[0][1:-1].split(',')]
            for col_idx, value in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def search_data(self):
        dialog = InputDialog(("Введите имя",))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()[0]
            with next(get_db()) as db:
                try:
                    data, header = search_by_field(db, "users", "name", user_input)
                    self.display_table(data, header)
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

    # def show_users(self):
    #     with next(get_db()) as db:
    #         for row in show_users(db):
    #             QMessageBox.information(self, "Успех", str(row))
