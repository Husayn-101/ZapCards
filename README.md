# ⚡ ZapCards - AI-Powered Study Companion

**Transform any topic into interactive quiz sessions with AI-generated questions!**

ZapCards is a modern, aesthetic study application that uses Google's Gemini AI to generate personalized quiz decks on any subject. Perfect for students, professionals, and lifelong learners who want to make studying engaging and effective.

## ✨ Key Features

### 🤖 **AI-Powered Question Generation**
- Enter any topic and get instant multiple-choice questions
- Powered by Google Gemini AI for high-quality, relevant content
- Smart distractor generation for challenging quiz options

### 🎨 **8 Stunning Themes**
- 🌌 **Stranger Things** - Dark sci-fi with neon accents
- 📟 **Retro Student** - Classic Windows 95 computer lab vibes
- 📚 **Notebook Scribble** - Hand-drawn notebook with doodles
- 🌸 **Pastel Teen Core** - Soft pastels with motivational energy
- 🎮 **GameBoy Study** - Retro green pixel screen aesthetic
- 🖤 **Mall Goth Mode** - Dark theme for late-night study sessions
- 🕹 **Arcade Neon** - Bright neon colors on black background
- ✏️ **Minimal Stationery** - Clean, professional beige theme

### 📚 **Smart Learning System**
- **Difficulty Levels**: Easy, Medium, Hard question generation
- **Spaced Repetition**: Leitner box system for optimal retention
- **Progress Tracking**: Monitor your learning journey
- **Deck Management**: Create, edit, delete, and regenerate quiz decks

### 🎯 **User-Friendly Interface**
- **Home Page**: Welcome screen with feature overview
- **Settings**: Easy theme switching and preferences
- **Right-Click Menus**: Quick deck actions (delete, change difficulty)
- **Responsive Design**: Works on desktop and laptop screens

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Husayn-101/zapcards.git
   cd zapcards
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and replace `your_actual_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY=your-actual-api-key-here
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 📖 How to Use

### Getting Started
1. **Launch ZapCards** - Start with the welcome home page
2. **Choose Your Theme** - Go to Settings and pick your favorite aesthetic
3. **Generate Your First Deck** - Click "VIEW DECKS" → "🎯 NEW DECK"
4. **Enter Any Topic** - History, Science, Movies, Programming, etc.
5. **Select Difficulty** - Easy for beginners, Hard for experts
6. **Start Learning** - Take quizzes and track your progress!

### Advanced Features
- **Right-click any deck** to change difficulty or delete
- **Regenerate decks** with different difficulty levels
- **Switch themes** anytime in Settings
- **Spaced repetition** automatically schedules review sessions

## 🛠️ Technical Details

### Built With
- **PyQt5** - Modern GUI framework
- **Google Gemini AI** - Advanced question generation
- **SQLite** - Local database storage
- **Python 3.8+** - Core application logic

### Project Structure
```
ZapCards/
├── main.py              # Application entry point
├── config.py            # Configuration and themes
├── themes.py            # Theme system (8 aesthetic options)
├── main_window.py       # Main application window
├── home_view.py         # Welcome/home page
├── settings_view.py     # Settings and theme selection
├── simple_deck_list_view.py  # Deck management interface
├── simple_quiz_view.py  # Quiz taking interface
├── web_question_finder.py    # AI question generation
├── simple_db.py         # Database operations
├── widgets.py           # Custom UI components
└── requirements.txt     # Python dependencies
```

## 🎓 Perfect For

- **Students** preparing for exams
- **Professionals** learning new skills
- **Language learners** practicing vocabulary
- **Trivia enthusiasts** testing knowledge
- **Teachers** creating study materials
- **Anyone** who wants to make learning fun!

## 🔧 Configuration

### API Setup
Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your-api-key-here
```

### Customization
- **Themes**: Modify `themes.py` to create custom color schemes
- **Difficulty**: Adjust question complexity in `web_question_finder.py`
- **Spaced Repetition**: Customize review intervals in `config.py`

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Ideas for Contributions
- New theme designs
- Additional AI providers
- Export/import functionality
- Mobile app version
- Study statistics dashboard

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful question generation
- **PyQt5** for the excellent GUI framework
- **The open-source community** for inspiration and support

## 📞 Support

Having issues? We're here to help!

- 🐛 **Bug Reports**: [Open an issue](https://github.com/yourusername/zapcards/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/yourusername/zapcards/discussions)
- 📧 **Email**: support@zapcards.app

---

**Made with ❤️ for learners everywhere**

*ZapCards - Where AI meets beautiful design to make learning irresistible!*
