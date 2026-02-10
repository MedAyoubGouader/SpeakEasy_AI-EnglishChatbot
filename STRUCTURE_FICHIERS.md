# Structure des Fichiers - SpeakEasy AI

Ce document explique l'utilité de chaque fichier et dossier du projet.

---

## 📄 Fichiers Racine

### Fichiers Essentiels (Utilisés)

| Fichier | Statut | Description |
|---------|--------|-------------|
| `voice_app.py` | ✅ **PRINCIPAL** | Application Streamlit complète (~2000 lignes). Contient: CSS, pages (landing, login, signup, chat), logique IA, fonctions vocales, authentification. |
| `ENGLISH_CHATBOT_IMPLEMENTATION.ipynb` | ✅ **IMPORTANT** | Notebook Jupyter démontrant toutes les technologies: RAG, ChromaDB, Prompt Engineering, LLM, TTS. **Fichier clé pour l'évaluation.** |
| `requirements.txt` | ✅ Utilisé | Liste des dépendances Python nécessaires. |
| `start.bat` | ✅ Utilisé | Script de lancement Windows basique. |
| `START_VOICE.bat` | ✅ Utilisé | Script de lancement avec clé API pré-configurée (recommandé). |

### Fichiers Legacy/Utilitaires

| Fichier | Statut | Description |
|---------|--------|-------------|
| `voice_app_legacy.py` | ⚠️ **Legacy** | Ancienne version de l'application sans système d'authentification ni pages multiples. Conservé comme référence. **Peut être supprimé.** |
| `voice_engine.py` | ⚠️ **Legacy** | Module vocal standalone. Les fonctions ont été intégrées directement dans `voice_app.py`. **Peut être supprimé.** |
| `admin_view.py` | 🔧 Utilitaire | Outil administrateur pour visualiser et requêter la base de données SQLite. Utile pour le debug mais pas nécessaire en production. |
| `DOCUMENTATION.md` | ❌ **Ancien** | Ancienne documentation. Remplacée par `DOCUMENTATION_TECHNIQUE.md`. **À supprimer.** |

---

## 📁 Dossier `modules/`

Modules Python backend réutilisables.

| Fichier | Statut | Description |
|---------|--------|-------------|
| `__init__.py` | ✅ Utilisé | Fichier d'initialisation du package Python. |
| `database.py` | ✅ **Utilisé** | Gestion de la base de données SQLite: création tables users/conversations/messages, authentification, CRUD. |
| `chat_logic.py` | ⚠️ Partiellement | Logique de chat originale. Certaines fonctions utilisées, d'autres intégrées dans `voice_app.py`. |
| `correction.py` | ⚠️ Partiellement | Module d'analyse grammaticale. Fonctionnalité intégrée dans les prompts IA. |
| `voice.py` | ⚠️ Partiellement | Fonctions STT/TTS originales. La plupart intégrées dans `voice_app.py`. |
| `ui.py` | ⚠️ Legacy | Composants UI réutilisables. Non utilisé actuellement, CSS dans `voice_app.py`. |

---

## 📁 Dossier `data/`

Données textuelles pour le système RAG (indexées dans ChromaDB).

| Sous-dossier | Fichiers | Description |
|--------------|----------|-------------|
| `grammar/` | `rules.txt` | Règles grammaticales anglaises (tenses, articles, etc.) |
| `vocabulary/` | `topics.txt`, `ENGLISH_CERF_WORDS.csv` | Vocabulaire thématique + 5000+ mots classés par niveau CEFR (A1-C2) |
| `pronunciation/` | `ipa_guide.txt` | Guide de prononciation avec symboles IPA |
| `conversation_scripts/` | `dialogues.txt` | Exemples de dialogues et conversations |
| `phrasal_verbs_idioms/` | `comprehensive.txt` | Phrasal verbs et expressions idiomatiques |
| `exam_prep/` | `ielts_toefl.txt` | Ressources préparation aux examens |
| `listening_materials/` | `transcripts.txt` | Transcriptions pour compréhension orale |
| `writing_guides/` | `tips.txt` | Conseils et guides de rédaction |

