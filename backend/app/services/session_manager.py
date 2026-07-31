from app.schemas.chat import ChatMessage
import uuid

class SessionManager:

    def __init__(self):
        self.sessions: dict[str, list[ChatMessage]] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id]=[]
        return session_id

    def get_history(self, session_id: str) -> list[ChatMessage]:
        return self.sessions.get(session_id,[])

    def add_message(self, session_id: str, message: ChatMessage):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(message)

    def clear_session(self, session_id: str):
        self.sessions.pop(session_id,None)

session_manager = SessionManager()