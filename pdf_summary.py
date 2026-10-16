
from pypdf import PdfReader
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    return text


def summarize_text(text):
    prompt = f"""
You are StudyMate AI, a helpful study assistant.

Summarize these study notes in simple English.
Use headings and bullet points.
Include important definitions and concepts.
Do not invent information that is missing from the notes.

STUDY NOTES:
{text[:12000]}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    return response.json()["response"]


def main():
    print("📚 Welcome to StudyMate AI PDF Summarizer!")

    file_path = input("Enter your PDF file path: ").strip().strip('"')

    try:
        notes = read_pdf(file_path)

        if not notes.strip():
            print("No readable text found in this PDF.")
            return

        print("\n🤖 Generating your summary...\n")
        summary = summarize_text(notes)
        print(summary)

    except FileNotFoundError:
        print("PDF file not found. Please check the file path.")

    except requests.exceptions.ConnectionError:
        print("Cannot connect to Ollama. Make sure Ollama is running.")

    except requests.exceptions.Timeout:
        print("AI is taking too long. Please try again.")

    except Exception as error:
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()
