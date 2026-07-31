from app.services.llm.gemini_provider import GeminiProvider
from app.services.llm.prompt_builder import PromptBuilder
from app.schemas.chat import ChatMessage

class LLMService:
    def __init__(self):
        self.provider = GeminiProvider()

    def answer_question(self, question:str, retrieved_chunks:str) -> str:

        prompt = PromptBuilder.build_qa_prompt(
            question,
            retrieved_chunks
        )

        response = self.provider.generate_response(prompt)

        return response

    def answer_chat(self, question:str, history:list[ChatMessage], retrieved_chunks:list):

        prompt = PromptBuilder.build_chat_prompt(
            question,
            history,
            retrieved_chunks,
        )

        response = self.provider.generate_response(prompt)

        return response
