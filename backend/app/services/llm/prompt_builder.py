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

    @staticmethod
    def build_architecture_prompt(
        repository_name: str,
        project_tree: dict,
        analysis: dict,
    ) -> str:

        prompt = ""

        prompt += (
            "You are an expert software architect specializing in "
            "repository analysis.\n\n"
            "Analyze the provided Python repository and infer its "
            "logical component architecture.\n\n"
            "IMPORTANT RULES:\n"
            "1. Do not assume directory names represent components.\n"
            "2. Do not assume common architectural patterns such as "
            "services, controllers, models, or repositories.\n"
            "3. Infer components from the actual code structure, "
            "imports, functions, classes, and dependencies.\n"
            "4. A repository may be flat, deeply nested, or organized "
            "in an unusual way.\n"
            "5. Every component must contain files that actually exist "
            "in the provided repository analysis.\n"
            "6. Do not invent files, dependencies, or relationships.\n"
            "7. Small utility or configuration files may remain "
            "independent if there is insufficient evidence to group them.\n\n"
        )

        prompt += "=" * 80 + "\n"
        prompt += "REPOSITORY\n"
        prompt += "=" * 80 + "\n\n"

        prompt += f"Repository: {repository_name}\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "PROJECT TREE\n"
        prompt += "=" * 80 + "\n\n"

        prompt += str(project_tree)
        prompt += "\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "STATIC ANALYSIS\n"
        prompt += "=" * 80 + "\n\n"

        prompt += str(analysis)
        prompt += "\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "OUTPUT FORMAT\n"
        prompt += "=" * 80 + "\n\n"

        prompt += (
            "For every component, include the exact repository file paths "
            "that belong to that component.\n"
            "Use only file paths that appear in the provided STATIC ANALYSIS.\n"
            "Do not invent or modify file paths.\n"
            "A component may contain one or multiple files.\n"
            "If a file does not clearly belong to another component, it may "
            "form its own component.\n\n"
        )

        prompt += """
    Return ONLY valid JSON in exactly this structure:

    {
    "nodes": [
        {
        "id": "component_1",
        "label": "Component Name",
        "type": "module",
        "group": "component",
        "files": [
            "path/to/file1.py",
            "path/to/file2.py"
        ]
        }
    ],
    "edges": [
        {
        "source": "component_1",
        "target": "component_2",
        "relation": "depends_on"
        }
    ]
    }

The nodes represent logical components of the repository.

The edges represent meaningful relationships between those
components.

Do not include Markdown.
Do not include ```json.
Do not include explanations outside the JSON.
"""

        return prompt