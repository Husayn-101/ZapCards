"""
Settings view for theme selection and app configuration.
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                             QComboBox, QGroupBox, QScrollArea)

from themes import get_current_theme, get_theme_list, set_theme
from widgets import PrimaryButton

class SettingsView(QWidget):
    theme_changed_signal = pyqtSignal(str)
    navigate_back_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        theme = get_current_theme()
        
        # Title
        title = QLabel("⚙️ SETTINGS & PREFERENCES")
        title.setStyleSheet(f"""
            QLabel {{
                font-family: {theme['title_font']};
                font-size: 24px;
                font-weight: bold;
                color: {theme['primary']};
                text-align: center;
                padding: 20px;
                margin-bottom: 20px;
                background: {theme['panel_bg']};
                border: 2px solid {theme['button_border']};
                border-radius: 8px;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Scroll area for settings
        scroll = QScrollArea()
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        
        # Theme Selection Group
        theme_group = QGroupBox("🎨 APPEARANCE THEMES")
        theme_group.setStyleSheet(f"""
            QGroupBox {{
                font-family: {theme['font_family']};
                font-size: 16px;
                font-weight: bold;
                color: {theme['foreground']};
                background: {theme['window_bg']};
                border: 2px solid {theme['button_border']};
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }}
        """)
        
        theme_layout = QVBoxLayout(theme_group)
        
        # Theme description
        theme_desc = QLabel("Choose your perfect study aesthetic:")
        theme_desc.setStyleSheet(f"""
            QLabel {{
                font-family: {theme['font_family']};
                color: {theme['foreground']};
                margin-bottom: 15px;
            }}
        """)
        theme_layout.addWidget(theme_desc)
        
        # Theme selector
        theme_selector_layout = QHBoxLayout()
        theme_label = QLabel("Current Theme:")
        theme_label.setStyleSheet(f"color: {theme['foreground']}; font-weight: bold;")
        
        self.theme_combo = QComboBox()
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background: {theme['button_bg']};
                border: 2px solid {theme['button_border']};
                border-radius: 4px;
                padding: 8px;
                font-family: {theme['font_family']};
                font-weight: bold;
                color: {theme['foreground']};
                min-width: 200px;
            }}
            QComboBox::drop-down {{
                border: none;
                background: {theme['primary']};
            }}
            QComboBox::down-arrow {{
                width: 12px;
                height: 12px;
            }}
        """)
        
        # Populate theme options
        for theme_key, theme_name in get_theme_list():
            self.theme_combo.addItem(theme_name, theme_key)
        
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        theme_selector_layout.addWidget(theme_label)
        theme_selector_layout.addWidget(self.theme_combo)
        theme_selector_layout.addStretch()
        
        theme_layout.addLayout(theme_selector_layout)
        
        # Theme previews
        preview_label = QLabel("🎭 Theme Previews:")
        preview_label.setStyleSheet(f"color: {theme['foreground']}; font-weight: bold; margin-top: 15px;")
        theme_layout.addWidget(preview_label)
        
        themes_info = QLabel("""
📟 Retro Student - Classic Windows 95 computer lab vibes
📚 Notebook Scribble - Hand-drawn notebook with doodles  
🌸 Pastel Teen Core - Soft pastels with motivational energy
🎮 GameBoy Study - Retro green pixel screen aesthetic
🖤 Mall Goth Mode - Dark theme for late-night study sessions
🕹 Arcade Neon - Bright neon colors on black background
✏️ Minimal Stationery - Clean, professional beige theme
🌌 Stranger Things - Dark sci-fi with neon accents
        """)
        themes_info.setStyleSheet(f"""
            QLabel {{
                font-family: {theme['font_family']};
                color: {theme['foreground']};
                background: {theme['panel_bg']};
                border: 1px solid {theme['button_border']};
                border-radius: 4px;
                padding: 15px;
                margin: 10px 0;
            }}
        """)
        theme_layout.addWidget(themes_info)
        
        layout.addWidget(theme_group)
        
        # Back button
        back_button = PrimaryButton("🔙 BACK TO HOME")
        back_button.clicked.connect(self.navigate_back_signal.emit)
        layout.addWidget(back_button)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: {theme['background']};
            }}
        """)
        
        main_layout.addWidget(scroll)
    
    def on_theme_changed(self):
        """Handle theme selection change."""
        theme_key = self.theme_combo.currentData()
        if theme_key and set_theme(theme_key):
            self.theme_changed_signal.emit(theme_key)
    
    def refresh_theme(self):
        """Refresh the UI with current theme."""
        # Simple refresh - styles will update on next interaction
        pass