**Tous ces fichiers sont utilisés** pour alimenter la base vectorielle ChromaDB et fournir du contexte aux réponses IA.

---

## 📁 Dossier `english_learning_db/`

Bases de données du projet.

| Fichier | Description |
|---------|-------------|
| `chroma.sqlite3` | Base de données ChromaDB contenant les embeddings vectoriels des documents `data/`. Utilisée pour la recherche sémantique RAG. |
| `users_chat.db` | Base de données SQLite contenant: utilisateurs, conversations, messages. Gère l'authentification et l'historique. |

---

## 📁 Dossier `assets/`

Ressources visuelles SVG animées pour l'interface.

| Fichier | Utilisé | Description |
|---------|---------|-------------|
| `logo_animated.svg` | ✅ | Logo SpeakEasy AI avec animation |
| `robot_animated.svg` | ✅ | Mascotte robot animée |
| `hero_animated.svg` | ✅ | Illustration hero pour landing/login |
| `icon_grammar_animated.svg` | ✅ | Icône grammaire animée |
| `icon_speaking_animated.svg` | ✅ | Icône conversation animée |
| `icon_vocabulary_animated.svg` | ✅ | Icône vocabulaire animée |
| `icon_listening_animated.svg` | ✅ | Icône écoute animée |
| `mic_animated.svg` | ✅ | Icône microphone animée |
| `favicon.svg` | ✅ | Favicon du navigateur |
| `bot_avatar.svg` | ⚠️ | Avatar bot (non utilisé actuellement) |
| `user_avatar.svg` | ⚠️ | Avatar utilisateur (non utilisé actuellement) |
| `chat_animation.svg` | ⚠️ | Animation chat (disponible) |
| `hero_illustration.svg` | ⚠️ | Illustration alternative |
| `landing_bg.svg` | ⚠️ | Arrière-plan landing (non utilisé) |
| `login_illustration.svg` | ⚠️ | Illustration login alternative |
| `icon_*.svg` | ⚠️ | Versions non-animées des icônes |

---

## 📁 Dossier `tests/`

Tests unitaires et de validation.

| Fichier | Description |
|---------|-------------|
| `test_chatbot.py` | Tests complets du chatbot |
| `test_chatbot_quick.py` | Tests rapides de validation |
| `test_results.json` | Résultats des derniers tests |

---

## 📁 Dossiers Système

| Dossier | Description |
|---------|-------------|
| `venv/` | Environnement virtuel Python avec toutes les dépendances installées |
| `__pycache__/` | Cache Python (généré automatiquement) |
| `.gradio/` | Cache Gradio (peut être supprimé) |

---

## 🗑️ Fichiers Pouvant Être Supprimés

Si vous souhaitez nettoyer le projet:

```bash
# Fichiers legacy non nécessaires
voice_app_legacy.py      # Ancienne version
voice_engine.py          # Fonctions intégrées dans voice_app.py
DOCUMENTATION.md         # Remplacé par DOCUMENTATION_TECHNIQUE.md

# Dossiers cache
.gradio/
__pycache__/
modules/__pycache__/
```

**Attention**: Ne supprimez PAS les fichiers essentiels listés en haut de ce document!

---

## 📋 Résumé

### Fichiers Essentiels à Conserver

1. `voice_app.py` - Application principale
2. `ENGLISH_CHATBOT_IMPLEMENTATION.ipynb` - Notebook démo
3. `requirements.txt` - Dépendances
4. `START_VOICE.bat` - Script de lancement
5. `modules/database.py` - Module BDD
6. Dossier `data/` - Données RAG
7. Dossier `english_learning_db/` - Bases de données
8. Dossier `assets/` - SVG (au moins les *_animated.svg)

### Fichiers Optionnels

- `admin_view.py` - Utile pour debug
- `tests/` - Tests unitaires
- Autres fichiers modules/

### Fichiers Supprimables

- `voice_app_legacy.py`
- `voice_engine.py`
- `DOCUMENTATION.md` (ancien)
- Caches Python
