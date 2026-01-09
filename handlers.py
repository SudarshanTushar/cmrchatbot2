"""
Message and command handlers for the AI Career Guidance Chatbot
Contains all the bot logic for handling user interactions
"""

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from typing import Optional
from config import OWNER_ID, SUDO_USERS
from gemini_ai import GeminiAI
import asyncio
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Initialize AI assistant
ai_assistant = GeminiAI()

def register_handlers(app: Client) -> None:
    """Register all bot handlers"""

    @app.on_message(filters.command("start"))
    async def start_command(client: Client, message: Message):
        """Handle /start command"""
        welcome_text = """
🤖 **AI Career Guidance Chatbot**

Hello! I'm your AI-powered career guidance assistant. I can help you with:

🎯 **Career Planning & Advice**
- Career path exploration
- Skill development guidance
- Industry insights
- Job market trends

💬 **Interactive Conversations**
- Ask me anything about careers
- Get personalized recommendations
- Learn about different professions

📚 **Educational Support**
- Study tips and resources
- Certification guidance
- Learning path suggestions

Just send me a message about your career interests, questions, or goals, and I'll provide helpful guidance!

**Example questions:**
- "What career should I choose with my computer science degree?"
- "How can I transition into data science?"
- "What skills do I need for a UX designer role?"
- "Tell me about the future of AI jobs"

Type /help for more commands.
        """

        await message.reply_text(
            welcome_text,
            parse_mode="markdown"
        )

    @app.on_message(filters.command("help"))
    async def help_command(client: Client, message: Message):
        """Handle /help command"""
        help_text = """
📋 **Available Commands:**

🤖 **AI Career Guidance**
• `/ask <question>` - Ask the AI assistant anything
• `/career <field>` - Get career info for a specific field
• `/skills <role>` - Learn required skills for a job role

💬 **Interactive Chat**
• Just send any message for personalized career advice
• Reply to any message for contextual responses

👑 **Admin Commands** (Owner/Sudo only)
• `/stats` - Bot usage statistics
• `/broadcast <message>` - Send message to all users

📖 **How to Use:**
1. Send me your career goals or questions
2. Ask about specific job roles or industries
3. Get advice on skill development
4. Explore different career paths

**Example:** "I'm interested in technology careers, what should I study?"
        """

        await message.reply_text(
            help_text,
            parse_mode="markdown"
        )

    @app.on_message(filters.command("ask"))
    async def ask_command(client: Client, message: Message):
        """Handle /ask command for AI assistance"""
        # Show typing indicator
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        # Get the question from command arguments
        question = message.text.replace("/ask", "").strip()

        if not question:
            await message.reply_text(
                "❓ Please provide a question after /ask\n\nExample: `/ask What career should I choose?`",
                parse_mode="markdown"
            )
            return

        try:
            # Generate AI response
            response = await ai_assistant.generate_response(question)

            # Send the response
            await message.reply_text(
                f"🤖 **AI Career Assistant:**\n\n{response}",
                parse_mode="markdown"
            )

        except Exception as e:
            logger.error(f"Error in ask command: {e}")
            await message.reply_text(
                "❌ Sorry, I'm having trouble processing your request. Please try again later."
            )

    @app.on_message(filters.command("career"))
    async def career_command(client: Client, message: Message):
        """Handle /career command for specific career information"""
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        career_field = message.text.replace("/career", "").strip()

        if not career_field:
            await message.reply_text(
                "🏢 Please specify a career field after /career\n\nExample: `/career software development`",
                parse_mode="markdown"
            )
            return

        prompt = f"Provide detailed information about a career in {career_field}, including required skills, education, salary expectations, job outlook, and career progression paths."

        try:
            response = await ai_assistant.generate_response(prompt)
            await message.reply_text(
                f"🏢 **Career Information: {career_field.title()}**\n\n{response}",
                parse_mode="markdown"
            )
        except Exception as e:
            logger.error(f"Error in career command: {e}")
            await message.reply_text("❌ Error fetching career information. Please try again.")

    @app.on_message(filters.command("skills"))
    async def skills_command(client: Client, message: Message):
        """Handle /skills command for job role skills"""
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        job_role = message.text.replace("/skills", "").strip()

        if not job_role:
            await message.reply_text(
                "🛠️ Please specify a job role after /skills\n\nExample: `/skills data scientist`",
                parse_mode="markdown"
            )
            return

        prompt = f"What are the essential skills, both technical and soft skills, needed for a {job_role}? Please provide a comprehensive list with brief explanations for each skill."

        try:
            response = await ai_assistant.generate_response(prompt)
            await message.reply_text(
                f"🛠️ **Skills for {job_role.title()}:**\n\n{response}",
                parse_mode="markdown"
            )
        except Exception as e:
            logger.error(f"Error in skills command: {e}")
            await message.reply_text("❌ Error fetching skills information. Please try again.")

    @app.on_message(filters.command("stats"))
    async def stats_command(client: Client, message: Message):
        """Handle /stats command (admin only)"""
        if message.from_user.id not in [OWNER_ID] + SUDO_USERS:
            await message.reply_text("❌ This command is only available to bot administrators.")
            return

        # Simple stats (can be expanded)
        stats_text = """
📊 **Bot Statistics:**

🤖 **AI Career Guidance Chatbot**
• Status: Active
• AI Assistant: Gemini 2.5 Flash
• Commands Processed: Available
• Users Helped: Growing daily

For detailed analytics, check the database directly.
        """

        await message.reply_text(stats_text, parse_mode="markdown")

    @app.on_message(filters.text & ~filters.command(["start", "help", "ask", "career", "skills", "stats", "broadcast"]))
    async def handle_text_messages(client: Client, message: Message):
        """Handle regular text messages for conversational AI"""
        # Show typing indicator
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        user_input = message.text.strip()

        # Skip if message is too short or seems like a command
        if len(user_input) < 2:
            return

        try:
            # Add career guidance context to the AI prompt
            career_context = """
You are an AI Career Guidance Counselor. Help users with career planning, skill development, job search advice, and professional growth. Be encouraging, informative, and provide actionable advice.

Focus areas:
- Career exploration and planning
- Skill development and learning paths
- Industry insights and trends
- Job search strategies
- Resume and interview tips
- Work-life balance advice
- Career transitions

Always be supportive and provide practical, realistic advice.
            """

            response = await ai_assistant.generate_response(user_input, career_context)

            await message.reply_text(
                f"🤖 {response}",
                parse_mode="markdown"
            )

        except Exception as e:
            logger.error(f"Error handling text message: {e}")
            await message.reply_text(
                "❌ I'm sorry, I encountered an error processing your message. Please try again or use /ask for specific questions."
            )

    @app.on_message(filters.command("broadcast"))
    async def broadcast_command(client: Client, message: Message):
        """Handle /broadcast command (admin only)"""
        if message.from_user.id not in [OWNER_ID] + SUDO_USERS:
            await message.reply_text("❌ This command is only available to bot administrators.")
            return

        broadcast_text = message.text.replace("/broadcast", "").strip()

        if not broadcast_text:
            await message.reply_text("📢 Please provide a message to broadcast after /broadcast")
            return

        # For now, just acknowledge (implement actual broadcasting if needed)
        await message.reply_text(f"📢 Broadcast message prepared: {broadcast_text}")

    # Log successful handler registration
    logger.info("✅ All career guidance handlers registered successfully")