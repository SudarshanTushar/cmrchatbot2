# 🎯 Collective Quiz Bot - Ultimate Telegram Quiz Experience

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-blue.svg)](https://core.telegram.org/bots/api)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-green.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **🌟 The Ultimate Group Quiz Experience with Interactive Polls & Real-time Leaderboards! 🌟**

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Installation](#️-installation)
- [🔧 Configuration](#-configuration)
- [📱 Commands Reference](#-commands-reference)
- [🎮 How to Use](#-how-to-use)
- [📊 Question Formats](#-question-formats)
- [🏗️ Project Structure](#️-project-structure)
- [🛠️ Development](#️-development)
- [📝 License](#-license)

## ✨ Features

### 🎮 Core Features
- **Interactive Quiz Polls** - Telegram's native quiz polls with instant feedback
- **Real-time Leaderboards** - Live scoring and participant rankings
- **Multiplayer Group Competitions** - Everyone answers the same questions together
- **Multiple Question Formats** - Flexible question parsing and validation
- **Admin Controls** - Group admin permissions for quiz management
- **Progress Tracking** - Detailed statistics and performance analytics

### 🔧 Advanced Features
- **Question Set Management** - Create, update, and delete quiz sets
- **Customizable Timing** - Set delays between questions
- **Personal Reports** - Individual performance tracking with `/myanswer`
- **Bulk Question Upload** - Add multiple questions at once
- **Auto-feedback System** - Instant correct/wrong indicators
- **Database Persistence** - MongoDB storage for all quiz data

### 🤖 AI Assistant Features
- **Intelligent Q&A** - Ask questions and get detailed explanations
- **Creative Content** - Generate poems, stories, translations
- **Quiz Generation** - Auto-generate questions from study material
- **Context Awareness** - Reply to messages with relevant context
- **Multi-language Support** - Respond in user's preferred language
- **Educational Focus** - Optimized for learning and teaching

### 👥 User Roles
- **👑 Owner** - Full bot control and management
- **🔧 Sudo Users** - Question set creation and management
- **👮 Group Admins** - Quiz control in their groups
- **👤 Regular Users** - Quiz participation and personal stats

## 🚀 Quick Start

1. **Add Bot to Group** - Invite the bot to your Telegram group
2. **Make Admin** - Give bot admin permissions in the group
3. **Check Available Sets** - Use `/sets` to see quiz options
4. **Start Quiz** - Use `/quiz set_name` to begin
5. **Answer Together** - Everyone participates in the same quiz polls!

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB database (local or Atlas)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)
- Gemini AI API Key from [Google AI Studio](https://makersuite.google.com/app/apikey) (Optional - for AI features)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/quiz-bot.git
   cd quiz-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Edit `config.py` with your credentials
   - Set up MongoDB connection
   - Configure bot settings

4. **Run the Bot**
   ```bash
   python bot.py
   ```

## 🔧 Configuration

### Edit `config.py`:

```python
# Telegram Bot Configuration
API_ID = your_api_id  # From https://my.telegram.org
API_HASH = "your_api_hash"  # From https://my.telegram.org
BOT_TOKEN = "your_bot_token"  # From @BotFather

# MongoDB Configuration
MONGO_URI = "your_mongodb_uri"  # MongoDB connection string

# Bot Owner Configuration
OWNER_ID = your_user_id  # Your Telegram user ID
SUDO_USERS = [user_id_1, user_id_2]  # Authorized quiz creators

# Main Quiz Management Group
MAIN_QUIZ_GROUP_ID = -your_group_id  # Group for creating quiz sets

# Gemini AI Configuration (Optional - for AI features)
GEMINI_API_KEY = "your_gemini_api_key"  # From https://makersuite.google.com/app/apikey
```

### Deploy to Heroku:

1. **Create Heroku App**
   ```bash
   heroku create your-quiz-bot
   ```

2. **Set Config Variables**
   ```bash
   heroku config:set API_ID=your_api_id
   heroku config:set API_HASH=your_api_hash
   heroku config:set BOT_TOKEN=your_bot_token
   heroku config:set MONGO_URI=your_mongodb_uri
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

## 📱 Commands Reference

### 👥 Group Commands (Admin Only)

| Command | Description | Usage Example |
|---------|-------------|---------------|
| `/quiz <set_name>` | Start collective group quiz | `/quiz math_basics` |
| `/endquiz` | End active group quiz | `/endquiz` |
| `/time <seconds>` | Set question delay timing | `/time 15` |
| `/sets` | List available quiz sets | `/sets` |
| `/cancel` | Cancel active quiz/creation | `/cancel` |

### 🔧 Admin Commands (Sudo Users Only)

| Command | Description | Usage Example | Location |
|---------|-------------|---------------|----------|
| `/new <set_name>` | Create new question set | `/new science_quiz` | Main group only |
| `/add <set_name>` | Add questions to existing set | `/add math_basics` | Main group only |
| `/save` | Save uploaded questions | `/save` | Main group only |
| `/list` | List all question sets | `/list` | Main group only |
| `/delete <set_name>` | Delete entire question set | `/delete old_quiz` | Main group only |
| `/qdelete` or `/qdlt` | Delete specific questions | `/qdelete` | Main group only |
| `/update` | Update existing questions | `/update` | Main group only |
| `/download <set_name>` | Download question set | `/download math_quiz` | Main group only |

### 👤 User Commands

| Command | Description | Usage Example |
|---------|-------------|---------------|
| `/start` | Show welcome message and help | `/start` |
| `/myanswer [set_name]` | View personal quiz report | `/myanswer math_basics` |

### 🧪 Debug Commands

| Command | Description | Usage Example |
|---------|-------------|---------------|
| `/testleaderboard` | Test leaderboard functionality | `/testleaderboard` |

### 🤖 AI Assistant Commands (Owner & Sudo Users Only)

| Command | Description | Usage Example |
|---------|-------------|---------------|
| `/ask <question>` | AI assistant for questions & creative requests | `/ask What is photosynthesis?` |
| `/generate <count> <difficulty> <material>` | Generate quiz from study material | `/generate 5 medium Photosynthesis is...` |
| `/aistatus` | Check AI assistant status | `/aistatus` |

## 🎮 How to Use

### For Group Admins:

1. **Setup**
   - Add bot to your group
   - Make bot admin
   - Check available quiz sets with `/sets`

2. **Start Quiz**
   ```
   /quiz math_basics
   ```

3. **Customize Settings**
   ```
   /time 10  # Set 10-second delays
   ```

4. **End Quiz**
   ```
   /endquiz
   ```

### For Quiz Creators (Sudo Users):

1. **Create New Set**
   ```
   /new science_quiz
   ```

2. **Add Questions** (Multiple formats supported)
   ```
   Q) What is 2+2? A. Two B. Four C. Six D. Eight Answer: B. Four
   
   Q: What is H2O? || A) Hydrogen || B) Water || C) Oxygen || D) Carbon || Answer: B
   ```

3. **Save Questions**
   ```
   /save
   ```

### For Participants:

1. **Answer Questions**
   - Click on quiz poll options
   - Get instant feedback (✅/❌)
   - See poll statistics in real-time

2. **Check Personal Stats**
   ```
   /myanswer math_basics
   ```

### For AI Assistant Users (Owner & Sudo Users):

1. **Ask Questions & Get Help**
   ```
   /ask What is the theory of relativity?
   /ask Write a poem about programming
   /ask Translate "Hello World" to French
   /ask How to sort an array in Python?
   ```

2. **Generate Quiz Questions from Study Material**
   ```
   /generate 5 medium Photosynthesis is the process by which plants convert light energy into chemical energy using chlorophyll...
   ```

3. **Check AI Status**
   ```
   /aistatus
   ```

## 📊 Question Formats

The bot supports two flexible question formats:

### Format 1: Traditional Style
```
Q) What is the capital of France?
A. London B. Berlin C. Paris D. Madrid
Answer: C. Paris
```

### Format 2: Pipe-Separated Style
```
Q: What is 2+2? || A) Two || B) Four || C) Six || D) Eight || Answer: B
```

### Multiple Questions in One Message
```
Q) Question 1? A. Opt1 B. Opt2 C. Opt3 D. Opt4 Answer: A

