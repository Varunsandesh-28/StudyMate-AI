
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"


def ask_ai(prompt):
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


def generate_quiz(topic):
    prompt = f"""
Create exactly 5 beginner multiple-choice questions about {topic}.

Return ONLY valid JSON in this format:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "answer": "A",
      "explanation": "Short explanation"
    }}
  ]
}}

Rules:
- The answer must be one letter: A, B, C, or D.
- Each question must have four different options.
- Make sure the answer matches the explanation.
- Do not include Markdown or text outside the JSON.
"""

    result = ask_ai(prompt)

    # Extract JSON if the model adds extra text.
    start = result.find("{")
    end = result.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("AI did not return valid JSON.")

    data = json.loads(result[start:end + 1])
    questions = data.get("questions", [])

    if len(questions) != 5:
        raise ValueError("AI did not generate exactly 5 questions.")

    for question in questions:
        if question.get("answer") not in ["A", "B", "C", "D"]:
            raise ValueError("A question has an invalid answer key.")

        if not all(
            key in question.get("options", {})
            for key in ["A", "B", "C", "D"]
        ):
            raise ValueError("A question is missing options.")

    return questions


def play_quiz(questions):
    score = 0
    total = len(questions)

    for number, question in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {question['question']}")

        for letter, option in question["options"].items():
            print(f"{letter}. {option}")

        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()

            if answer in ["A", "B", "C", "D"]:
                break

            print("Please enter A, B, C, or D.")

        correct_answer = question["answer"]

        if answer == correct_answer:
            print("Correct! 🎉")
            score += 1
        else:
            print("Not quite!")

        print("Correct answer:", correct_answer)
        print("Explanation:", question["explanation"])

    percentage = (score / total) * 100

    print("\n" + "=" * 35)
    print("       QUIZ RESULTS")
    print("=" * 35)
    print(f"Score: {score}/{total}")
    print(f"Percentage: {percentage:.0f}%")

    if score == total:
        print("Excellent work, mawa! 🏆")
    elif score >= 3:
        print("Good job! Keep practising. 💪")
    else:
        print("Keep learning. You can improve! 📚")


def main():
    print("=" * 35)
    print("       STUDYMATE AI")
    print("     INTERACTIVE QUIZ")
    print("=" * 35)

    topic = input("\nEnter a topic to study: ").strip()

    if not topic:
        print("Please enter a topic.")
        return

    try:
        print("\nGenerating your quiz... Please wait!")
        questions = generate_quiz(topic)
        play_quiz(questions)

    except requests.exceptions.ConnectionError:
        print("Cannot connect to Ollama. Check if it is running.")

    except requests.exceptions.Timeout:
        print("AI took too long. Please try again.")

    except (ValueError, json.JSONDecodeError) as error:
        print("Quiz generation failed:", error)
        print("Please run the program again.")

    except requests.exceptions.RequestException as error:
        print("AI request failed:", error)

    except Exception as error:
        print("Something went wrong:", error)


if __name__ == "__main__":
    main()
