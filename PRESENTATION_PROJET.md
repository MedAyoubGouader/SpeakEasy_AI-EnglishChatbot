# SpeakEasy AI - Présentation du Projet

---

## 🎯 Informations Générales

| Élément | Détail |
|---------|--------|
| **Nom du Projet** | SpeakEasy AI - English Learning Chatbot |
| **Type** | Application Web d'Apprentissage de l'Anglais |
| **Technologies** | Python, Streamlit, LLM (Groq), RAG, ChromaDB |
| **Auteur** | [Votre Nom] |
| **Date** | Janvier 2026 |

---

## 📋 Résumé Exécutif

**SpeakEasy AI** est une plateforme web intelligente d'apprentissage de l'anglais qui combine l'intelligence artificielle conversationnelle avec des fonctionnalités vocales avancées. L'application utilise le modèle Llama 3.3 70B via l'API Groq, enrichi par un système RAG (Retrieval-Augmented Generation) pour fournir des réponses contextuelles et pédagogiques.

### Points Clés du Projet

- ✅ **Chatbot IA conversationnel** adapté au niveau de l'utilisateur
- ✅ **Système RAG** avec ChromaDB pour des réponses précises
- ✅ **Prompt Engineering** avancé avec classification des requêtes
- ✅ **Reconnaissance vocale** (Speech-to-Text)
- ✅ **Synthèse vocale** multi-accents (Text-to-Speech)
- ✅ **Authentification** avec persistance de session
- ✅ **Interface moderne** responsive "Ocean Blue"

---

## 🏗️ Architecture du Projet

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        UTILISATEUR                               │
│            (Navigateur Web - Interface Streamlit)                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION WEB                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Frontend  │  │   Backend   │  │  Database   │             │
│  │  Streamlit  │◀▶│   Python    │◀▶│   SQLite    │             │
│  │  + CSS      │  │  Modules    │  │  + ChromaDB │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICES EXTERNES                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Groq API  │  │  Edge-TTS   │  │ Google STT  │             │
│  │ Llama 3.3   │  │  Microsoft  │  │  Speech     │             │
│  │    70B      │  │   Voices    │  │ Recognition │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies Utilisées

### Intelligence Artificielle

| Technologie | Utilisation |
|-------------|-------------|
| **Groq API** | Accès au LLM Llama 3.3 70B pour les réponses conversationnelles |
| **LangChain** | Orchestration du pipeline RAG et gestion des prompts |
| **HuggingFace** | Modèle d'embeddings `all-MiniLM-L6-v2` pour la vectorisation |
| **ChromaDB** | Base de données vectorielle pour le stockage et la recherche sémantique |

### Fonctionnalités Vocales

| Technologie | Utilisation |
|-------------|-------------|
| **Edge-TTS** | Synthèse vocale avec voix naturelles Microsoft (US, UK, Australian) |
| **SpeechRecognition** | Reconnaissance vocale via Google Speech API |
| **audio-recorder-streamlit** | Composant d'enregistrement audio dans Streamlit |

### Interface et Backend

| Technologie | Utilisation |
|-------------|-------------|
| **Streamlit** | Framework web Python pour l'interface utilisateur |
| **SQLite** | Base de données pour utilisateurs et historique des conversations |
| **CSS Custom** | Design system "Ocean Blue" avec animations |

---

## 📁 Structure des Fichiers

### Fichiers Principaux

```
📦 english-chatbot/
│
├── 📄 voice_app.py                          # Application Streamlit principale
│   └── (2000+ lignes) - UI, CSS, logique complète
│
├── 📓 ENGLISH_CHATBOT_IMPLEMENTATION.ipynb  # ⭐ NOTEBOOK IMPORTANT
│   └── Démonstration complète: RAG, Prompts, LLM, TTS
│
├── 📄 requirements.txt                      # Dépendances Python
├── 📄 start.bat / START_VOICE.bat           # Scripts de lancement
│
├── 📁 modules/                              # Modules backend
│   ├── database.py      # Gestion SQLite
│   ├── chat_logic.py    # Logique RAG
│   ├── correction.py    # Analyse grammaticale
│   └── voice.py         # Fonctions vocales
│
├── 📁 data/                                 # Données RAG
│   ├── grammar/         # Règles grammaticales
│   ├── vocabulary/      # Vocabulaire CEFR
│   ├── pronunciation/   # Guide IPA
│   └── ...              # Autres ressources
│
├── 📁 english_learning_db/                  # Bases de données
│   ├── chroma.sqlite3   # Vecteurs ChromaDB
│   └── users_chat.db    # Utilisateurs SQLite
│
└── 📁 assets/                               # SVG animés
    ├── logo_animated.svg
    ├── robot_animated.svg
    └── ...
```

### Fichiers Non Utilisés (Legacy)

| Fichier | Statut | Raison |
|---------|--------|--------|
| `voice_app_legacy.py` | ❌ Non utilisé | Ancienne version sans authentification |
| `voice_engine.py` | ⚠️ Legacy | Fonctions intégrées dans voice_app.py |
| `admin_view.py` | 🔧 Utilitaire | Outil admin pour visualiser la BDD |

---

## 🔍 Fonctionnalités Détaillées

### 1. Système RAG (Retrieval-Augmented Generation)

Le cœur intelligent de l'application:

