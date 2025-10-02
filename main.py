import sys

from PyQt5.QtWidgets import QApplication

from simple_db import init_db
from main_window import MainWindow
from themes import get_current_theme


def main():
    """
    The main entry point for the ZapCards application.

    Initializes the database and launches the PyQt5 user interface.
    """
    # 1. Initialize the database (creates tables if they don't exist)
    print("Initializing database...")
    init_db()
    print("Database initialized.")

    # 2. Create and run the PyQt application
    app = QApplication(sys.argv)
    
    # Apply current theme
    theme = get_current_theme()
    app.setStyleSheet(f"""
        QWidget {{
            font-family: {theme['font_family']};
            font-size: {theme['font_size']};
            background: {theme['background']};
            color: {theme['foreground']};
        }}
        QMessageBox {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {theme['background']}, stop:1 {theme['panel_bg']});
            border: 2px solid {theme['button_border']};
            background-image: {theme.get('grid_texture', 'none')};
        }}
        QMessageBox QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {theme['button_bg']}, stop:1 {theme['background']});
            border: 2px solid {theme['button_border']};
            border-radius: 4px;
            padding: 10px 20px;
            font-weight: bold;
            color: {theme['foreground']};
            background-image: {theme.get('scan_lines', 'none')};
        }}
        QMessageBox QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {theme['primary']}, stop:1 {theme['secondary']});
            color: {theme['background']};
        }}
    """)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()