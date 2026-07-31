from app.services.retrieval_service import RetrievalService
from app.services.llm.llm_service import LLMService
from app.services.session_manager import session_manager
from app.schemas.chat import ChatRequest,ChatResponse,ChatMessage,MessageRole

class ConversationService:

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()
        self.session_manager = session_manager

    def chat(self, request:ChatRequest) -> ChatResponse:

        session_id = request.session_id

        if session_id is None:
            session_id = self.session_manager.create_session()

        history = self.session_manager.get_history(session_id)

        search_result = self.retrieval_service.search(
            repository_name=request.repository_name,
            query=request.question,
            top_k=5,
        )

        answer = self.llm_service.answer_chat(
            question=request.question,
            history=history,
            retrieved_chunks=search_result["results"],
        )

        # Saving Conversation

        # saving user's request
        self.session_manager.add_message(
            session_id=session_id,
            message=ChatMessage(
                role=MessageRole.USER,
                content=request.question,
            ),
        )

        # saving assistant's reply
        self.session_manager.add_message(
            session_id=session_id,
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=answer,
            ),
        )

        sources = list(dict.fromkeys(
            chunk["file_path"]
            for chunk in search_result["results"]
        ))

        return ChatResponse(
            answer=answer,
            session_id=session_id,
            sources=sources,
        )