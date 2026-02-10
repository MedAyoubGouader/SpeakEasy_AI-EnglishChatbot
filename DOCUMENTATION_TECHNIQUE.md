# SpeakEasy AI - Documentation Technique Complète

## Table des Matières

1. [Présentation du Projet](#1-présentation-du-projet)
2. [Architecture Technique](#2-architecture-technique)
3. [Technologies et Dépendances](#3-technologies-et-dépendances)
4. [Structure du Projet](#4-structure-du-projet)
5. [RAG et Base de Données Vectorielle](#5-rag-et-base-de-données-vectorielle)
6. [Prompt Engineering](#6-prompt-engineering)
7. [Système d'Authentification](#7-système-dauthentification)
8. [Interface Utilisateur](#8-interface-utilisateur)
9. [Fonctionnalités Vocales](#9-fonctionnalités-vocales)
10. [Installation et Déploiement](#10-installation-et-déploiement)
11. [Guide d'Utilisation](#11-guide-dutilisation)

---

## 1. Présentation du Projet

### 1.1 Description

**SpeakEasy AI** est une plateforme web intelligente d'apprentissage de l'anglais combinant:
- Chatbot IA conversationnel avec LLM (Llama 3.3 70B via Groq)
- Reconnaissance vocale (Speech-to-Text)
- Synthèse vocale naturelle (Text-to-Speech via Edge-TTS)
- Système RAG (Retrieval-Augmented Generation) avec ChromaDB
- Authentification utilisateur avec persistance de session
- Interface moderne "Ocean Blue" responsive

### 1.2 Objectifs Pédagogiques

| Objectif | Implementation |
|----------|----------------|
| Pratique conversationnelle | Chat IA adaptatif selon le niveau |
| Correction grammaticale | Analyse et suggestions en temps réel |
| Vocabulaire | Base de données CEFR (A1-C2) |
| Pronunciation | TTS multi-accents (US, UK, Australian) |
| Compréhension orale | STT + feedback vocal |

### 1.3 Public Cible

- Étudiants apprenant l'anglais (niveaux A1-C2)
- Professionnels souhaitant améliorer leur anglais
- Autodidactes cherchant une pratique interactive

---

## 2. Architecture Technique

### 2.1 Diagramme d'Architecture Général

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Streamlit)                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │  Landing Page   │  │  Auth Pages     │  │  Chat Interface │         │
│  │  - Hero Section │  │  - Login        │  │  - Messages     │         │
│  │  - Features     │  │  - Signup       │  │  - Voice Input  │         │
│  │  - CTA          │  │  - Session      │  │  - Sidebar      │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
└───────────┼────────────────────┼────────────────────┼───────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          BACKEND MODULES                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  database   │  │ chat_logic  │  │ correction  │  │   voice     │    │
│  │  - SQLite   │  │ - RAG       │  │ - Grammar   │  │ - STT/TTS   │    │
│  │  - Users    │  │ - Prompts   │  │ - Analysis  │  │ - Edge-TTS  │    │
│  │  - History  │  │ - Context   │  │ - Feedback  │  │ - Google SR │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
└─────────┼────────────────┼────────────────┼────────────────┼────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SERVICES                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Groq API   │  │  ChromaDB   │  │  Edge-TTS   │  │ Google STT  │    │
│  │  (LLM)      │  │  (Vectors)  │  │  (Voices)   │  │  (Speech)   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Flux de Données

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User    │────▶│  Input       │────▶│  Processing  │────▶│  Output      │
│  Action  │     │  (Text/Voice)│     │  (RAG + LLM) │     │  (Text/Voice)│
└──────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                        │                    │                    │
                        ▼                    ▼                    ▼
                 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
                 │ STT (if voice)│    │ ChromaDB     │     │ TTS (auto)   │
                 │ Google API   │     │ Context      │     │ Edge-TTS     │
                 └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 3. Technologies et Dépendances

### 3.1 Stack Technologique

| Catégorie | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Framework Web** | Streamlit | 1.28+ | Interface utilisateur |
| **LLM** | Groq API | - | Llama 3.3 70B pour réponses IA |
| **Embeddings** | HuggingFace | - | sentence-transformers/all-MiniLM-L6-v2 |
| **Vector DB** | ChromaDB | 0.4+ | Stockage et recherche sémantique |
| **TTS** | Edge-TTS | 6.1+ | Synthèse vocale Microsoft |
| **STT** | SpeechRecognition | 3.10+ | Reconnaissance vocale Google |
| **Database** | SQLite | 3 | Utilisateurs et historique |
| **LangChain** | langchain | 0.1+ | Orchestration RAG |

### 3.2 Dépendances (requirements.txt)

```
streamlit>=1.28.0
groq>=0.4.0
langchain>=0.1.0
langchain-groq>=0.0.1
langchain-huggingface>=0.0.1
langchain-community>=0.0.1
chromadb>=0.4.0
sentence-transformers>=2.2.0
edge-tts>=6.1.0
SpeechRecognition>=3.10.0
audio-recorder-streamlit>=0.0.8
gTTS>=2.3.0
pandas>=2.0.0
python-dotenv>=1.0.0
```

---

## 4. Structure du Projet

### 4.1 Arborescence Complète

```
english-chatbot/
│
├── 📄 voice_app.py              # Application principale Streamlit (2000+ lignes)
├── 📓 ENGLISH_CHATBOT_IMPLEMENTATION.ipynb  # Notebook démonstration RAG/Prompts
├── 📄 requirements.txt          # Dépendances Python
├── 📄 start.bat                 # Script démarrage Windows
├── 📄 START_VOICE.bat           # Script démarrage avec clé API
│
├── 📁 modules/                  # Modules Python backend
│   ├── __init__.py
│   ├── database.py              # Gestion SQLite (users, conversations)
│   ├── chat_logic.py            # Logique RAG et prompts
│   ├── correction.py            # Analyse grammaticale
│   ├── voice.py                 # Fonctions STT/TTS
│   └── ui.py                    # Composants UI réutilisables
│
├── 📁 data/                     # Données pour RAG
│   ├── grammar/
│   │   └── rules.txt            # Règles grammaticales anglaises
│   ├── vocabulary/
│   │   ├── topics.txt           # Vocabulaire thématique
│   │   └── ENGLISH_CERF_WORDS.csv  # Mots CEFR A1-C2
│   ├── pronunciation/
│   │   └── ipa_guide.txt        # Guide prononciation IPA
│   ├── conversation_scripts/
│   │   └── dialogues.txt        # Exemples de dialogues
│   ├── phrasal_verbs_idioms/
│   │   └── comprehensive.txt    # Phrasal verbs et idiomes
│   ├── exam_prep/
│   │   └── ielts_toefl.txt      # Préparation examens
│   ├── listening_materials/
│   │   └── transcripts.txt      # Transcriptions audio
│   └── writing_guides/
│       └── tips.txt             # Conseils rédaction
│
├── 📁 english_learning_db/      # Bases de données
│   ├── chroma.sqlite3           # ChromaDB (vecteurs)
│   └── users_chat.db            # SQLite (utilisateurs)
│
├── 📁 assets/                   # Ressources visuelles SVG
│   ├── logo_animated.svg        # Logo animé SpeakEasy
│   ├── robot_animated.svg       # Mascotte robot
│   ├── hero_animated.svg        # Illustration hero
│   ├── icon_grammar_animated.svg
│   ├── icon_speaking_animated.svg
│   ├── icon_vocabulary_animated.svg
│   ├── icon_listening_animated.svg
│   ├── mic_animated.svg         # Icône microphone
│   └── ... (autres SVG)
│
├── 📁 tests/                    # Tests unitaires
│   ├── test_chatbot.py
│   ├── test_chatbot_quick.py
│   └── test_results.json
│
└── 📁 venv/                     # Environnement virtuel Python
```

### 4.2 Description des Fichiers Principaux

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `voice_app.py` | ~2000 | Application Streamlit complète avec CSS, pages, chat |
| `ENGLISH_CHATBOT_IMPLEMENTATION.ipynb` | ~560 | Notebook Jupyter démontrant RAG et prompt engineering |
| `modules/database.py` | ~160 | Gestion base de données SQLite |
| `modules/chat_logic.py` | ~200 | Logique conversationnelle et RAG |
| `voice_engine.py` | ~300 | Moteur vocal (legacy, fonctions intégrées dans voice_app.py) |

---

## 5. RAG et Base de Données Vectorielle

### 5.1 Concept RAG (Retrieval-Augmented Generation)

Le système RAG permet d'enrichir les réponses du LLM avec du contenu spécifique à l'apprentissage de l'anglais:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ User Query  │────▶│  Embedding  │────▶│  ChromaDB   │────▶│  Context    │
│             │     │  (MiniLM)   │     │  Search     │     │  Retrieved  │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                    │
                                                                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────────────────────────┐
│  Response   │◀────│   LLM       │◀────│  System Prompt + Context        │
│             │     │  (Llama 3)  │     │  + User Query + Category Prompt │
└─────────────┘     └─────────────┘     └─────────────────────────────────┘
```

### 5.2 Implementation ChromaDB

```python
# Initialisation des embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# Création/Chargement de ChromaDB
vectordb = Chroma(
    persist_directory="english_learning_db",
    embedding_function=embeddings
)

# Recherche sémantique
def retrieve_context(query, k=3):
    results = vectordb.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])
```

### 5.3 Données Indexées

| Catégorie | Fichier | Contenu |
|-----------|---------|---------|
| Grammar | `rules.txt` | Règles grammaticales (tenses, articles, etc.) |
| Vocabulary | `topics.txt`, `ENGLISH_CERF_WORDS.csv` | 5000+ mots CEFR |
| Pronunciation | `ipa_guide.txt` | Guide IPA et conseils |
| Conversations | `dialogues.txt` | Exemples de dialogues |
| Idioms | `comprehensive.txt` | Phrasal verbs et expressions |

---

## 6. Prompt Engineering

### 6.1 Structure des Prompts

Le système utilise une hiérarchie de prompts:

```
┌─────────────────────────────────────────────────────────────┐
│                     SYSTEM PROMPT                            │
│  - Rôle: Expert English tutor                               │
│  - Niveau utilisateur: {level}                              │
│  - Contexte RAG: {retrieved_context}                        │
│  - Instructions générales                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   CATEGORY PROMPT                            │
│  - grammar: Focus sur les règles                            │
│  - vocabulary: Définitions et exemples                      │
│  - pronunciation: Guide prononciation                       │
│  - conversation: Expressions naturelles                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    USER MESSAGE                              │
│  + Historique conversation (10 derniers messages)           │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Exemples de Prompts

**System Prompt Principal:**
```
You are an expert English tutor. Your role is to help users learn English effectively.

User's level: {level}

When responding:
1. Be friendly, encouraging, and patient
2. Explain concepts clearly with examples
3. Correct grammar mistakes gently:
   📝 **Correction:** [what was wrong]
   ✅ **Better:** [corrected version]
   💡 **Tip:** [brief explanation]
4. Ask follow-up questions to encourage practice
5. Use the context provided when relevant

Context from knowledge base:
{context}
```

**Category Prompt (Grammar):**
```
Focus on grammar rules. Explain:
1. The grammatical structure
2. When to use it
3. Common mistakes to avoid
4. 2-3 example sentences
```

### 6.3 Classification des Requêtes

```python
def classify_query(query):
    query_lower = query.lower()
    
    grammar_keywords = ['tense', 'verb', 'noun', 'grammar', ...]
    vocab_keywords = ['word', 'meaning', 'vocabulary', ...]
    pronunciation_keywords = ['pronounce', 'sound', 'accent', ...]
    conversation_keywords = ['conversation', 'dialogue', 'expression', ...]
    
    if any(kw in query_lower for kw in grammar_keywords):
        return 'grammar'
    # ... etc
```

---

## 7. Système d'Authentification

### 7.1 Base de Données Utilisateurs

```sql
-- Table users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table conversations
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table messages
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    role TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

### 7.2 Persistance de Session

La session utilisateur est persistée via les query params de Streamlit:

```python
# Sauvegarde session après login
st.query_params["user_id"] = str(user['id'])
st.query_params["username"] = user['username']

# Restauration session au refresh
def restore_session():
    params = st.query_params
    if "user_id" in params and "username" in params:
        # Restaurer l'utilisateur
        st.session_state.auth_status = True
        st.session_state.user = {"id": user_id, "username": username}
```

---

## 8. Interface Utilisateur

### 8.1 Design System "Ocean Blue"

```css
:root {
    --primary-blue: #2563EB;
    --primary-blue-hover: #1D4ED8;
    --primary-blue-light: #DBEAFE;
    --accent-green: #10B981;
    --bg-white: #FFFFFF;
    --bg-cream: #F8FAFC;
    --text-dark: #1E293B;
    --text-light: #64748B;
}
```

### 8.2 Pages de l'Application

| Page | Route | Description |
|------|-------|-------------|
| Landing | `/` | Page d'accueil avec hero, features, CTA |
| Login | `?page=login` | Formulaire de connexion |
| Signup | `?page=signup` | Formulaire d'inscription |
| Chat | `?page=chat` | Interface de chat principale |

### 8.3 Composants SVG Animés

Tous les assets sont des SVG animés custom:
- `logo_animated.svg` - Logo avec effet de respiration
- `robot_animated.svg` - Mascotte avec animation
- `icon_*_animated.svg` - Icônes de fonctionnalités

---

## 9. Fonctionnalités Vocales

### 9.1 Speech-to-Text (STT)

```python
# Utilisation de Google Speech Recognition
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300

with sr.AudioFile(audio_path) as source:
    audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language='en-US')
```

### 9.2 Text-to-Speech (TTS)

```python
# Utilisation de Edge-TTS (voix Microsoft naturelles)
voice_map = {
    "US": "en-US-AriaNeural",
    "UK": "en-GB-SoniaNeural",
    "Australian": "en-AU-NatashaNeural"
}

async def generate_speech(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
```

---

## 10. Installation et Déploiement

### 10.1 Installation Locale

```bash
# 1. Cloner le projet
git clone <repository>
cd english-chatbot

# 2. Créer environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configurer API Key
set GROQ_API_KEY=your_api_key

# 5. Lancer l'application
streamlit run voice_app.py --theme.base="light"
```

### 10.2 Script de Démarrage (START_VOICE.bat)

```batch
@echo off
set GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
call venv\Scripts\activate
streamlit run voice_app.py --theme.base="light"
pause
```

---

## 11. Guide d'Utilisation

### 11.1 Pour les Utilisateurs

1. **Page d'accueil**: Découvrir les fonctionnalités
2. **Créer un compte**: Remplir le formulaire d'inscription
3. **Se connecter**: Entrer identifiants
4. **Chatter**: Poser des questions en anglais
5. **Voix**: Cliquer sur le micro pour parler
6. **Paramètres**: Ajuster niveau et accent dans la sidebar

### 11.2 Pour les Développeurs

- **Modifier les prompts**: Éditer `voice_app.py` section `get_ai_response()`
- **Ajouter des données RAG**: Placer fichiers .txt dans `data/`
- **Personnaliser l'UI**: Modifier le CSS dans `voice_app.py`
- **Tester**: Exécuter les notebooks et tests

### 11.3 Pour le Professeur (Notebook)

Le fichier `ENGLISH_CHATBOT_IMPLEMENTATION.ipynb` démontre:
1. Configuration des API
2. Initialisation du LLM (Groq)
3. Embeddings HuggingFace
4. Création ChromaDB
5. Fonction de retrieval
6. Prompt engineering
7. Classification des requêtes
8. Chat engine complet
9. Text-to-Speech
10. Classe exportable

---

## Conclusion

SpeakEasy AI est une application complète d'apprentissage de l'anglais utilisant les technologies modernes d'IA:
- **RAG** pour des réponses contextuelles précises
- **Prompt Engineering** pour des interactions naturelles
- **Voice AI** pour la pratique orale
- **Design moderne** pour une expérience utilisateur optimale

L'architecture modulaire permet une extension facile des fonctionnalités.
