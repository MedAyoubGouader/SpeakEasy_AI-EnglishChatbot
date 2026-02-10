<div align="center">

# 🎓 SpeakEasy AI — English Learning Chatbot

**An AI-powered web application for learning English through conversation, voice interaction, and intelligent tutoring.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange)](https://groq.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-green)](https://trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [RAG Pipeline](#-rag-pipeline)
- [Prompt Engineering](#-prompt-engineering)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🌟 Overview

**SpeakEasy AI** is a full-stack English learning platform that combines:

- A **conversational AI chatbot** powered by Llama 3.3 70B (via Groq API)
- A **RAG (Retrieval-Augmented Generation)** system for accurate, context-aware responses
- **Voice interaction** with speech-to-text and text-to-speech (multiple accents)
- A **modern web interface** with the "Ocean Blue" design system
- **User authentication** and conversation history persistence

The chatbot adapts to the user's English level (Beginner / Intermediate / Advanced) and covers grammar, vocabulary, pronunciation, conversation practice, IELTS/TOEFL prep, and more.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Chatbot** | Natural conversation with Llama 3.3 70B LLM, adapted to user level |
| 📚 **RAG System** | Retrieves relevant knowledge from 8+ data sources before answering |
| 🎙️ **Voice Input** | Speech-to-Text via Google Speech Recognition |
| 🔊 **Voice Output** | Text-to-Speech with 3 accents: 🇺🇸 US, 🇬🇧 UK, 🇦🇺 Australian |
| ✍️ **Grammar Correction** | Automatic detection and gentle correction of mistakes |
| 🔐 **Authentication** | User registration, login, and session persistence |
| 💬 **Chat History** | Conversations saved in SQLite, resumable anytime |
| 🎨 **Modern UI** | "Ocean Blue" responsive design with animated SVG assets |
| 📊 **Admin Panel** | Database viewer for managing users and conversations |
| 🧪 **Notebook Demo** | Jupyter Notebook showcasing RAG, embeddings, prompts, and LLM |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER (Browser)                            │
│              Streamlit Web Interface (Ocean Blue)                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Streamlit  │  │  Python      │  │  SQLite +    │           │
│  │  Frontend   │◄►│  Backend     │◄►│  ChromaDB    │           │
│  │  + CSS      │  │  Modules     │  │  Databases   │           │
│  └─────────────┘  └──────────────┘  └──────────────┘           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Groq API   │  │  Edge-TTS    │  │  Google STT  │           │
│  │  Llama 3.3  │  │  Microsoft   │  │  Speech      │           │
│  │  70B LLM    │  │  Neural TTS  │  │  Recognition │           │
│  └─────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### AI & Machine Learning

| Technology | Role |
|------------|------|
| **Groq API** | LLM inference — Llama 3.3 70B Versatile |
| **LangChain** | RAG pipeline orchestration & prompt management |
| **HuggingFace** | Sentence embeddings (`all-MiniLM-L6-v2`) |
| **ChromaDB** | Vector database for semantic search |

### Voice

| Technology | Role |
|------------|------|
| **Edge-TTS** | Text-to-Speech with natural Microsoft Neural Voices |
| **SpeechRecognition** | Speech-to-Text via Google Speech API |
| **audio-recorder-streamlit** | In-browser audio recording component |

### Web & Data

| Technology | Role |
|------------|------|
| **Streamlit** | Full-stack Python web framework |
| **SQLite** | User accounts & conversation history |
| **CSS (custom)** | "Ocean Blue" design system with animations |
| **SVG (custom)** | Animated illustrations and icons |

---

## 📁 Project Structure

```
📦 SpeakEasy_AI-EnglishChatbot/
│
├── 📄 voice_app.py                          # Main Streamlit application (~2000 lines)
├── 📓 ENGLISH_CHATBOT_IMPLEMENTATION.ipynb  # ⭐ Jupyter Notebook (RAG + LLM demo)
├── 📄 admin_view.py                         # Database admin viewer
├── 📄 requirements.txt                      # Python dependencies
├── 📄 start.bat / START_VOICE.bat           # Launch scripts (Windows)
│
├── 📁 modules/                              # Backend modules
│   ├── database.py                          #   SQLite operations (auth, history)
│   ├── chat_logic.py                        #   RAG retrieval + LLM logic
│   ├── correction.py                        #   Grammar correction engine
│   ├── voice.py                             #   TTS / STT functions
│   └── ui.py                                #   UI helper components
│
├── 📁 data/                                 # RAG knowledge base
│   ├── grammar/rules.txt                    #   English grammar rules (A1–C2)
│   ├── vocabulary/ENGLISH_CERF_WORDS.csv    #   3000+ CEFR-tagged words
│   ├── vocabulary/topics.txt                #   Thematic vocabulary
│   ├── pronunciation/ipa_guide.txt          #   IPA pronunciation guide
│   ├── conversation_scripts/dialogues.txt   #   Real-world dialogues
│   ├── listening_materials/transcripts.txt  #   Listening comprehension
│   ├── phrasal_verbs_idioms/comprehensive.txt  # Idioms & phrasal verbs
│   ├── exam_prep/ielts_toefl.txt            #   IELTS/TOEFL preparation
│   └── writing_guides/tips.txt              #   Writing tips & structures
│
├── 📁 english_learning_db/                  # Databases
│   ├── chroma.sqlite3                       #   ChromaDB vector store
│   └── users_chat.db                        #   Users & conversations (SQLite)
│
├── 📁 assets/                               # SVG illustrations & icons
│   ├── logo_animated.svg
│   ├── robot_animated.svg
│   ├── hero_animated.svg
│   └── icon_*_animated.svg                  #   Feature icons
│
├── 📁 tests/                                # Test suite
│   ├── test_chatbot.py                      #   Full chatbot tests
│   └── test_chatbot_quick.py                #   Quick smoke tests
│
└── 📁 docs/                                 # Project documentation
    ├── DOCUMENTATION_TECHNIQUE.md
    ├── PRESENTATION_PROJET.md
    └── STRUCTURE_FICHIERS.md
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+**
- **Git**
- A **Groq API key** (free at [console.groq.com](https://console.groq.com))

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/MedAyoubGouader/SpeakEasy_AI-EnglishChatbot.git
cd SpeakEasy_AI-EnglishChatbot

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Groq API key
# Windows (CMD)
set GROQ_API_KEY=your_groq_api_key_here
# Windows (PowerShell)
$env:GROQ_API_KEY="your_groq_api_key_here"
# macOS/Linux
export GROQ_API_KEY="your_groq_api_key_here"

# 5. Run the application
streamlit run voice_app.py --theme.base="light"
```

The app opens at **http://localhost:8501**.

---

## 🖥️ Usage

### Quick Start (Windows)

Double-click `start.bat` or `START_VOICE.bat` (after setting your API key inside the file).

### Application Pages

| Page | URL | Description |
|------|-----|-------------|
| **Landing** | `localhost:8501` | Welcome page with features overview |
| **Login** | `?page=login` | User authentication |
| **Sign Up** | `?page=signup` | New account registration |
| **Chat** | `?page=chat` | AI chatbot interface with voice |

### Chat Features

1. **Text input** — Type your English question or practice message
2. **Voice input** — Click the 🎙️ mic button to speak
3. **Voice output** — Listen to AI responses in US, UK, or Australian accent
4. **Grammar correction** — Toggle automatic correction in settings
5. **Level selection** — Choose Beginner / Intermediate / Advanced
6. **Conversation history** — Switch between saved conversations in the sidebar

### Admin Panel

```bash
streamlit run admin_view.py --server.port 8502
```
Opens a database viewer at `http://localhost:8502` to inspect users, conversations, and messages.

---

## 🔍 RAG Pipeline

The Retrieval-Augmented Generation pipeline ensures accurate, knowledge-grounded responses:

```
User Question
     │
     ▼
┌─────────────────┐
│ Query Embedding  │  → HuggingFace all-MiniLM-L6-v2
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ChromaDB        │  → Semantic similarity search
│  Vector Search   │     across 8 data collections
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Context Assembly │  → Top-k relevant documents
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Generation  │  → Groq Llama 3.3 70B
│  with Context    │     System prompt + RAG context + user query
└─────────────────┘
```

### Data Sources

| Collection | File | Content |
|------------|------|---------|
| Grammar | `rules.txt` | Complete English grammar rules (CEFR A1–C2) |
| Vocabulary | `ENGLISH_CERF_WORDS.csv` | 3000+ words tagged by CEFR level |
| Pronunciation | `ipa_guide.txt` | IPA symbols and pronunciation patterns |
| Dialogues | `dialogues.txt` | Real-world conversation scripts |
| Idioms | `comprehensive.txt` | Phrasal verbs and idiomatic expressions |
| Listening | `transcripts.txt` | Listening comprehension materials |
| Exam Prep | `ielts_toefl.txt` | IELTS/TOEFL tips and practice |
| Writing | `tips.txt` | Academic and general writing guides |

---

## 🧠 Prompt Engineering

The system uses a **three-layer prompt hierarchy**:

1. **System Prompt** — Defines the AI tutor persona, user level, and RAG context
2. **Category Prompt** — Specialized instructions per topic (grammar, vocabulary, pronunciation, conversation)
3. **User Message** — The actual question + last 10 messages for context

### Automatic Query Classification

User queries are automatically classified into categories using keyword matching:

- **Grammar** → tense, verb, noun, article, preposition...
- **Vocabulary** → word, meaning, synonym, definition...
- **Pronunciation** → pronounce, sound, accent, IPA...
- **Conversation** → dialogue, expression, how to say...

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [DOCUMENTATION_TECHNIQUE.md](DOCUMENTATION_TECHNIQUE.md) | Full technical documentation |
| [PRESENTATION_PROJET.md](PRESENTATION_PROJET.md) | Project presentation (French) |
| [STRUCTURE_FICHIERS.md](STRUCTURE_FICHIERS.md) | File structure explanation |
| [ENGLISH_CHATBOT_IMPLEMENTATION.ipynb](ENGLISH_CHATBOT_IMPLEMENTATION.ipynb) | Interactive notebook demo |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👤 Author

**Mohamed Ayoub Gouader**

- GitHub: [@MedAyoubGouader](https://github.com/MedAyoubGouader)
- Email: doubaay12@gmail.com

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ If you find this project useful, please give it a star! ⭐**

*Built with Python, Streamlit, Groq, LangChain, and ChromaDB*

</div>