```
Question Utilisateur
        │
        ▼
┌───────────────────┐
│   Vectorisation   │ ← HuggingFace Embeddings
│   de la question  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Recherche dans   │ ← ChromaDB
│    ChromaDB       │   (Similarity Search)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Contexte Pertinent│
│   (3 documents)   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  System Prompt +  │
│  Context + Query  │ ← Prompt Engineering
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│     LLM Groq      │ ← Llama 3.3 70B
│   (Génération)    │
└─────────┬─────────┘
          │
          ▼
    Réponse IA
```

### 2. Prompt Engineering

Classification automatique des questions:

| Catégorie | Mots-clés | Prompt Spécialisé |
|-----------|-----------|-------------------|
| **Grammar** | tense, verb, noun... | Explication des règles + exemples |
| **Vocabulary** | word, meaning... | Définition + synonymes + contexte |
| **Pronunciation** | pronounce, sound... | Guide IPA + conseils |
| **Conversation** | dialogue, expression... | Phrases naturelles + culture |

### 3. Interface Utilisateur

| Page | Fonctionnalités |
|------|-----------------|
| **Landing** | Hero section, features, statistiques, CTA |
| **Login/Signup** | Formulaires avec illustrations animées |
| **Chat** | Messages, sidebar, paramètres, voice input |

### 4. Fonctionnalités Vocales

- **STT**: Enregistrement → Transcription → Envoi au chat
- **TTS**: Réponse IA → Synthèse vocale → Lecture audio
- **Accents**: US (AriaNeural), UK (SoniaNeural), Australian (NatashaNeural)

---

## 📓 Le Notebook Jupyter (Important pour l'Évaluation)

Le fichier `ENGLISH_CHATBOT_IMPLEMENTATION.ipynb` démontre **toutes les compétences techniques** du projet:

### Cellules du Notebook

| # | Section | Contenu |
|---|---------|---------|
| 1 | Configuration API | Setup des clés API Groq |
| 2 | Imports | Toutes les dépendances utilisées |
| 3 | LLM Model | Initialisation Groq + test |
| 4 | Embeddings | HuggingFace sentence-transformers |
| 5 | ChromaDB | Création/chargement de la BDD vectorielle |
| 6 | Retrieval | Fonction de recherche sémantique |
| 7 | Prompts | Templates de prompts par catégorie |
| 8 | Classification | Détection du type de question |
| 9 | Chat Engine | Fonction principale de conversation |
| 10 | TTS | Text-to-Speech avec gTTS |
| 11 | Classe | EnglishLearningChatbot exportable |
| 12+ | Tests | Exemples interactifs |

### Démonstrations dans le Notebook

- ✅ Utilisation de **Groq API** avec Llama 3.3 70B
- ✅ **Embeddings** HuggingFace pour vectorisation
- ✅ **ChromaDB** pour stockage et recherche vectorielle
- ✅ **RAG complet** (Retrieval → Augmentation → Generation)
- ✅ **Prompt Engineering** avec templates spécialisés
- ✅ **Classification** automatique des requêtes
- ✅ **Text-to-Speech** pour sortie audio

---

## 🚀 Comment Exécuter le Projet

### Méthode 1: Script Batch (Recommandé)

```batch
# Double-cliquer sur START_VOICE.bat
```

### Méthode 2: Ligne de Commande

```bash
# Activer l'environnement virtuel
venv\Scripts\activate

# Définir la clé API
set GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE

# Lancer Streamlit
streamlit run voice_app.py --theme.base="light"
```

### Méthode 3: Notebook Jupyter

```bash
# Ouvrir le notebook dans VS Code ou Jupyter
# Exécuter les cellules une par une
```

---

## 📊 Résultats et Démonstration

### Captures d'Écran

1. **Landing Page**: Design moderne avec animations
2. **Login/Signup**: Formulaires avec illustrations
3. **Chat Interface**: Messages, sidebar, voice input
4. **Réponses IA**: Correction grammaticale, explications

### Fonctionnalités Testées

- [x] Création de compte utilisateur
- [x] Connexion avec persistance de session
- [x] Chat textuel avec réponses IA
- [x] Input vocal (microphone)
- [x] Output vocal (TTS multi-accents)
- [x] Historique des conversations
- [x] Paramètres (niveau, accent, corrections)

---

## 💡 Compétences Démontrées

| Compétence | Implementation |
|------------|----------------|
| **LLM/GenAI** | Groq API avec Llama 3.3 70B |
| **RAG** | ChromaDB + LangChain + HuggingFace |
| **Prompt Engineering** | Templates spécialisés + classification |
| **Speech AI** | STT (Google) + TTS (Edge-TTS) |
| **Web Development** | Streamlit + CSS custom |
| **Database** | SQLite + ChromaDB |
| **UX Design** | Interface moderne responsive |

---
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

---
## 📚 Références et Ressources

- [Groq API Documentation](https://console.groq.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Edge-TTS GitHub](https://github.com/rany2/edge-tts)

---
 6.1 Structure des Prompts

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
## 📝 Conclusion

Ce projet démontre une maîtrise complète des technologies modernes d'IA appliquées à l'éducation:

1. **RAG** pour des réponses contextuelles et précises
2. **Prompt Engineering** pour des interactions naturelles et pédagogiques
3. **Voice AI** pour une pratique orale immersive
4. **Full-Stack Development** pour une expérience utilisateur complète

L'architecture modulaire permet une extension facile des fonctionnalités futures.

---

*SpeakEasy AI - Your English Learning Companion*
*Powered by Advanced AI Technology*
