import sys

from PyQt6.QtWidgets import QApplication

from app.procedures import create_procedures
from app.tables import create_tables
from app.triggers import create_triggers
from gui.main_window import MainWindow

if __name__ == "__main__":
    # Инициализация базы данных
    create_tables()
    create_triggers()
    create_procedures()

    # Запуск приложения
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
