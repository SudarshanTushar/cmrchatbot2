"""
Database module for AI Career Guidance Chatbot
Handles MongoDB connection for basic logging and user data
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME
import logging

logger = logging.getLogger(__name__)

# Sync MongoDB Client
try:
    client = MongoClient(MONGO_URI)
    # Test the connection
    client.admin.command('ping')
    logger.info("✅ MongoDB connection successful!")
except ConnectionFailure as e:
    logger.error(f"❌ MongoDB connection failed: {e}")
    client = None

# Database
db = client[DB_NAME] if client is not None else None

# Collections (simplified for career guidance)
user_conversations = db.user_conversations if db is not None else None  # Store conversation history
user_preferences = db.user_preferences if db is not None else None     # Store user preferences
bot_stats = db.bot_stats if db is not None else None                   # Store bot usage statistics

# Async MongoDB Client
async_client = AsyncIOMotorClient(MONGO_URI)
async_db = async_client[DB_NAME]

# Async Collections
async_user_conversations = async_db.user_conversations
async_user_preferences = async_db.user_preferences
async_bot_stats = async_db.bot_stats

def get_db_status() -> bool:
    """Check if database connection is active"""
    return client is not None and db is not None

async def log_conversation(user_id: int, user_message: str, bot_response: str):
    """Log a conversation for analytics"""
    if not async_user_conversations:
        return

    try:
        await async_user_conversations.insert_one({
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": __import__('datetime').datetime.utcnow()
        })
    except Exception as e:
        logger.error(f"Failed to log conversation: {e}")

async def update_bot_stats(command: str, user_id: int):
    """Update bot usage statistics"""
    if not async_bot_stats:
        return

    try:
        # Increment command usage counter
        await async_bot_stats.update_one(
            {"command": command},
            {"$inc": {"usage_count": 1}, "$set": {"last_used": __import__('datetime').datetime.utcnow()}},
            upsert=True
        )

        # Update unique users count
        await async_bot_stats.update_one(
            {"type": "unique_users"},
            {"$addToSet": {"user_ids": user_id}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Failed to update bot stats: {e}")

async def get_bot_stats():
    """Get bot usage statistics"""
    if not async_bot_stats:
        return {"error": "Database not available"}

    try:
        stats = {}
        async for stat in async_bot_stats.find():
            if "command" in stat:
                stats[stat["command"]] = stat.get("usage_count", 0)
            elif stat.get("type") == "unique_users":
                stats["unique_users"] = len(stat.get("user_ids", []))

        return stats
    except Exception as e:
        logger.error(f"Failed to get bot stats: {e}")
        return {"error": str(e)}
        
    try:
        # Create TTL index on timestamp field (expires after 30 minutes = 1800 seconds)
        await async_quiz_results.create_index("timestamp", expireAfterSeconds=1800)
        print("✅ TTL index created for quiz results (30 minutes expiry)")
        _ttl_initialized = True
    except Exception as e:
        print(f"⚠️ TTL index already exists or error creating: {e}")
        _ttl_initialized = True  # Mark as initialized even on error to avoid repeated attempts

def get_db_status():
    """Check if database connection is working"""
    if client is not None and db is not None:
        try:
            client.admin.command('ping')
            return True
        except:
            return False
    return False

async def save_quiz_answer(chat_id: int, user_id: int, username: str, set_name: str, 
                          question_no: int, user_answer: str, correct_answer: str, is_correct: bool, session_id: Optional[str] = None):
    """Save individual quiz answer to database (InlineKeyboard system)"""
    try:
        # Initialize TTL index if needed
        await setup_ttl_index()
        
        # Check if user already answered this question in the current session
        query = {
            "chat_id": chat_id,
            "user_id": user_id,
            "set_name": set_name,
            "question_no": question_no
        }
        # Only check for same session if session_id is provided
        if session_id:
            query["session_id"] = session_id
        
        existing_answer = await async_quiz_results.find_one(query)
        
        if existing_answer:
            return False  # User already answered this question in current session
        
        # Save new answer
        answer_doc = {
            "chat_id": chat_id,
            "user_id": user_id,
            "username": username,
            "set_name": set_name,
            "question_no": question_no,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "timestamp": datetime.now(),  # MongoDB TTL will use this
            "session_id": session_id
        }
        
        await async_quiz_results.insert_one(answer_doc)
        return True
        
    except Exception as e:
        print(f"Error saving quiz answer: {e}")
        return False

async def save_quiz_result(chat_id: int, user_id: int, user_name: str, quiz_set: str, 
                          correct: int, wrong: int, total: int):
    """Save individual quiz result to database (legacy compatibility)"""
    try:
        result = {
            "chat_id": chat_id,
            "user_id": user_id,
            "user_name": user_name,
            "quiz_set": quiz_set,
            "correct_answers": correct,
            "wrong_answers": wrong,
            "total_questions": total,
            "percentage": (correct / total * 100) if total > 0 else 0,
            "timestamp": asyncio.get_event_loop().time()
        }
        await async_quiz_results.insert_one(result)
        
        # Update cumulative user scores
        await update_user_cumulative_score(user_id, user_name, correct, total)
        
    except Exception as e:
        print(f"Error saving quiz result: {e}")

async def update_user_cumulative_score(user_id: int, user_name: str, correct: int, total: int):
    """Update user's cumulative score across all quizzes"""
    try:
        # Find existing user score or create new one
        existing_score = await async_user_scores.find_one({"user_id": user_id})
        
        if existing_score:
            # Update existing score
            new_total_correct = existing_score["total_correct"] + correct
            new_total_questions = existing_score["total_questions"] + total
            new_quiz_count = existing_score["quiz_count"] + 1
            
            await async_user_scores.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_name": user_name,  # Update name in case it changed
                        "total_correct": new_total_correct,
                        "total_questions": new_total_questions,
                        "quiz_count": new_quiz_count,
                        "average_percentage": (new_total_correct / new_total_questions * 100) if new_total_questions > 0 else 0,
                        "last_quiz_timestamp": asyncio.get_event_loop().time()
                    }
                }
            )
        else:
            # Create new user score record
            new_score = {
                "user_id": user_id,
                "user_name": user_name,
                "total_correct": correct,
                "total_questions": total,
                "quiz_count": 1,
                "average_percentage": (correct / total * 100) if total > 0 else 0,
                "first_quiz_timestamp": asyncio.get_event_loop().time(),
                "last_quiz_timestamp": asyncio.get_event_loop().time()
            }
            await async_user_scores.insert_one(new_score)
            
    except Exception as e:
        print(f"Error updating user cumulative score: {e}")

