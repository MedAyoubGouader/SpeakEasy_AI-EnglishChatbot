"""
✏️ CORRECTION MODULE
English Grammar and Sentence Correction Engine
"""

from groq import Groq
import os
import re


class EnglishCorrector:
    """Handle English grammar and sentence correction"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
    
    def analyze_sentence(self, sentence: str, level: str = "Intermediate") -> dict:
        """
        Analyze and correct an English sentence
        
        Args:
            sentence: The user's sentence to analyze
            level: User's English level (Beginner/Intermediate/Advanced)
            
        Returns:
            Dictionary with correction details
        """
        prompt = f"""Analyze this English sentence and provide corrections.
User's English level: {level}

Sentence: "{sentence}"

Respond in this exact JSON format:
{{
    "has_errors": true/false,
    "original": "original sentence",
    "corrected": "corrected sentence (or same if no errors)",
    "explanation": "brief explanation of errors (if any)",
    "alternative": "a more natural way to say this",
    "vocabulary_tip": "one vocabulary or phrase tip related to the sentence"
}}

Be encouraging and helpful. If the sentence is correct, praise the user."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an English language expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            import json
            try:
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result
            except:
                pass
            
            # Fallback if JSON parsing fails
            return {
                "has_errors": False,
                "original": sentence,
                "corrected": sentence,
                "explanation": "Your sentence looks good!",
                "alternative": sentence,
                "vocabulary_tip": ""
            }
            
        except Exception as e:
            return {
                "has_errors": False,
                "original": sentence,
                "corrected": sentence,
                "explanation": f"Could not analyze: {str(e)}",
                "alternative": "",
                "vocabulary_tip": ""
            }
    
    def format_correction(self, analysis: dict) -> str:
        """
        Format correction analysis into readable message
        
        Args:
            analysis: Dictionary from analyze_sentence
            
        Returns:
            Formatted string for display
        """
        if not analysis.get("has_errors", False):
            return f"""✅ **Great job!** Your sentence is correct.

💡 **Tip:** {analysis.get('vocabulary_tip', 'Keep practicing!')}"""
        
        return f"""📝 **Let me help you with that:**

❌ **Original:** {analysis.get('original', '')}

✅ **Corrected:** {analysis.get('corrected', '')}

💡 **Explanation:** {analysis.get('explanation', '')}

🗣️ **Alternative way:** {analysis.get('alternative', '')}

📚 **Vocabulary tip:** {analysis.get('vocabulary_tip', '')}"""


class GrammarChecker:
    """Simple grammar checking utilities"""
    
    @staticmethod
    def check_common_errors(text: str) -> list:
        """
        Check for common English errors
        
        Args:
            text: Text to check
            
        Returns:
            List of potential issues
        """
        issues = []
        
        # Common patterns to check
        patterns = [
            (r'\bi am\b', "Consider: 'I am' should have capital 'I'"),
            (r'\bdont\b', "Missing apostrophe: 'don't'"),
            (r'\bdoesnt\b', "Missing apostrophe: 'doesn't'"),
            (r'\bwont\b', "Missing apostrophe: 'won't'"),
            (r'\bcant\b', "Missing apostrophe: 'can't'"),
            (r'\bits\b(?!\s)', "Check: 'its' (possessive) vs 'it's' (it is)"),
            (r'\btheir\s+(?:is|are|was|were)\b', "Check: 'their' vs 'there'"),
            (r'\byour\s+(?:a|the|going|doing)\b', "Check: 'your' vs 'you're'"),
        ]
        
        text_lower = text.lower()
        for pattern, message in patterns:
            if re.search(pattern, text_lower):
                issues.append(message)
        
        return issues
