"""
Top-level configuration variables for the ZapCards application.
"""

from pathlib import Path

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip
    pass

# --- General ---
APP_NAME = "ZapCards"

# --- Paths ---
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data" / "zapcards.db"
ASSETS_PATH = BASE_DIR / "assets"

# --- UI Theme (Stranger Things 80s Aesthetic) ---
# Dark backgrounds with neon colors, retro sci-fi vibes
THEME = {
    "background": "#0B0B0F",      # Deep dark blue-black
    "window_bg": "#1A1A2E",      # Dark navy for panels
    "panel_bg": "#16213E",       # Slightly lighter panel background
    "foreground": "#E94560",     # Neon red text
    "primary": "#FF073A",        # Bright neon red
    "secondary": "#00D4FF",      # Electric blue
    "accent": "#39FF14",         # Neon green
    "purple": "#8A2BE2",         # Blue violet
    "highlight": "#FFD700",      # Gold
    "success": "#00FF41",       # Matrix green
    "error": "#FF073A",         # Neon red
    "button_bg": "#2E2E48",     # Dark purple-gray
    "button_border": "#E94560", # Neon red border
    "shadow": "#000000",        # Pure black shadow
    "glow": "#FF073A",          # Red glow effect
    "font_family": "'Courier New', 'Consolas', monospace",
    "title_font": "'Impact', 'Arial Black', sans-serif",
    "font_size": "14px",
    "title_size": "20px",
    # Texture patterns (CSS background patterns)
    "grid_texture": "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(233, 69, 96, 0.1) 2px, rgba(233, 69, 96, 0.1) 4px)",
    "scan_lines": "repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(0, 212, 255, 0.03) 2px, rgba(0, 212, 255, 0.03) 4px)",
}

# --- API Configuration ---
# Get your free API key from: https://makersuite.google.com/app/apikey
# For security, use environment variable or replace with your actual key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')

# --- Spaced Repetition ---
# Delays in days for each Leitner box.
# Box 0 is for new/failed cards, so the delay is short.
LEITNER_BOX_DELAYS = {0: 1, 1: 3, 2: 7, 3: 14, 4: 30}
LEITNER_BOX_COUNT = len(LEITNER_BOX_DELAYS)

# --- 80s Aesthetic Elements ---
STRANGER_THINGS_EMOJIS = {
    "lightning": "⚡",
    "radio": "📻",
    "flashlight": "🔦",
    "warning": "⚠️",
    "skull": "💀",
    "alien": "👾",
    "computer": "💻",
    "cassette": "📼",
}