from app.services.retrieval_service import RetrievalService
from app.services.llm.llm_service import LLMService

class QuestionAnswerService:

    def __init__(self):
        self.retriever=RetrievalService()
        self.llm=LLMService()

    def answer_question(
        self,
        repository_name: str,
        question: str,
        top_k: int=5
    ):
        search_result = self.retriever.search(
            repository_name=repository_name,
            query=question,
            top_k=top_k,
        )

        llm_answer = self.llm.answer_question(
            question=question,
            retrieved_chunks=search_result["results"],
        )

        return {
            "question":question,
            "answer":llm_answer,
            "sources":search_result["results"],
        }