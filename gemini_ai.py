"""
Gemini AI Assistant Feature for Career Guidance Chatbot
Handles intelligent responses for career questions, advice, and guidance
"""

import google.generativeai as genai
import json
import re
from typing import Dict, Any, List, Optional
import logging
from config import GEMINI_API_KEY, OWNER_ID, SUDO_USERS

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini AI
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Multiple models for different purposes - using faster preview versions
    models = {
        'fast': genai.GenerativeModel('gemini-2.5-flash-lite'),  # Fastest model for quick responses
        'pro': genai.GenerativeModel('gemini-2.5-flash-lite'),                   # Detailed career advice
        'flash_latest': genai.GenerativeModel('gemini-2.5-flash-lite'),     # Always latest stable flash
        'pro_latest': genai.GenerativeModel('gemini-2.5-flash-lite')          # Always latest stable pro
    }
    model = models['fast']  # Default to fastest model
    logger.info("✅ Gemini AI initialized with optimized models (using gemini-2.5-flash-lite)")
except Exception as e:
    logger.error(f"❌ Gemini AI initialization failed: {e}")
    models = None
    model = None

class GeminiAI:
    """Gemini AI Assistant for the Career Guidance Chatbot"""

    def __init__(self):
        self.models = models
        self.model = model  # Default model
        self.system_prompt = """
You are an AI Career Guidance Counselor with extensive knowledge about careers, job markets, skill development, and professional growth. Help users make informed career decisions by providing:

1. **Career Exploration:**
   - Help users identify suitable career paths based on their interests, skills, and education
   - Provide information about various industries and job roles
   - Suggest career transitions and how to make them successfully

2. **Skill Development:**
   - Recommend learning paths and resources
   - Identify essential skills for different careers
   - Suggest certifications, courses, and training programs

3. **Job Market Insights:**
   - Provide information about salary ranges, job outlook, and industry trends
   - Help with resume writing and interview preparation
   - Offer job search strategies and networking advice

4. **Educational Guidance:**
   - Advise on degree programs and their career outcomes
   - Suggest continuing education and professional development
   - Help with choosing between different educational paths

5. **Practical Advice:**
   - Offer work-life balance tips
   - Provide guidance on career advancement
   - Help with overcoming career challenges

Always be encouraging, realistic, and provide actionable advice. Use current market data when possible and be honest about the challenges and rewards of different career paths. Respond in a conversational, supportive tone.
        """
    
    async def generate_response(self, user_input: str, context: Optional[str] = None) -> str:
        """
        Generate AI response based on user input
        
        Args:
            user_input: User's message/question
            context: Optional context from previous messages
            
        Returns:
            AI generated response
        """
        if not self.models or not self.model:
            return "❌ AI Assistant is currently unavailable. Please try again later."
        
        try:
            # Use only the best model (gemini-2.5-flash) for /ask command
            # This prevents multiple responses
            selected_model = self.models.get('fast', self.model)
            
            # Prepare the prompt
            full_prompt = self.system_prompt + "\n\n"
            if context:
                full_prompt += f"Context: {context}\n\n"
            full_prompt += f"User Input: {user_input}\n\nResponse:"
            
            # Generate response using only one model with optimized config
            logger.info(f"🤖 Using model: gemini-2.5-flash-preview-05-20 for /ask command")
            response = selected_model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1000,  # Limit for faster responses
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            
            if response and response.text:
                logger.info(f"✅ AI response generated successfully")
                return response.text.strip()
            else:
                return "❌ Sorry, I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Gemini AI error: {e}")
            return "❌ AI Assistant error occurred. Please try again later."
    
    async def generate_quiz_questions(self, topic: str, count: int = 5, difficulty: str = "medium") -> str:
        """
        Generate quiz questions on a specific topic
        
        Args:
            topic: Topic to generate questions about
            count: Number of questions to generate
            difficulty: Difficulty level (easy/medium/hard)
            
        Returns:
            Formatted quiz questions
        """
        if not self.models:
            return "❌ AI Assistant is currently unavailable."
        
        # Select model based on difficulty
        selected_model = self.model  # Default
        if difficulty.lower() == "hard":
            selected_model = self.models.get('pro', self.model)
        elif difficulty.lower() in ["easy", "medium"]:
            selected_model = self.models.get('fast', self.model)
        
        try:
            prompt = f"""You are a Quiz Generator AI.
Generate {count} multiple-choice quiz questions on the topic "{topic}".

⚡ Rules:
1. Each question must have exactly 4 options.
2. Label options as A., B., C., D.
3. Clearly specify the correct answer at the end as: Answer: X
4. Output must ONLY follow the below format (no extra explanation, no extra text):

Format Example:
Q) What is the capital of France?
A. Berlin
B. Madrid
C. Paris
D. Rome
Answer: C

Generate {count} questions now:"""
            
            response = selected_model.generate_content(prompt)
            
            if response and response.text:
                # Return the formatted quiz questions directly
                return response.text.strip()
            else:
                return "❌ Failed to generate quiz questions."
                
        except Exception as e:
            logger.error(f"Quiz generation error: {e}")
            return "❌ Error generating quiz questions."
    
    async def explain_answer(self, question: str, user_answer: str, correct_answer: str) -> str:
        """
        Explain quiz answer and provide feedback
        
        Args:
            question: The quiz question
            user_answer: User's selected answer
            correct_answer: The correct answer
            
        Returns:
            Explanation of the answer
        """
        if not self.model:
            return "❌ AI Assistant is currently unavailable."
        
        try:
            prompt = f"""
Question: {question}
User's Answer: {user_answer}
Correct Answer: {correct_answer}

Please explain:
1. Whether the user's answer is correct or incorrect
2. Why the correct answer is right
3. Provide a brief educational explanation

Keep the response concise and educational.
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "❌ Could not generate explanation."
                
        except Exception as e:
            logger.error(f"Answer explanation error: {e}")
            return "❌ Error generating answer explanation."

# Global instance
gemini_ai = GeminiAI()

# Simple cache to prevent duplicate responses
recent_requests = {}

async def handle_ai_request(user_input: str, user_id: int, context: Optional[str] = None) -> str:
    """
    Handle AI request with permission checking and duplicate prevention
    
    Args:
        user_input: User's message
        user_id: Telegram user ID
        context: Optional context
        
    Returns:
        AI response or permission error
    """
    # Check if user has permission (owner or sudo users only)
    if user_id not in [OWNER_ID] + SUDO_USERS:
        return "❌ AI Assistant access is restricted to authorized users only."
    
    # Create request key for deduplication
    request_key = f"{user_id}:{hash(user_input)}"
    
    # Check if this exact request was made recently (within last 10 seconds)
    import time
    current_time = time.time()
    if request_key in recent_requests:
        if current_time - recent_requests[request_key] < 10:
            logger.info(f"🔄 Preventing duplicate request from user {user_id}")
            return "⏳ Please wait, your previous request is still being processed..."
    
    # Update request timestamp
    recent_requests[request_key] = current_time
    
    # Clean old entries (older than 60 seconds)
    to_remove = [key for key, timestamp in recent_requests.items() if current_time - timestamp > 60]
    for key in to_remove:
        del recent_requests[key]
    
    logger.info(f"🤖 Processing AI request from user {user_id}: {user_input[:50]}...")
    return await gemini_ai.generate_response(user_input, context)

async def handle_quiz_generation(topic: str, count: int, difficulty: str, user_id: int) -> str:
    """
    Handle quiz generation request with permission checking
    
    Args:
        topic: Topic to generate questions about
        count: Number of questions
        difficulty: Difficulty level
        user_id: Telegram user ID
        
    Returns:
        Generated quiz questions or permission error
    """
    # Check if user has permission (owner or sudo users only)
    if user_id not in [OWNER_ID] + SUDO_USERS:
        return "❌ Quiz generation access is restricted to authorized users only."
    
    # Validate parameters
    if count < 1 or count > 20:
        return "❌ Question count must be between 1 and 20."
    
    if difficulty.lower() not in ['easy', 'medium', 'hard']:
        return "❌ Difficulty must be: easy, medium, or hard."
    
    if len(topic.strip()) < 2:
        return "❌ Topic is too short. Please provide a valid topic."
    
    return await gemini_ai.generate_quiz_questions(topic, count, difficulty.lower())

def is_ai_available() -> bool:
    """Check if AI assistant is available"""
    return models is not None and model is not None

def get_ai_status() -> str:
    """Get AI assistant status message"""
    if is_ai_available():
        available_models = list(models.keys()) if models else []
        return f"✅ Crush AI Assistant is active!\n🔥 Available Models: {', '.join(available_models)}"
    else:
        return "❌ Crush AI Assistant is currently unavailable."
