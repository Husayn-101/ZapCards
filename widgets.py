"""
Reusable custom widgets for the Quiz-Go UI.
"""

from PyQt5.QtWidgets import QPushButton
from themes import get_current_theme

class StrangerPanel(QPushButton):
    """A dark panel with 80s sci-fi styling."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        theme = get_current_theme()
        self.setStyleSheet(f"""
            QPushButton {{
                background: {theme['panel_bg']};
                border: 1px solid {theme['button_border']};
                border-radius: 2px;
                padding: 8px;
                font-family: {theme['font_family']};
                background-image: {theme.get('grid_texture', 'none')};
            }}
        """)

class NeonLabel(QPushButton):
    """A neon-styled label with 80s glow effect."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        theme = get_current_theme()
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {theme['primary']};
                border: none;
                font-family: {theme['title_font']};
                font-weight: bold;
                font-size: {theme['title_size']};
                letter-spacing: 2px;
            }}
        """)
        self.setEnabled(False)

class PrimaryButton(QPushButton):
    """Themed button that adapts to current theme."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        theme = get_current_theme()
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['button_bg']}, stop:1 {theme['background']});
                color: {theme['foreground']};
                border: 2px solid {theme['button_border']};
                border-radius: 4px;
                padding: 12px 24px;
                font-family: {theme['font_family']};
                font-weight: bold;
                font-size: {theme['font_size']};
                text-transform: uppercase;
                letter-spacing: 1px;
                background-image: {theme.get('scan_lines', 'none')};
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['primary']}, stop:1 {theme['button_bg']});
                border-color: {theme['accent']};
                color: {theme['background']};
                border-width: 3px;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['background']}, stop:1 {theme['primary']});
                border-color: {theme['secondary']};
                color: {theme['accent']};
            }}
            QPushButton:disabled {{
                background: {theme.get('shadow', '#000000')};
                color: #444444;
                border-color: #333333;
            }}
        """)