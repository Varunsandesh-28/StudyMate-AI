
import json
import re

import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from Tools import (
    explain_topic,
    important_questions,
    quick_revision,
    summarize_notes,
)
from Model import ask_ai


app = FastAPI(title="StudyMate AI - Offline Study Assistant")

templates = Jinja2Templates(directory="templates")


# --------------------------------------------------
# Request models
# --------------------------------------------------

class TeacherRequest(BaseModel):
    topic: str = ""
    mode: str = "explain"
    question: str = ""


class QuizRequest(BaseModel):
    topic: str


class SummaryRequest(BaseModel):
    notes: str


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
async def health():
    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=3,
        )
        response.raise_for_status()
        models = response.json().get("models", [])

        available = any(
            model.get("name", "").startswith("gemma3:1b")
            for model in models
        )

        return {
            "app": "StudyMate AI",
            "ollama_connected": True,
            "model_available": available,
            "model": "gemma3:1b",
            "offline_mode": True,
        }

    except requests.RequestException:
        return {
            "app": "StudyMate AI",
            "ollama_connected": False,
            "model_available": False,
            "offline_mode": True,
            "error": "Ollama is not running. Start Ollama and try again.",
        }


# --------------------------------------------------
# AI Teacher
# --------------------------------------------------

@app.post("/ai-teacher")
async def ai_teacher(data: TeacherRequest):
    topic = data.topic.strip()
    question = data.question.strip()
    mode = data.mode.strip().lower()

    try:
        if mode in ("explain", "explain topic"):
            if not topic:
                return {"error": "Please enter a topic."}
            answer = explain_topic(topic)

        elif mode in ("important", "important questions"):
            if not topic:
                return {"error": "Please enter a topic."}
            answer = important_questions(topic)

        elif mode in ("revision", "quick revision"):
            if not topic:
                return {"error": "Please enter a topic."}
            answer = quick_revision(topic)

        elif mode in ("doubt", "ask a doubt"):
            doubt = question or topic

            if not doubt:
                return {"error": "Please enter your question."}

            answer = ask_ai(
                "Answer this student's doubt in simple English. "
                "Explain step by step if needed. Be honest if unsure.\n\n"
                f"Student's question: {doubt}"
            )

        else:
            return {
                "error": (
                    "Unknown mode. Choose explain, important, "
                    "revision, or doubt."
                )
            }

        return {
            "success": True,
            "answer": answer,
            "response": answer,
        }

    except requests.RequestException:
        return {
            "error": (
                "Cannot connect to local Ollama. "
                "Please make sure Ollama is running."
            )
        }

    except Exception as exc:
        return {"error": f"AI Teacher error: {str(exc)}"}


# --------------------------------------------------
# AI Quiz Generator
# --------------------------------------------------

@app.post("/generate-quiz")
async def generate_quiz(data: QuizRequest):
    topic = data.topic.strip()

    if not topic:
        return {"error": "Please enter a quiz topic."}

    prompt = f"""
Create exactly 5 multiple-choice quiz questions about: {topic}

Use simple English. Return ONLY valid JSON, with this structure:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": 0,
      "explanation": "Short explanation"
    }}
  ]
}}

Rules:
- Exactly 5 questions.
- Each question has exactly 4 options.
- The answer is an integer from 0 to 3, indicating the correct option.
- Each question has only one correct answer.
- Explanations should be short and educational.
- Do not include Markdown fences or text outside the JSON.
"""

    try:
        raw = ask_ai(prompt)

        # Remove accidental Markdown code fences.
        cleaned = re.sub(
            r"^\s*```(?:json)?\s*|\s*```\s*$",
            "",
            raw,
            flags=re.IGNORECASE,
        )

        result = json.loads(cleaned)
        questions = result.get("questions", [])

        if not isinstance(questions, list):
            raise ValueError("Quiz questions were not returned as a list.")

        valid_questions = []

        for item in questions:
            if not isinstance(item, dict):
                continue

            question = item.get("question")
            options = item.get("options")
            answer = item.get("answer")
            explanation = item.get("explanation", "")

            if (
                isinstance(question, str)
                and isinstance(options, list)
                and len(options) == 4
                and all(isinstance(option, str) for option in options)
                and isinstance(answer, int)
                and not isinstance(answer, bool)
                and 0 <= answer <= 3
            ):
                valid_questions.append({
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "explanation": str(explanation),
                })

        if not valid_questions:
            return {
                "error": (
                    "The AI could not create a valid quiz. "
                    "Please try the topic again."
                )
            }

        return {
            "success": True,
            "topic": topic,
            "questions": valid_questions,
        }

    except json.JSONDecodeError:
        return {
            "error": (
                "The AI returned an invalid quiz format. "
                "Please generate the quiz again."
            )
        }

    except requests.RequestException:
        return {
            "error": (
                "Cannot connect to local Ollama. "
                "Please make sure Ollama is running."
            )
        }

    except Exception as exc:
        return {"error": f"Quiz generation error: {str(exc)}"}


# --------------------------------------------------
# Notes summarizer
# --------------------------------------------------

@app.post("/summarize-notes")
async def summarize_student_notes(data: SummaryRequest):
    notes = data.notes.strip()

    if not notes:
        return {"error": "Please enter or paste your notes."}

    try:
        summary = summarize_notes(notes)

        return {
            "success": True,
            "summary": summary,
            "answer": summary,
        }

    except requests.RequestException:
        return {
            "error": "Cannot connect to local Ollama. Please start Ollama."
        }

    except Exception as exc:
        return {"error": f"Summarization error: {str(exc)}"}
