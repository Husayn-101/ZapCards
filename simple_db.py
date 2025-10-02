"""
Simple SQLite database implementation without SQLAlchemy.
"""

import sqlite3
import json
from pathlib import Path
from config import DB_PATH

def init_db():
    """Initialize the database and create tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER NOT NULL,
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            distractors TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (deck_id) REFERENCES decks (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            card_id INTEGER PRIMARY KEY,
            leitner_box INTEGER DEFAULT 0,
            last_reviewed_at TIMESTAMP,
            next_review_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_id) REFERENCES cards (id)
        )
    ''')
    
    conn.commit()
    
    # Add distractors column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE cards ADD COLUMN distractors TEXT")
        conn.commit()
        print("Added distractors column to cards table")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Add sample data if no decks exist
    cursor.execute("SELECT COUNT(*) FROM decks")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO decks (name, description) VALUES (?, ?)", 
                      ("Sample Vocabulary", "Basic vocabulary words"))
        deck_id = cursor.lastrowid
        
        sample_cards = [
            ("Hello", "A greeting"),
            ("Goodbye", "A farewell"),
            ("Thank you", "Expression of gratitude"),
            ("Please", "Polite request word"),
            ("Sorry", "Expression of apology")
        ]
        
        for front, back in sample_cards:
            cursor.execute("INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)", 
                          (deck_id, front, back))
        
        conn.commit()
    
    conn.close()

class SimpleDB:
    def __init__(self):
        self.db_path = DB_PATH
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_all_decks(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM decks")
        decks = cursor.fetchall()
        conn.close()
        return [{"id": d[0], "name": d[1], "description": d[2]} for d in decks]
    
    def get_deck_cards(self, deck_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, front, back, distractors FROM cards WHERE deck_id = ?", (deck_id,))
        cards = cursor.fetchall()
        conn.close()
        result = []
        for c in cards:
            card = {"id": c[0], "front": c[1], "back": c[2]}
            if c[3]:  # If distractors exist
                import json
                try:
                    card["distractors"] = json.loads(c[3])
                except:
                    pass
            result.append(card)
        return result

    def import_deck(self, deck_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insert deck
        cursor.execute("INSERT INTO decks (name, description) VALUES (?, ?)", 
                      (deck_data.get("name", "Unnamed Deck"), deck_data.get("description", "")))
        deck_id = cursor.lastrowid
        
        # Insert cards with distractors
        for card_data in deck_data.get("cards", []):
            distractors_json = None
            if "distractors" in card_data:
                distractors_json = json.dumps(card_data["distractors"])
            
            cursor.execute("INSERT INTO cards (deck_id, front, back, distractors) VALUES (?, ?, ?, ?)", 
                          (deck_id, card_data.get("front", ""), card_data.get("back", ""), distractors_json))
        
        conn.commit()
        conn.close()
        return deck_id
    
    def delete_deck(self, deck_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete cards first (foreign key constraint)
        cursor.execute("DELETE FROM cards WHERE deck_id = ?", (deck_id,))
        # Delete deck
        cursor.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        
        conn.commit()
        conn.close()

# Global database instance
db = SimpleDB()