from app.services.llm.gemini_provider import GeminiProvider
from app.services.llm.prompt_builder import PromptBuilder

class LLMService:
    def __init__(self):
        self.provider = GeminiProvider()

    def answer_question(self, question:str, retrieved_chunks:str) -> str:

        prompt = PromptBuilder.build_explanation_prompt(
            question,
            retrieved_chunks
        )

        response = self.provider.generate_response(prompt)

        return response
