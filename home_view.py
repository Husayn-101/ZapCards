"""
Home page view explaining the QuizGO application.
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
                             QScrollArea, QFrame)

from themes import get_current_theme
from widgets import PrimaryButton

class HomeView(QWidget):
    navigate_to_decks_signal = pyqtSignal()
    navigate_to_settings_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        
        theme = get_current_theme()
        
        # Title
        title = QLabel("⚡ ZAPCARDS - MIND PALACE ⚡")
        title.setStyleSheet(f"""
            QLabel {{
                font-family: {theme['title_font']};
                font-size: 28px;
                font-weight: bold;
                color: {theme['primary']};
                text-align: center;
                padding: 20px;
                margin-bottom: 20px;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("""
        Welcome to ZapCards - Your Personal Study Companion!
        
        🎯 WHAT IS ZAPCARDS?
        ZapCards transforms any topic into interactive quiz sessions using AI-powered question generation.
        Perfect for students, professionals, or anyone who loves learning!
        
        ⚡ KEY FEATURES:
        • AI-Generated Quizzes: Enter any topic and get instant multiple-choice questions
        • Difficulty Levels: Choose Easy, Medium, or Hard based on your knowledge
        • Smart Learning: Spaced repetition system helps you remember better
        • Multiple Themes: 8+ aesthetic themes from retro to modern
        • Progress Tracking: Monitor your learning journey
        
        🚀 HOW TO GET STARTED:
        1. Click "VIEW DECKS" to see your quiz collections
        2. Generate new quizzes by entering any topic
        3. Take quizzes and track your progress
        4. Customize your experience in Settings
        
        📚 PERFECT FOR:
        • Students preparing for exams
        • Professionals learning new skills  
        • Trivia enthusiasts
        • Anyone who wants to make learning fun!
        """)
        
        desc.setStyleSheet(f"""
            QLabel {{
                font-family: {theme['font_family']};
                font-size: {theme['font_size']};
                color: {theme['foreground']};
                background: {theme['panel_bg']};
                border: 2px solid {theme['button_border']};
                border-radius: 8px;
                padding: 25px;
                line-height: 1.6;
                background-image: {theme.get('scan_lines', 'none')};
            }}
        """)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        decks_button = PrimaryButton("📚 VIEW DECKS")
        decks_button.clicked.connect(self.navigate_to_decks_signal.emit)
        
        settings_button = PrimaryButton("⚙️ SETTINGS")  
        settings_button.clicked.connect(self.navigate_to_settings_signal.emit)
        
        button_layout.addWidget(decks_button)
        button_layout.addStretch()
        button_layout.addWidget(settings_button)
        
        layout.addLayout(button_layout)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: {theme['window_bg']};
            }}
        """)
        
        main_layout.addWidget(scroll)
    
    def refresh_theme(self):
        """Refresh the UI with current theme."""
        # Simple refresh - styles will update on next interaction
        pass