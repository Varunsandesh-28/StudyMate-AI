
from Model import ask_ai


def explain_topic(topic: str) -> str:
    return ask_ai(
        f"Explain this topic for a beginner: {topic}. "
        "Include a definition, example, and recap."
    )


def important_questions(topic: str) -> str:
    return ask_ai(
        f"Generate 10 important practice questions about {topic}. "
        "Include short answers. Do not guarantee exam predictions."
    )


def quick_revision(topic: str) -> str:
    return ask_ai(
        f"Create simple, concise revision notes for {topic}. "
        "Use headings, key points, and examples."
    )


def summarize_notes(notes: str) -> str:
    return ask_ai(
        "Summarize the following student notes. "
        "Do not add unsupported facts.\n\n"
        f"NOTES:\n{notes}"
    )


def ask_doubt(question: str) -> str:
    return ask_ai(
        f"Answer this student's doubt in simple English: {question}"
    )