async def get_top_users(limit: int = 10):
    """Get top users by average percentage across all quizzes"""
    try:
        cursor = async_user_scores.find().sort([
            ("average_percentage", -1),
            ("total_correct", -1),
            ("quiz_count", -1)
        ]).limit(limit)
        
        results = []
        async for user in cursor:
            results.append({
                "user_id": user["user_id"],
                "user_name": user["user_name"],
                "total_correct": user["total_correct"],
                "total_questions": user["total_questions"],
                "quiz_count": user["quiz_count"],
                "average_percentage": user["average_percentage"]
            })
        
        return results
        
    except Exception as e:
        print(f"Error getting top users: {e}")
        return []

async def get_user_quiz_history(user_id: int, limit: int = 5):
    """Get user's recent quiz history"""
    try:
        cursor = async_quiz_results.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)
        
        results = []
        async for quiz in cursor:
            results.append({
                "quiz_set": quiz["quiz_set"],
                "correct_answers": quiz["correct_answers"],
                "total_questions": quiz["total_questions"],
                "percentage": quiz["percentage"],
                "timestamp": quiz["timestamp"]
            })
        
        return results
        
    except Exception as e:
        print(f"Error getting user quiz history: {e}")
        return []

async def get_user_quiz_answers(user_id: int, set_name: str):
    """Get user's answers for a specific quiz set (latest session only)"""
    try:
        # First, get the latest session_id for this user and set
        latest_session_cursor = async_quiz_results.find({
            "user_id": user_id,
            "set_name": set_name
        }).sort("timestamp", -1).limit(1)
        
        latest_session = None
        async for doc in latest_session_cursor:
            latest_session = doc
            break
        
        if not latest_session:
            return []
        
        # Get all answers from the latest session
        session_id = latest_session.get("session_id")
        
        # If session_id exists, filter by it, otherwise get latest by timestamp
        if session_id:
            cursor = async_quiz_results.find({
                "user_id": user_id,
                "set_name": set_name,
                "session_id": session_id
            }).sort("question_no", 1)
        else:
            # Fallback: get answers from latest timestamp
            latest_timestamp = latest_session["timestamp"]
            cursor = async_quiz_results.find({
                "user_id": user_id,
                "set_name": set_name,
                "timestamp": {"$gte": latest_timestamp - timedelta(minutes=30)}
            }).sort("question_no", 1)
        
        results = []
        async for answer in cursor:
            results.append({
                "question_no": answer["question_no"],
                "user_answer": answer["user_answer"],
                "correct_answer": answer["correct_answer"],
                "is_correct": answer["is_correct"]
            })
        
        return results
        
    except Exception as e:
        print(f"Error getting user quiz answers: {e}")
        return []

# TTL index is automatically initialized when save_quiz_answer is first called
