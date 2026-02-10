"""
💬 CHAT LOGIC MODULE
Conversational AI and Response Generation
"""

from groq import Groq
import os
from datetime import datetime


class ChatEngine:
    """Handle chat conversation logic"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
    def get_system_prompt(self, level: str = "Intermediate", correction_enabled: bool = True) -> str:
        """
        Generate system prompt based on user settings
        
        Args:
            level: User's English level
            correction_enabled: Whether to correct grammar
            
        Returns:
            System prompt string
        """
        correction_instruction = ""
        if correction_enabled:
            correction_instruction = """
When the user makes grammar or vocabulary mistakes:
1. First, understand what they meant
2. Respond naturally to their message
3. Then gently point out any errors
4. Show the corrected version
5. Give a brief, simple explanation
6. Suggest a more natural way to say it

Format corrections like this:
📝 **Quick tip:** [correction explanation]
✅ **Better way:** [corrected sentence]
"""
        
        level_instruction = {
            "Beginner": "Use simple vocabulary and short sentences. Explain things clearly.",
            "Intermediate": "Use moderate vocabulary. Include some idioms and phrasal verbs.",
            "Advanced": "Use rich vocabulary, idioms, and complex structures. Challenge the user."
        }.get(level, "Use moderate vocabulary.")
        
        return f"""You are a friendly, encouraging English tutor and conversation partner.

Your role:
- Help users practice and improve their English
- Have natural, engaging conversations
- Be patient, supportive, and never discouraging
- Adapt to the user's level: {level}
- {level_instruction}

{correction_instruction}

Guidelines:
- Always respond in clear, natural English
- Be warm and encouraging
- Ask follow-up questions to keep the conversation going
- Share interesting facts or cultural insights when relevant
- Celebrate the user's progress
- If they seem frustrated, offer encouragement

Remember: Learning a language takes time. Be the supportive tutor everyone wishes they had!"""

    def generate_response(
        self, 
        messages: list, 
        level: str = "Intermediate",
        correction_enabled: bool = True
    ) -> str:
        """
        Generate AI response to user message
        
        Args:
            messages: List of conversation messages
            level: User's English level
            correction_enabled: Whether to include corrections
            
        Returns:
            AI response string
        """
        system_prompt = self.get_system_prompt(level, correction_enabled)
        
        # Prepare messages for API
        api_messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history (limit to last 10 messages)
        for msg in messages[-10:]:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, I'm having trouble responding right now. Error: {str(e)}"
    
    def generate_conversation_starter(self, level: str = "Intermediate") -> str:
        """
        Generate a conversation starter based on level
        
        Args:
            level: User's English level
            
        Returns:
            Conversation starter message
        """
        starters = {
            "Beginner": [
                "Hello! 👋 How are you today? Let's practice some simple English together!",
                "Hi there! 😊 What's your name? I'm here to help you learn English!",
                "Welcome! 🌟 Tell me about yourself. What do you like to do?"
            ],
            "Intermediate": [
                "Hey! 👋 I'm excited to chat with you today. What would you like to talk about?",
                "Hello! 🎯 How's your English learning journey going? Any topics you'd like to explore?",
                "Hi there! 📚 Shall we have a conversation about something interesting?"
            ],
            "Advanced": [
                "Greetings! 🎓 I'm looking forward to an engaging conversation. What's on your mind?",
                "Hello! 💡 Ready for some stimulating discussion? What topics intrigue you lately?",
                "Welcome! 🌍 Let's dive into an interesting conversation. What would you like to explore?"
            ]
        }
        
        import random
        return random.choice(starters.get(level, starters["Intermediate"]))


class ConversationManager:
    """Manage conversation history and state"""
    
    def __init__(self):
        self.messages = []
        self.created_at = datetime.now()
    
    def add_message(self, role: str, content: str) -> dict:
        """
        Add a message to conversation history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            
        Returns:
            The added message dict
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        self.messages.append(message)
        return message
    
    def get_messages(self) -> list:
        """Get all messages"""
        return self.messages
    
    def clear(self):
        """Clear conversation history"""
        self.messages = []
        self.created_at = datetime.now()
    
    def get_message_count(self) -> int:
        """Get total message count"""
        return len(self.messages)
    
    def get_user_message_count(self) -> int:
        """Get user message count only"""
        return len([m for m in self.messages if m["role"] == "user"])
