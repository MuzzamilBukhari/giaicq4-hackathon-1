from typing import Optional, Dict, Any
from ..auth.security import verify_token
from ..auth.crud import get_user_by_id
from sqlalchemy.orm import Session
from ..db.connection import SessionLocal
import uuid


def get_user_context_for_personalization(token: Optional[str] = None) -> Dict[str, Any]:
    """
    Get user context for personalization based on JWT token.
    Returns default context if no token or invalid token.
    """
    if not token:
        # Default context for unauthenticated users (intermediate level)
        return {
            "robotics_level": "intermediate",
            "hardware_exp": "intermediate",
            "software_exp": "intermediate",
            "is_authenticated": False,
            "user_id": None
        }

    # Verify token
    token_data = verify_token(token)
    if not token_data:
        # Invalid token, return default context
        return {
            "robotics_level": "intermediate",
            "hardware_exp": "intermediate",
            "software_exp": "intermediate",
            "is_authenticated": False,
            "user_id": None
        }

    # Get user from database
    db: Session = SessionLocal()
    try:
        user_id = uuid.UUID(token_data.user_id)
        user = get_user_by_id(db, user_id)

        if not user:
            # User not found, return default context
            return {
                "robotics_level": "intermediate",
                "hardware_exp": "intermediate",
                "software_exp": "intermediate",
                "is_authenticated": False,
                "user_id": None
            }

        # Return user context
        return {
            "robotics_level": user.robotics_level or "intermediate",
            "hardware_exp": user.hardware_exp or "intermediate",
            "software_exp": user.software_exp or "intermediate",
            "is_authenticated": True,
            "user_id": str(user.id),
            "goals": user.goals
        }
    except Exception:
        # Error occurred, return default context
        return {
            "robotics_level": "intermediate",
            "hardware_exp": "intermediate",
            "software_exp": "intermediate",
            "is_authenticated": False,
            "user_id": None
        }
    finally:
        db.close()


def modify_prompt_based_on_user_context(prompt: str, user_context: Dict[str, Any]) -> str:
    """
    Modify a prompt based on the user's context for personalization.
    """
    robotics_level = user_context.get("robotics_level", "intermediate")

    # Create personalized context injection
    if robotics_level == "beginner":
        personalization_context = (
            f"User Profile: Beginner in robotics (robotics_level: {user_context.get('robotics_level', 'intermediate')}, "
            f"hardware_exp: {user_context.get('hardware_exp', 'intermediate')}, "
            f"software_exp: {user_context.get('software_exp', 'intermediate')}). "
            "When explaining technical concepts, use simple language, provide analogies, "
            "and break down complex processes into smaller steps. Avoid jargon and explain "
            "any technical terms that must be used."
        )
    elif robotics_level == "advanced":
        personalization_context = (
            f"User Profile: Advanced in robotics (robotics_level: {user_context.get('robotics_level', 'intermediate')}, "
            f"hardware_exp: {user_context.get('hardware_exp', 'intermediate')}, "
            f"software_exp: {user_context.get('software_exp', 'intermediate')}). "
            "Provide detailed technical explanations, use domain-specific terminology, "
            "and include advanced implementation details. Assume familiarity with "
            "fundamental concepts and focus on sophisticated aspects."
        )
    else:  # intermediate
        personalization_context = (
            f"User Profile: Intermediate in robotics (robotics_level: {user_context.get('robotics_level', 'intermediate')}, "
            f"hardware_exp: {user_context.get('hardware_exp', 'intermediate')}, "
            f"software_exp: {user_context.get('software_exp', 'intermediate')}). "
            "Provide balanced technical explanations with some high-level overviews. "
            "Include relevant technical details while maintaining accessibility for "
            "users with some background knowledge."
        )

    # Add the personalization context to the original prompt
    return f"{personalization_context}\n\n{prompt}"


def get_response_instruction_for_level(robotics_level: str) -> str:
    """
    Get specific instruction for response complexity based on user level.
    """
    if robotics_level == "beginner":
        return (
            "Explain this concept in simple terms with analogies and step-by-step breakdowns. "
            "Avoid jargon and explain any technical terms. Use beginner-friendly language."
        )
    elif robotics_level == "advanced":
        return (
            "Provide in-depth technical details with advanced terminology. "
            "Include implementation specifics and assume knowledge of fundamentals. "
            "Focus on complex aspects and sophisticated applications."
        )
    else:  # intermediate
        return (
            "Provide balanced technical explanations with appropriate detail. "
            "Include relevant technical information while maintaining accessibility. "
            "Assume some background knowledge but explain important concepts."
        )