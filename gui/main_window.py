from datetime import date, datetime

from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
)

from app.database import get_db
from app.handlers import add_user, add_schedule, add_service, add_booking, clear_tables, clear_user, clear_service, \
    clear_booking, clear_schedule, get_table_data, search_by_field, update_row, delete_by_field, delete_row
from gui.forms import TableWindow, InputDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Booking")
        self.setGeometry(100, 100, 800, 600)

        self.search_field = QLineEdit()
        self.layout = QVBoxLayout()

        self.button_stack = []
        self.tables = []
        self.current_buttons = []
        self.button_functions = {
            "Добавить": lambda x: self.ultimative_replace_button(
                {"Добавить пользователя": self.add_user, "Добавить услугу": self.add_service, \
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
            "Поиск услуги по названию": self.search_data,
            "Обновить запись": lambda x: self.ultimative_replace_button({
                "Обновить данные о пользователе": lambda x: self.update_record("users", ("Введите имя пользователя", "Введите телефон поьзователя", "Введите роль пользователя")),
                "Обновить данные об услуге": lambda x: self.update_record("services", ("Введите имя услуги", "Введите цену в час")),
                "Обновить данные о расписании": lambda x: self.update_record("schedule", ("Введите id тренера", "Введите id услуги", "Введите дату", "Введите время начала", "Введите время окончания")),
                "Обновить данные о бронировании": lambda x: self.update_record("bookings", ("Введите id клиента", "Введите id расписания"))}),
            "Удалить услугу": self.delete_by_field,
            "Удалить запись": lambda x: self.ultimative_replace_button({
                "Удалить пользователя(-ей)": lambda x: self.delete_row("users", ("Введите id пользователя", "Введите имя пользователя", "Введите телефон поьзователя", "Введите роль пользователя")),
                "Удалить услугу(-и)": lambda x: self.delete_row("services", ("Введите id услуги", "Введите имя услуги", "Введите цену в час")),
                "Удалить расписание(-я)": lambda x: self.delete_row("schedule", ("Введите id расписания", "Введите id тренера", "Введите id услуги", "Введите дату", "Введите время начала", "Введите время окончания")),
                "Удалить бронирование(-я)": lambda x: self.delete_row("bookings", ("Введите id бронирования", "Введите id клиента", "Введите id расписания"))})
        }

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(lambda x: self.ultimative_replace_button(
            {"Добавить пользователя": self.add_user, "Добавить услугу": self.add_service, \
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
        self.search_btn = QPushButton("Поиск услуги по названию")
        self.search_btn.clicked.connect(self.search_data)
        self.layout.addWidget(self.search_btn)

        # Обновление данных
        self.update_btn = QPushButton("Обновить запись")
        self.update_btn.clicked.connect(lambda x: self.ultimative_replace_button({
                "Обновить данные о пользователе": lambda x: self.update_record("users", ("Введите имя пользователя", "Введите телефон поьзователя", "Введите роль пользователя")),
                "Обновить данные об услуге": lambda x: self.update_record("services", ("Введите имя услуги", "Введите цену в час")),
                "Обновить данные о расписании": lambda x: self.update_record("schedule", ("Введите id тренера", "Введите id услуги", "Введите дату", "Введите время начала", "Введите время окончания")),
                "Обновить данные о бронировании": lambda x: self.update_record("bookings", ("Введите id клиента", "Введите id расписания"))}))
        self.layout.addWidget(self.update_btn)

        # Удаление данных
        self.delete_by_field_btn = QPushButton("Удалить услугу")
        self.delete_by_field_btn.clicked.connect(self.delete_by_field)
        self.layout.addWidget(self.delete_by_field_btn)

        self.delete_row_btn = QPushButton("Удалить запись")
        self.delete_row_btn.clicked.connect(lambda x: self.ultimative_replace_button({
                "Удалить пользователя(-ей)": lambda x: self.delete_row("users", ("Введите id пользователя", "Введите имя пользователя", "Введите телефон поьзователя", "Введите роль пользователя")),
                "Удалить услугу(-и)": lambda x: self.delete_row("services", ("Введите id услуги", "Введите имя услуги", "Введите цену в час")),
                "Удалить расписание(-я)": lambda x: self.delete_row("schedule", ("Введите id расписания", "Введите id тренера", "Введите id услуги", "Введите дату", "Введите время начала", "Введите время окончания")),
                "Удалить бронирование(-я)": lambda x: self.delete_row("bookings", ("Введите id бронирования", "Введите id клиента", "Введите id расписания"))}))
        self.layout.addWidget(self.delete_row_btn)

        # Работа с таблицами
        self.load_data_btn = QPushButton("Вывести содержимое таблиц")
        self.load_data_btn.clicked.connect(lambda x: self.ultimative_replace_button({
            "Вывести таблицу пользователей": lambda x: self.load_data("users"),
            "Вывести таблицу услуг": lambda x: self.load_data("services"),
            "Вывести таблицу расписания": lambda x: self.load_data("schedule"),
            "Вывести таблицу бронирования": lambda x: self.load_data("bookings")
        }))
        self.layout.addWidget(self.load_data_btn)

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
        self.delete_row_btn.deleteLater()

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
                if button_text == "Поиск услуги по названию":
                    self.search_btn = button
                if button_text == "Обновить запись":
                    self.update_btn = button
                if button_text == "Удалить услугу":
                    self.delete_by_field_btn = button
                if button_text == "Удалить запись":
                    self.delete_row_btn = button

            # Если стек пуст, отключаем кнопку "Назад", иначе оставляем включенной
            if not self.button_stack:
                self.back_button.setEnabled(False)

    def add_user(self):
        dialog = InputDialog(("Введите имя", "Введите телефон", "Введите роль customer/trainer"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            if any(len(input) == 0 for input in user_input):
                QMessageBox.information(self, "Неудача", "Заполните все поля")
                return
            with next(get_db()) as db:
                try:
                    add_user(db, *user_input)
                    QMessageBox.information(self, "Успех", "Пользователь добавлен!")
                except Exception as e:
                    QMessageBox.information(self, "Неудача",
                                            "Неправильные аргументы {}".format(e.args[0].split("\n")[0]))

    def add_service(self):
        dialog = InputDialog(("Введите название", "Введите цену за час"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            if any(len(input) == 0 for input in user_input):
                QMessageBox.information(self, "Неудача", "Заполните все поля")
                return
            with next(get_db()) as db:
                try:
                    s_name, s_price = user_input[0], int(user_input[1])
                    add_service(db, s_name, s_price)
                    QMessageBox.information(self, "Успех", "Услуга добавлена!")
                except Exception as e:
                    QMessageBox.information(self, "Неудача", f"Неправильные аргументы {e}")

    def add_schedule(self):
        dialog = InputDialog(
            ("Введите id тренера", "Введите id услуги", "Введите дату", "Введите время начала", "Введите время конца"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            if any(len(input) == 0 for input in user_input):
                QMessageBox.information(self, "Неудача", "Заполните все поля")
                return
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
            if any(len(input) == 0 for input in user_input):
                QMessageBox.information(self, "Неудача", "Заполните все поля")
                return
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
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def search_data(self):
        dialog = InputDialog(("Введите название услуги"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()[0]
            with next(get_db()) as db:
                try:
                    data, header = search_by_field(db, user_input)
                    self.tables.append(TableWindow(data, header))
                    self.tables[-1].show()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

    def update_record(self, table_name, strings):
        dialog = InputDialog(("Введите id"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            id_row = dialog.get_input()[0]
            dialog = InputDialog(strings)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                updates = dialog.get_input()
                if all(len(input) == 0 for input in updates):
                    QMessageBox.information(self, "Неудача", "Заполните хотя бы одно поле")
                    return
                id_row = int(id_row)
                columns = ()
                if table_name == 'users':
                    columns = ('name', 'phone', 'role')
                if table_name == 'services':
                    columns = ('service_name', 'price_per_hour')
                if table_name == 'schedule':
                    columns = ('trainer_id', 'service_id', 'date_calendar', 'start_time', 'end_time')
                if table_name == 'bookings':
                    columns = ('client_id', 'schedule_id')
                updates = {columns[i]: updates[i] for i in range(len(updates)) if len(updates[i]) > 0}
                with next(get_db()) as db:
                    try:
                        update_row(db, table_name, id_row, updates)  # Пример обновления
                        QMessageBox.information(self, "Успех", "Запись успешно обновлена.")
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка", str(e))

    def delete_by_field(self):
        dialog = InputDialog(("Введите название услуги"))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            value = dialog.get_input()[0]
            with next(get_db()) as db:
                try:
                    delete_by_field(db, "services", "service_name", value)
                    QMessageBox.information(self, "Успех", "Запись успешно удалена.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

    def delete_row(self, table_name, strings):
        dialog = InputDialog(strings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_input()
            if all(len(input) == 0 for input in values):
                QMessageBox.information(self, "Неудача", "Заполните хотя бы одно поле")
                return
            columns = ()
            if table_name == 'users':
                columns = ('id', 'name', 'phone', 'role')
            if table_name == 'services':
                columns = ('id', 'service_name', 'price_per_hour')
            if table_name == 'schedule':
                columns = ('id', 'trainer_id', 'service_id', 'date_calendar', 'start_time', 'end_time')
            if table_name == 'bookings':
                columns = ('id', 'client_id', 'schedule_id')
            values = {columns[i]: values[i] for i in range(len(values)) if len(values[i]) > 0}
            with next(get_db()) as db:
                try:
                    delete_row(db, table_name, values)
                    QMessageBox.information(self, "Успех", "Запись успешно удалена.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", str(e))
