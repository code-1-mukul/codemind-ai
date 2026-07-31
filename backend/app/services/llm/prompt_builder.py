from app.schemas.chat import ChatMessage

class PromptBuilder:

    @staticmethod
    def build_qa_prompt(question:str, retrieved_chunks:list) -> str:
        prompt = ""

        prompt += (
            "You are an expert Software Engineer specializing in code analysis.\n\n"
            "You are given code snippets retrieved from a GitHub repository.\n"
            "Answer ONLY using the provided repository context.\n"
            "Do NOT make assumptions or hallucinate missing information.\n"
            "If the answer cannot be determined from the provided context, "
            "clearly state that more repository context is required.\n\n"
        )

        prompt += "=" * 80 + "\n"
        prompt += "REPOSITORY CONTEXT\n"
        prompt += "=" * 80 + "\n\n"

        for i,chunk in enumerate(retrieved_chunks,start=1):
            prompt += f"chunk {i}\n"
            prompt += "-" * 40 + "\n"
            prompt += f"File: {chunk.get('file_path', 'Unknown')}\n"
            prompt += f"Name: {chunk.get('chunk_name', 'Unknown')}\n"
            prompt += (
                f"Lines: {chunk.get('start_line', '?')} - "
                f"{chunk.get('end_line', '?')}\n\n"
            )
            prompt += "Code:\n"
            prompt += "```python\n"
            prompt += chunk.get("content", "")
            prompt += "\n```\n\n" 

        prompt += "=" * 80 + "\n"
        prompt += "USER QUESTION\n"
        prompt += "=" * 80 + "\n\n"

        prompt += f"{question}\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "ANSWER INSTRUCTIONS\n"
        prompt += "=" * 80 + "\n\n"

        prompt += (
            "Provide a clear and structured explanation.\n"
            "Mention the relevant files and code chunks used.\n"
            "Do not use information outside the provided repository context.\n"
        )

        return prompt

    @staticmethod
    def build_chat_prompt(question:str, history:list[ChatMessage], retrieved_chunks:list) -> str:
        prompt = ""

        prompt += (
            "You are an expert Software Engineer specializing in code analysis.\n\n"
            "You are given code snippets retrieved from a GitHub repository.\n"
            "Answer ONLY using the provided repository context.\n"
            "Do NOT make assumptions or hallucinate missing information.\n"
            "If the answer cannot be determined from the provided context, "
            "clearly state that more repository context is required.\n\n"
        )

        prompt += "=" * 80 + "\n"
        prompt += "CONVERSATION HISTORY\n"
        prompt += "=" * 80 + "\n\n"

        for message in history:
            prompt += f"{message.role.value.capitalize()}:\n"
            prompt += f"{message.content}\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "REPOSITORY CONTEXT\n"
        prompt += "=" * 80 + "\n\n"

        for i,chunk in enumerate(retrieved_chunks,start=1):
            prompt += f"chunk {i}\n"
            prompt += "-" * 40 + "\n"
            prompt += f"File: {chunk.get('file_path', 'Unknown')}\n"
            prompt += f"Name: {chunk.get('chunk_name', 'Unknown')}\n"
            prompt += (
                f"Lines: {chunk.get('start_line', '?')} - "
                f"{chunk.get('end_line', '?')}\n\n"
            )
            prompt += "Code:\n"
            prompt += "```python\n"
            prompt += chunk.get("content", "")
            prompt += "\n```\n\n" 

        prompt += "=" * 80 + "\n"
        prompt += "USER QUESTION\n"
        prompt += "=" * 80 + "\n\n"

        prompt += f"{question}\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "ANSWER INSTRUCTIONS\n"
        prompt += "=" * 80 + "\n\n"

        prompt += (
            "Provide a clear and structured explanation.\n"
            "Mention the relevant files and code chunks used.\n"
            "Do not use information outside the provided repository context.\n"
        )

        return prompt