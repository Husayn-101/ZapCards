"""
The main window of the application, which handles navigation between different views.
"""
from typing import Dict

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QMessageBox
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from config import APP_NAME
from themes import get_current_theme
from home_view import HomeView
from settings_view import SettingsView
from simple_deck_list_view import DeckListView
from simple_quiz_view import QuizView
from web_question_finder import find_questions_for_topic
from simple_db import db
from PyQt5.QtWidgets import QApplication

class DeckGenerationWorker(QObject):
    """
    A worker that runs the deck generation task in a separate thread.
    Emits the generated deck data or an error message upon completion.
    """
    finished = pyqtSignal(object, str)  # Emits deck_data (dict or None) and the original topic
    error = pyqtSignal(str)

    def __init__(self, topic: str, difficulty: str = "Medium"):
        super().__init__()
        self.topic = topic
        self.difficulty = difficulty

    def run(self):
        """Performs the long-running task."""
        try:
            print(f"Worker thread starting to find questions for: {self.topic} (difficulty: {self.difficulty})")
            deck_data = find_questions_for_topic(self.topic, difficulty=self.difficulty)
            self.finished.emit(deck_data, self.topic)
        except Exception as e:
            print(f"Error in worker thread: {e}")
            self.error.emit(f"An unexpected error occurred during generation: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"⚡ {APP_NAME} - Study Companion")
        self.setGeometry(100, 100, 1000, 750)
        self.setMinimumSize(900, 650)
        
        self.apply_theme()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # --- Threading ---
        self.thread = None
        self.worker = None
        # --- View Management ---
        self.views: Dict[str, QWidget] = {}
        self._init_views()
        self._init_connections()

        # Start at the home page
        self.show_view("home")

    def _init_views(self):
        """Initializes and adds all views to the stacked widget."""
        self.views["home"] = HomeView()
        self.views["settings"] = SettingsView()
        self.views["deck_list"] = DeckListView()
        self.views["quiz"] = QuizView()

        for view in self.views.values():
            self.central_widget.addWidget(view)

    def _init_connections(self):
        """Connects signals from views to the main window's slots."""
        # Home view connections
        self.views["home"].navigate_to_decks_signal.connect(lambda: self.show_view("deck_list"))
        self.views["home"].navigate_to_settings_signal.connect(lambda: self.show_view("settings"))
        
        # Settings view connections
        self.views["settings"].theme_changed_signal.connect(self.change_theme)
        self.views["settings"].navigate_back_signal.connect(lambda: self.show_view("home"))
        
        # Deck list view connections
        self.views["deck_list"].start_quiz_signal.connect(self.start_quiz)
        self.views["deck_list"].generate_deck_signal.connect(self.generate_deck)
        self.views["deck_list"].regenerate_deck_signal.connect(self.regenerate_deck)
        self.views["deck_list"].delete_deck_signal.connect(self.delete_deck)
        
        # Quiz view connections
        self.views["quiz"].quiz_finished_signal.connect(lambda: self.show_view("deck_list"))

    def start_quiz(self, deck_id: int):
        self.views["quiz"].load_deck(deck_id)
        self.show_view("quiz")

    def show_view(self, view_name: str):
        """Switches the central widget to the specified view."""
        if view_name == "deck_list":
            self.views["deck_list"].refresh_decks()
        self.central_widget.setCurrentWidget(self.views[view_name])

    def generate_deck(self, topic_with_difficulty: str):
        """
        Handles the request to generate a deck from a topic by running
        the task in a background thread to keep the UI responsive.
        """
        # Parse topic and difficulty
        if "|" in topic_with_difficulty:
            topic, difficulty = topic_with_difficulty.split("|", 1)
        else:
            topic, difficulty = topic_with_difficulty, "Medium"
        
        # Provide immediate feedback to the user and prevent multiple clicks
        generate_button = self.views["deck_list"].generate_deck_button
        generate_button.setEnabled(False)
        generate_button.setText("Generating...")

        print(f"Main window received request to generate deck for: {topic} (difficulty: {difficulty})")

        # Set up the thread and worker
        self.thread = QThread()
        self.worker = DeckGenerationWorker(topic, difficulty)
        self.worker.moveToThread(self.thread)

        # Connect signals from the worker to slots in the main window
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        
        # Clean up after the worker is done
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the thread
        self.thread.start()

    def on_generation_finished(self, deck_data, topic: str):
        """Handles the successful completion of the deck generation task."""
        print("Worker finished, handling results in main thread.")

        # Hide loading indicator here
        if deck_data:
            try:
                deck_id = db.import_deck(deck_data)
                QMessageBox.information(self, "Success", f"Successfully generated and saved the deck '{deck_data['name']}'!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save the generated deck to the database: {e}")
        else:
            QMessageBox.warning(self, "Generation Failed", f"Could not generate a deck for the topic '{topic}'. Please try another topic.")

        self._reset_generate_button()
        self.views["deck_list"].refresh_decks()
    
    def regenerate_deck(self, deck_id: int, difficulty: str):
        """Regenerates an existing deck with new difficulty."""
        # Get the deck name first
        deck_name = None
        for deck in self.views["deck_list"].decks:
            if deck["id"] == deck_id:
                deck_name = deck["name"]
                break
        
        if not deck_name:
            QMessageBox.warning(self, "Error", "Could not find deck to regenerate.")
            return
        
        # Extract topic from deck name (assuming format like "Topic Name")
        topic = deck_name.replace(" - Easy", "").replace(" - Medium", "").replace(" - Hard", "")
        
        # Set up regeneration (similar to generate_deck but replace existing)
        generate_button = self.views["deck_list"].generate_deck_button
        generate_button.setEnabled(False)
        generate_button.setText("Regenerating...")
        
        print(f"Regenerating deck {deck_id} for topic: {topic} with difficulty: {difficulty}")
        
        self.thread = QThread()
        self.worker = DeckGenerationWorker(topic, difficulty)
        self.worker.deck_id_to_replace = deck_id  # Store which deck to replace
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_regeneration_finished)
        self.worker.error.connect(self.on_generation_error)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()
    
    def on_regeneration_finished(self, deck_data, topic: str):
        """Handles regeneration completion by replacing the existing deck."""
        print("Regeneration finished, replacing existing deck.")
        
        if deck_data and hasattr(self.worker, 'deck_id_to_replace'):
            try:
                # Delete old cards
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cards WHERE deck_id = ?", (self.worker.deck_id_to_replace,))
                
                # Insert new cards
                for card in deck_data["cards"]:
                    distractors_json = None
                    if "distractors" in card:
                        import json
                        distractors_json = json.dumps(card["distractors"])
                    
                    cursor.execute("INSERT INTO cards (deck_id, front, back, distractors) VALUES (?, ?, ?, ?)", 
                                 (self.worker.deck_id_to_replace, card["front"], card["back"], distractors_json))
                
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Success", f"Successfully regenerated the deck with new difficulty!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to regenerate the deck: {e}")
        else:
            QMessageBox.warning(self, "Regeneration Failed", f"Could not regenerate the deck for topic '{topic}'.")
        
        self._reset_generate_button()
        self.views["deck_list"].refresh_decks()
    
    def delete_deck(self, deck_id: int):
        """Delete a deck and refresh the list."""
        try:
            db.delete_deck(deck_id)
            QMessageBox.information(self, "Success", "Deck deleted successfully!")
            self.views["deck_list"].refresh_decks()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete deck: {e}")
    
    def change_theme(self, theme_name: str):
        """Change the application theme."""
        # Apply new theme to main window
        self.apply_theme()
        
        # Apply new theme to application
        theme = get_current_theme()
        QApplication.instance().setStyleSheet(f"""
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
        
        # Recreate all views with new theme
        current_view = self.central_widget.currentWidget()
        current_view_name = "settings"  # Stay on settings after theme change
        for name, view in self.views.items():
            if view == current_view:
                current_view_name = name
                break
        
        # Clear old views
        for view in list(self.views.values()):
            self.central_widget.removeWidget(view)
            view.setParent(None)
        
        self.views.clear()
        
        # Recreate views
        self._init_views()
        self._init_connections()
        
        # Return to settings view
        self.show_view("settings")
    
    def apply_theme(self):
        """Apply current theme to main window."""
        theme = get_current_theme()
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {theme['background']}, stop:0.5 {theme['panel_bg']}, stop:1 {theme['background']});
                border: 2px solid {theme['button_border']};
                background-image: {theme.get('grid_texture', 'none')}, {theme.get('scan_lines', 'none')};
            }}
            QStackedWidget {{
                background: {theme['window_bg']};
                border: 1px solid {theme['button_border']};
                border-radius: 8px;
                margin: 15px;
                background-image: {theme.get('scan_lines', 'none')};
            }}
        """)

    def on_generation_error(self, error_message: str):
        """Handles errors reported by the worker thread."""
        print(f"Worker reported an error: {error_message}")
        QMessageBox.critical(self, "Error", error_message)
        self._reset_generate_button()

    def _reset_generate_button(self):
        """Resets the 'Generate' button to its initial state."""
        try:
            generate_button = self.views["deck_list"].generate_deck_button
            generate_button.setText("✨ Generate from Topic")
            generate_button.setEnabled(True)
        except RuntimeError:
            # This can happen if the view has been closed.
            pass