Q) Question 2? A. Opt1 B. Opt2 C. Opt3 D. Opt4 Answer: B
```

### Validation Rules:
- ✅ Questions must start with `Q)` or `Q:`
- ✅ Must have 4 options (A, B, C, D)
- ✅ Answer must be specified with correct letter
- ✅ Flexible spacing and formatting
- ✅ Supports both period and parenthesis option markers

## 🏗️ Project Structure

```
quiz-bot/
├── bot.py                 # Main bot entry point
├── config.py              # Configuration settings
├── handlers.py            # Command and message handlers
├── db.py                 # Database operations
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment
├── runtime.txt          # Python version specification
└── polls/               # Quiz poll functionality
    ├── __init__.py
    ├── questions.py     # Question sending logic
    ├── answers.py       # Answer handling logic
    ├── leaderboard.py   # Leaderboard management
    └── myanswers.py     # Personal statistics
```

### Key Components:

- **`bot.py`** - Application entry point and client setup
- **`handlers.py`** - All command handlers and message processing
- **`db.py`** - MongoDB operations and data management  
- **`utils.py`** - Question parsing and validation utilities
- **`polls/`** - Modular quiz poll system with specialized handlers

## 🛠️ Development

### Dependencies

```python
# Core Framework
pyrogram>=2.0.0      # Telegram MTProto client
tgcrypto>=1.2.5      # Encryption for Pyrogram

