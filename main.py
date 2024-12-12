from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from app.database import engine
from app.models import Base
from app.triggers import create_triggers
from app.procedures import create_procedures

if __name__ == "__main__":
    import sys

    # Инициализация базы данных
    Base.metadata.create_all(bind=engine)
    create_triggers(engine)
    create_procedures(engine)

    # Запуск приложения
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
