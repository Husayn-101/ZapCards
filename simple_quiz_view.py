"""
Simple quiz view without SQLAlchemy dependencies.
"""

import random
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QRadioButton,
                             QButtonGroup, QHBoxLayout)

from themes import get_current_theme
from widgets import PrimaryButton
from simple_db import db

class QuizView(QWidget):
    quiz_finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.deck_id = None
        self.questions = []
        self.current_question_index = -1
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        self.question_label = QLabel("❓ Question will appear here...")
        theme = get_current_theme()
        self.question_label.setStyleSheet(f"""
            QLabel {{
                font-family: {theme['font_family']};
                font-size: 16px;
                font-weight: bold;
                color: {theme['foreground']};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {theme['background']}, stop:1 {theme['panel_bg']});
                border: 2px solid {theme['button_border']};
                border-radius: 8px;
                padding: 25px;
                margin-bottom: 25px;
                background-image: {theme.get('scan_lines', 'none')};
            }}
        """)
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.question_label)

        self.options_group = QButtonGroup(self)
        self.radio_buttons = []
        for i in range(4):
            radio = QRadioButton(f"● OPTION {i+1}")
            radio.setStyleSheet(f"""
                QRadioButton {{
                    font-family: {theme['font_family']};
                    font-size: 14px;
                    font-weight: bold;
                    color: {theme['foreground']};
                    background: {theme['panel_bg']};
                    border: 1px solid {theme['secondary']};
                    border-radius: 6px;
                    padding: 15px;
                    margin: 8px;
                    background-image: {theme.get('scan_lines', 'none')};
                }}
                QRadioButton:hover {{
                    background: {theme['button_bg']};
                    border-color: {theme['accent']};
                    color: {theme['accent']};
                }}
                QRadioButton:checked {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {theme['primary']}, stop:1 {theme['secondary']});
                    color: {theme['background']};
                    border-color: {theme['accent']};
                    border-width: 2px;
                }}
                QRadioButton::indicator {{
                    width: 16px;
                    height: 16px;
                    border: 2px solid {theme['button_border']};
                    border-radius: 8px;
                    background: {theme['background']};
                }}
                QRadioButton::indicator:checked {{
                    background: {theme['primary']};
                    border-color: {theme['accent']};
                }}
            """)
            self.radio_buttons.append(radio)
            self.options_group.addButton(radio, i)
            self.main_layout.addWidget(radio)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet(f"font-size: 16px; font-weight: bold;")
        self.main_layout.addWidget(self.feedback_label)

        button_layout = QHBoxLayout()
        self.submit_button = PrimaryButton("✨ SUBMIT")
        self.submit_button.clicked.connect(self.check_answer)
        
        self.finish_button = PrimaryButton("🏆 FINISH")
        self.finish_button.clicked.connect(self.finish_quiz)

        button_layout.addWidget(self.finish_button)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        self.main_layout.addLayout(button_layout)

    def load_deck(self, deck_id: int):
        self.deck_id = deck_id
        cards = db.get_deck_cards(deck_id)
        if len(cards) >= 2:
            self.questions = self.generate_questions(cards)
            random.shuffle(self.questions)
            self.current_question_index = -1
            self.next_question()

    def generate_questions(self, cards):
        questions = []
        
        for card in cards[:10]:  # Limit to 10 questions
            correct_answer = card["back"]
            print(f"Card: {card['front']} -> {card['back']}")
            print(f"Has distractors: {'distractors' in card}")
            if "distractors" in card:
                print(f"Distractors: {card['distractors']}")
            
            # Check if card has distractors from API
            if "distractors" in card and len(card["distractors"]) >= 3:
                distractors = card["distractors"][:3]
                print(f"Using API distractors: {distractors}")
            else:
                # Fallback: use other cards' answers as distractors
                all_answers = [c["back"] for c in cards]
                other_answers = [ans for ans in all_answers if ans != correct_answer]
                
                if len(other_answers) >= 3:
                    distractors = random.sample(other_answers, 3)
                else:
                    distractors = other_answers[:]
                    generic_distractors = ["None of the above", "Not applicable", "Unknown"]
                    while len(distractors) < 3:
                        distractors.append(generic_distractors[len(distractors) % len(generic_distractors)])
                print(f"Using fallback distractors: {distractors}")
            
            choices = distractors + [correct_answer]
            random.shuffle(choices)
            
            questions.append({
                "question": card["front"],
                "choices": choices,
                "answer": correct_answer
            })
        return questions

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            self.finish_quiz()
            return

        theme = get_current_theme()
        self.feedback_label.setText("")
        self.submit_button.setEnabled(True)
        self.options_group.setExclusive(False)
        for radio in self.radio_buttons:
            radio.setChecked(False)
            radio.setStyleSheet(f"color: {theme['foreground']};")
        self.options_group.setExclusive(True)

        question_data = self.questions[self.current_question_index]
        self.question_label.setText(question_data["question"])

        for i, choice in enumerate(question_data["choices"]):
            self.radio_buttons[i].setText(choice)
            self.radio_buttons[i].setVisible(True)
        
        for i in range(len(question_data["choices"]), 4):
            self.radio_buttons[i].setVisible(False)

    def check_answer(self):
        selected_button = self.options_group.checkedButton()
        if not selected_button:
            return

        self.submit_button.setEnabled(False)
        question_data = self.questions[self.current_question_index]
        selected_answer = selected_button.text()
        correct_answer = question_data["answer"]

        is_correct = (selected_answer == correct_answer)
        theme = get_current_theme()

        if is_correct:
            self.feedback_label.setText("Correct!")
            self.feedback_label.setStyleSheet(f"color: {theme['success']}; font-weight: bold;")
        else:
            self.feedback_label.setText(f"Incorrect. The answer is: {correct_answer}")
            self.feedback_label.setStyleSheet(f"color: {theme['error']}; font-weight: bold;")

        QTimer.singleShot(1500, self.next_question)

    def finish_quiz(self):
        self.quiz_finished_signal.emit()
    
    def refresh_theme(self):
        """Refresh the UI with current theme."""
        # Simple refresh - styles will update on next interaction
        pass