# Database
pymongo>=4.0.0       # MongoDB driver
motor>=3.0.0         # Async MongoDB driver  
dnspython>=2.0.0     # DNS resolution for MongoDB
```

### Database Schema

**Collections:**
- `question_sets` - Quiz question storage
- `user_sessions` - Active quiz sessions  
- `quiz_results` - Historical results and statistics

### Key Features Implementation:

- **Quiz Polls** - Using Telegram's native poll API for better UX
- **Real-time Updates** - Async handlers for immediate response
- **Session Management** - In-memory and database session tracking
- **Permission System** - Role-based access control
- **Error Handling** - Comprehensive error management and logging

### Local Development:

1. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

2. **Configure Development Settings**
   - Use local MongoDB or MongoDB Atlas free tier
   - Create test bot with @BotFather
   - Set up development group for testing

3. **Run in Development Mode**
   ```bash
   python bot.py
   ```

### Contributing:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 🔒 Security Features

- **Permission Validation** - Admin and sudo user verification
- **Group Restrictions** - Main group only for question management
- **Input Sanitization** - Question format validation and parsing
- **Session Management** - Secure session handling and cleanup
- **Rate Limiting** - Built-in protection against spam

## 📈 Performance

- **Async Operations** - Non-blocking I/O for better performance
- **In-Memory Caching** - Session and settings caching
- **Efficient Database Queries** - Optimized MongoDB operations
- **Modular Architecture** - Separated concerns for better maintainability

## 🐛 Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Check MongoDB URI in config.py
   - Verify network connectivity
   - Ensure database permissions

2. **Bot Not Responding**
   - Verify bot token is correct
   - Check API_ID and API_HASH
   - Ensure bot has admin permissions in groups

3. **Commands Not Working**
   - Confirm user has required permissions
   - Check if command is used in correct group type
   - Verify bot is added to the group

### Debug Mode:
Enable logging in `bot.py` for detailed error information:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

- **Developer**: [@Forever_Crush](https://t.me/Forever_Crush)
- **Version**: 2.0 (Quiz Poll Edition)
- **Support**: Contact through the group where bot is added
- **Issues**: [GitHub Issues](https://github.com/Radhaapi/Quizz/issues)

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and feel free to submit pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**💝 Made with love for quiz enthusiasts! 🎯**
