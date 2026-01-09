"""
Utility functions for the AI Career Guidance Chatbot
Contains helper functions for career guidance operations
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def format_career_response(response: str) -> str:
    """Format AI career guidance responses for better readability"""
    # Basic formatting - can be expanded
    if len(response) > 4000:  # Telegram message limit
        response = response[:4000] + "...\n\n*(Response truncated)*"

    return response

def validate_career_query(query: str) -> bool:
    """Validate if a query seems career-related"""
    career_keywords = [
        'career', 'job', 'work', 'profession', 'industry', 'skill',
        'education', 'degree', 'salary', 'interview', 'resume',
        'programming', 'technology', 'business', 'marketing', 'design'
    ]

    query_lower = query.lower()
    return any(keyword in query_lower for keyword in career_keywords)

def extract_career_field(message: str) -> Optional[str]:
    """Extract potential career field from a message"""
    # Simple extraction - can be made more sophisticated
    common_fields = {
        'software': ['software', 'programming', 'coding', 'developer'],
        'data': ['data science', 'data analyst', 'machine learning', 'ai'],
        'design': ['ux', 'ui', 'graphic design', 'product design'],
        'marketing': ['marketing', 'digital marketing', 'seo', 'content'],
        'business': ['business', 'management', 'consulting', 'finance']
    }

    message_lower = message.lower()
    for field, keywords in common_fields.items():
        if any(keyword in message_lower for keyword in keywords):
            return field

    return None
                "C": opt_c,
            }
            if opt_d:
                options["D"] = opt_d
            
            # If no answer_text provided, use the option text
            if not answer_text and answer_letter in options:
                answer_text = options[answer_letter]
                
            return {
                "q": question,
                "options": options,
                "answer": answer_letter,
                "answer_text": answer_text
            }
    
    # Format 2: Q: question || A) opt1 || B) opt2 || C) opt3 || D) opt4 || Answer: X
    format2_pattern = r"Q:\s*(.*?)\s*\|\|\s*A\)\s*(.*?)\s*\|\|\s*B\)\s*(.*?)\s*\|\|\s*C\)\s*(.*?)\s*(?:\|\|\s*D\)\s*(.*?)\s*)?\|\|\s*Answer:\s*([ABCD])"
    
    match2 = re.match(format2_pattern, line, re.IGNORECASE)
    if match2:
        question = match2.group(1).strip()
        opt_a = match2.group(2).strip()
        opt_b = match2.group(3).strip()
        opt_c = match2.group(4).strip()
        opt_d = match2.group(5).strip() if match2.group(5) else None
        answer_letter = match2.group(6).upper().strip()
        
        options = {
            "A": opt_a,
            "B": opt_b,
            "C": opt_c,
        }
        if opt_d:
            options["D"] = opt_d
            
        # For format 2, answer_text is the same as the option text
        answer_text = options[answer_letter]
        
        return {
            "q": question,
            "options": options,
            "answer": answer_letter,
            "answer_text": answer_text
        }
    
    return None

def check_answer(user_input: str, correct_answer: str, correct_answer_text: str, options: Dict[str, str]) -> bool:
    """
    Check if user's answer is correct. Accepts:
    1. Option letter (A, B, C, D) - case insensitive
    2. Full answer text - case insensitive match
    
    Args:
        user_input: User's answer (letter or text)
        correct_answer: Correct option letter (A/B/C/D)
        correct_answer_text: Correct answer text
        options: Dictionary of all options {A: text, B: text, ...}
        
    Returns:
        True if answer is correct, False otherwise
    """
    user_input = user_input.strip()
    
    # Check if input is a single letter (A, B, C, D)
    if len(user_input) == 1 and user_input.upper() in options.keys():
        return user_input.upper() == correct_answer.upper()
    
    # Check if input matches correct answer text (case insensitive)
    if user_input.lower() == correct_answer_text.lower():
        return True
    
    # Check if input matches any option text and it's the correct one
    for letter, option_text in options.items():
        if user_input.lower() == option_text.lower():
            return letter.upper() == correct_answer.upper()
    
    return False

# Keep the old function name for backward compatibility
def parse_question_line(line: str) -> Optional[Dict[str, Any]]:
    """
    Legacy function - calls the new parse_question function
    """
    return parse_question(line)

def validate_question(question_dict: Dict[str, Any]) -> bool:
    """
    Validate a question dictionary to ensure it has all required fields
    
    Args:
        question_dict: Dictionary containing question data
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(question_dict, dict):
        return False
    
    required_keys = ["q", "options", "answer"]
    if not all(key in question_dict for key in required_keys):
        return False
    
    # Check if question text exists
    if not question_dict["q"].strip():
        return False
    
    # Check question character limit (5000 characters max)
    question_text = question_dict["q"]
    if len(question_text) > 5000:
        return False
    
    # Check if options is a dict with at least A, B, C keys
    options = question_dict["options"]
    if not isinstance(options, dict):
        return False
    
    required_options = ["A", "B", "C"]
    if not all(opt in options for opt in required_options):
        return False
    
    # Check if all required options have text
    if not all(options[opt].strip() for opt in required_options if opt in options):
        return False
    
    # Check if D option exists and has text (if present)
    if "D" in options and not options["D"].strip():
        return False
    
    # Check if answer is valid (A, B, C, or D if D option exists)
    valid_answers = ["A", "B", "C"]
    if "D" in options:
        valid_answers.append("D")
    
    if question_dict["answer"] not in valid_answers:
        return False
    
    # Check if answer refers to an existing option
    if question_dict["answer"] not in options:
        return False
    
    return True

def format_question_for_display(question: Dict[str, Any], question_number: int) -> str:
    """
    Format a question for display to users
    
    Args:
        question: Question dictionary
        question_number: The question number (1-indexed)
        
    Returns:
        Formatted question string
    """
    options_text = (
        f"A) {question['options']['A']}\n"
        f"B) {question['options']['B']}\n"
        f"C) {question['options']['C']}\n"
    )
    
    # Add D option if it exists
    if 'D' in question['options']:
        options_text += f"D) {question['options']['D']}\n"
    
    # Determine valid answer options
    valid_options = "A/B/C/D" if 'D' in question['options'] else "A/B/C"
    
    return (
        f"Q{question_number}: {question['q']}\n"
        f"{options_text}\n"
        f"Send your answer ({valid_options}) or type the full answer text:"
    )
