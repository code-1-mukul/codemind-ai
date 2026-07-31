from app.services.question_answer_service import QuestionAnswerService

repository_name = "facialRecog"

question = "How does encodings work?"

service = QuestionAnswerService()

response = service.answer_question(
    repository_name=repository_name,
    question=question,
)

print("\n" + "=" * 80)
print("FINAL ANSWER")
print("=" * 80)
print(response["answer"])