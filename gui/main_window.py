from datetime import date, datetime

from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog, QLineEdit, QLabel, \
    QDialogButtonBox

from app.database import get_db
from app.handlers import add_user, add_schedule, add_service, add_booking, clear_tables, clear_user, clear_service, \
    clear_booking, clear_schedule


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

        # Устанавливаем self.layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(button_box)
        self.setLayout(self.layout)

    def get_input(self):
        return self.input_line.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Booking")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.button_stack = []

        self.button_functions = {
            "Добавить": self.replace_add_button,
            "Очистить таблицы": self.replace_clear_table_button,
        }

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.replace_add_button)
        self.layout.addWidget(self.add_btn)

        self.clear_tables_btn = QPushButton("Очистить таблицы")
        self.clear_tables_btn.clicked.connect(self.replace_clear_table_button)
        self.layout.addWidget(self.clear_tables_btn)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

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

            # Если стек пуст, отключаем кнопку "Назад", иначе оставляем включенной
            if not self.button_stack:
                self.back_button.setEnabled(False)

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

    def add_service(self):
        dialog = InputDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    s_name, s_price = user_input.split(' ')[0], int(user_input.split(' ')[1])
                    add_service(db, s_name, s_price)
                    QMessageBox.information(self, "Успех", "Услуга добавлена!")
                except TypeError:
                    QMessageBox.information(self, "Неудача", "Неправильные аргументы")

    def add_schedule(self):
        dialog = InputDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    parts = user_input.split()
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
        dialog = InputDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_input = dialog.get_input()
            with next(get_db()) as db:
                try:
                    client_id, schedule_id = map(int, user_input.split(' '))
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
