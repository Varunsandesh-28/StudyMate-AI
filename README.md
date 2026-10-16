# 📚 StudyMate AI

**Your Personal AI-Powered Study Assistant**

StudyMate AI is a locally powered AI study assistant designed to help students understand concepts, prepare for exams, practise questions, and revise notes using AI.

## ✨ Features

- 🤖 **AI Teacher** — Get simple explanations of difficult topics.
- 📝 **Important Questions** — Generate practice questions with answers.
- ⚡ **Quick Revision** — Create short revision notes.
- 🎯 **AI Quiz Generator** — Practise multiple-choice questions and check your score.
- 📄 **Notes Summarizer** — Summarize study notes quickly.
- 💻 **Local AI** — Uses Ollama with the Gemma 3 1B model to run AI locally.

## 🛠️ Technologies Used

- Python
- FastAPI
- HTML, CSS, JavaScript
- Ollama
- Gemma 3 1B

## 📋 Prerequisites

Install the following before running the project:

- Python 3.12 or a compatible Python version
- [Ollama](https://ollama.com/)
- Git (optional, for cloning the repository)

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/StudyMate-AI.git
cd StudyMate-AI
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn jinja2 requests python-multipart
```

### 3. Install dependencies

```bash
python -m pip install fastapi uvicorn jinja2 requests python-multipart
```

### 4. Download the AI model

```bash
ollama pull gemma3:1b
```

Make sure Ollama is running on your computer.

### 5. Start the application

```bash
python -m uvicorn webapp:app --reload
```

Open your browser and visit:

**http://127.0.0.1:8000**

## 📂 Project Structure

```text
StudyMate-AI/
├── Model.py
├── Tools.py
├── Skill.md
├── app.py
├── webapp.py
├── pdf_summary.py
├── templates/
│   └── index.html
├── .gitignore
└── README.md
```

## 🔒 Privacy

AI requests are processed using the local Ollama model. StudyMate AI is designed to work without a cloud AI API once the required software and model are installed. Internet access may still be needed for initial setup and downloading dependencies.

## 🎯 Project Goal

Our goal is to make studying simpler and more interactive by combining AI explanations, quiz generation, and note summarization in one student-friendly platform.

## 👨‍💻 Contributing

Suggestions, bug reports, and improvements are welcome!

## 📜 License

No license has been selected yet. Add an appropriate open-source license if you want others to reuse or modify this project under defined terms.
