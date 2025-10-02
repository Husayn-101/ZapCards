"""
Simple deck list view without SQLAlchemy dependencies.
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QVBoxLayout,
                             QWidget, QLabel, QHBoxLayout, QDialog, QLineEdit, 
                             QPushButton, QComboBox, QMenu, QAction, QMessageBox)

from themes import get_current_theme
from widgets import PrimaryButton
from simple_db import db

class DeckListView(QWidget):
    start_quiz_signal = pyqtSignal(int)
    generate_deck_signal = pyqtSignal(str)
    regenerate_deck_signal = pyqtSignal(int, str)  # deck_id, difficulty
    delete_deck_signal = pyqtSignal(int)  # deck_id

    def __init__(self):
        super().__init__()
        self.decks = []
        self.selected_deck_id = None
        self.init_ui()
        self.refresh_decks()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Dynamic title based on theme
        title = QLabel("📚 YOUR QUIZ DECKS 📚")
        theme = get_current_theme()
        title.setStyleSheet(f"""
            QLabel {{
                font-family: {theme['title_font']};
                font-size: 22px;
                font-weight: bold;
                color: {theme['primary']};
                background: {theme['panel_bg']};
                border: 2px solid {theme['button_border']};
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                text-align: center;
                background-image: {theme.get('scan_lines', 'none')};
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.deck_list_widget = QListWidget()
        self.deck_list_widget.setStyleSheet(f"""
            QListWidget {{
                background: {theme['background']};
                color: {theme['foreground']};
                border: 2px solid {theme['button_border']};
                border-radius: 8px;
                padding: 15px;
                font-family: {theme['font_family']};
                font-size: {theme['font_size']};
                selection-background-color: {theme['primary']};
                background-image: {theme.get('grid_texture', 'none')};
            }}
            QListWidget::item {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme['panel_bg']}, stop:1 {theme['button_bg']});
                border: 1px solid {theme['secondary']};
                border-radius: 6px;
                padding: 15px;
                margin: 6px;
                font-weight: bold;
                background-image: {theme.get('scan_lines', 'none')};
            }}
            QListWidget::item:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme['primary']}, stop:1 {theme['accent']});
                border-color: {theme['accent']};
                color: {theme['background']};
                border-width: 2px;
            }}
            QListWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme['primary']}, stop:1 {theme['secondary']});
                color: {theme['background']};
                border-color: {theme['accent']};
                border-width: 2px;
            }}
        """)
        self.deck_list_widget.itemClicked.connect(self.on_deck_selected)
        self.deck_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.deck_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.deck_list_widget)

        button_layout = QHBoxLayout()
        self.start_quiz_button = PrimaryButton("▶️ START QUIZ")
        self.start_quiz_button.clicked.connect(self.on_start_quiz)
        self.start_quiz_button.setEnabled(False)

        self.generate_deck_button = PrimaryButton("🎯 NEW DECK")
        self.generate_deck_button.clicked.connect(self.on_generate_deck)

        button_layout.addWidget(self.generate_deck_button)
        button_layout.addStretch()
        button_layout.addWidget(self.start_quiz_button)
        layout.addLayout(button_layout)
        self.generate_deck_button.setToolTip("Enter a topic and generate a new deck with questions from the internet.")

    def refresh_decks(self):
        self.deck_list_widget.clear()
        self.decks = db.get_all_decks()
        for deck in self.decks:
            item = QListWidgetItem(deck["name"])
            item.setData(32, deck["id"])
            self.deck_list_widget.addItem(item)

    def on_deck_selected(self, item):
        self.selected_deck_id = item.data(32)
        self.start_quiz_button.setEnabled(True)

    def on_start_quiz(self):
        if self.selected_deck_id is not None:
            self.start_quiz_signal.emit(self.selected_deck_id)

    def on_generate_deck(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel
        
        dialog = QDialog(self)
        theme = get_current_theme()
        dialog.setWindowTitle("🎯 Generate New Deck")
        dialog.setFixedSize(450, 320)
        dialog.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {theme['background']}, stop:1 {theme['panel_bg']});
                border: 2px solid {theme['button_border']};
                background-image: {theme.get('grid_texture', 'none')};
            }}
            QLabel {{
                font-family: {theme['font_family']};
                font-weight: bold;
                color: {theme['foreground']};
                font-size: {theme['font_size']};
            }}
            QLineEdit {{
                background: {theme['background']};
                border: 1px solid {theme['button_border']};
                border-radius: 4px;
                padding: 10px;
                font-family: {theme['font_family']};
                font-size: {theme['font_size']};
                color: {theme['foreground']};
                background-image: {theme.get('scan_lines', 'none')};
            }}
            QComboBox {{
                background: {theme['panel_bg']};
                border: 1px solid {theme['button_border']};
                border-radius: 4px;
                padding: 10px;
                font-family: {theme['font_family']};
                font-weight: bold;
                color: {theme['foreground']};
                background-image: {theme.get('scan_lines', 'none')};
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
        
        layout = QVBoxLayout(dialog)
        
        # Topic input
        layout.addWidget(QLabel("📝 Enter Topic:"))
        topic_input = QLineEdit()
        topic_input.setPlaceholderText("e.g., History, Science, Movies...")
        layout.addWidget(topic_input)
        
        # Difficulty selection
        layout.addWidget(QLabel("⚙️ Select Difficulty:"))
        difficulty_combo = QComboBox()
        difficulty_combo.addItems(["😊 Easy", "🤔 Medium", "😤 Hard"])
        difficulty_combo.setCurrentText("🤔 Medium")
        layout.addWidget(difficulty_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = PrimaryButton("✨ GENERATE")
        cancel_button = PrimaryButton("❌ CANCEL")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            topic = topic_input.text().strip()
            difficulty = difficulty_combo.currentText()
            if topic:
                print(f"User entered topic: {topic}, difficulty: {difficulty}")
                self.generate_deck_signal.emit(f"{topic}|{difficulty}")
    
    def show_context_menu(self, position):
        item = self.deck_list_widget.itemAt(position)
        if item is None:
            return
        
        deck_id = item.data(32)
        deck_name = item.text()
        
        menu = QMenu(self)
        
        # Change difficulty submenu
        change_difficulty_menu = menu.addMenu("Change Difficulty")
        
        easy_action = QAction("Easy", self)
        medium_action = QAction("Medium", self)
        hard_action = QAction("Hard", self)
        
        easy_action.triggered.connect(lambda: self.regenerate_deck(deck_id, deck_name, "Easy"))
        medium_action.triggered.connect(lambda: self.regenerate_deck(deck_id, deck_name, "Medium"))
        hard_action.triggered.connect(lambda: self.regenerate_deck(deck_id, deck_name, "Hard"))
        
        change_difficulty_menu.addAction(easy_action)
        change_difficulty_menu.addAction(medium_action)
        change_difficulty_menu.addAction(hard_action)
        
        # Delete option
        menu.addSeparator()
        delete_action = QAction("🗑️ Delete Deck", self)
        delete_action.triggered.connect(lambda: self.delete_deck(deck_id, deck_name))
        menu.addAction(delete_action)
        
        menu.exec_(self.deck_list_widget.mapToGlobal(position))
    
    def regenerate_deck(self, deck_id, deck_name, difficulty):
        reply = QMessageBox.question(self, "Regenerate Deck", 
                                   f"Regenerate '{deck_name}' with {difficulty} difficulty?\n\nThis will replace all existing questions.",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            print(f"Regenerating deck {deck_id} with difficulty: {difficulty}")
            self.regenerate_deck_signal.emit(deck_id, difficulty)
    
    def delete_deck(self, deck_id, deck_name):
        reply = QMessageBox.question(self, "Delete Deck", 
                                   f"Permanently delete '{deck_name}'?\n\nThis action cannot be undone.",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            print(f"Deleting deck {deck_id}")
            self.delete_deck_signal.emit(deck_id)
    
    def refresh_theme(self):
        """Refresh the UI with current theme."""
        # Simple refresh - just update the decks
        self.refresh_decks()