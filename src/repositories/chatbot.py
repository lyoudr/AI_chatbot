from sqlalchemy.orm import Session
from fastapi import status

from models.request import RAGLLMQuestionRequest
from db_models.chat import ChatBotLog
from utils.errors import CustomException

def create_chat_bot_log(
    db: Session,
    payload: RAGLLMQuestionRequest
):
    try:
        chatbot = ChatBotLog(
            name = 'test',
            question = payload.question,
        )
        db.add(chatbot)
        db.commit()
    except Exception as e:
        db.rollback()
        raise CustomException(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_msg=f"update chatbot log error: {str(e)}"
        )