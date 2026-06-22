# AI Quiz Generator — Streamlit Frontend

Transforms PowerPoint presentations into interactive MCQ quizzes with AI-generated questions and explanations.

## Features

### 1. Upload & Parse Screen
- Drag-and-drop `.pptx` validation
- Slide count & word count preview

### 2. Configure Quiz Screen
- Question count slider (5–30)
- Difficulty selector (Simple/Medium/Complex)
- Timed/Untimed toggle with live time estimation

### 3. Quiz Screen
- Single question display with 4 options
- Progress bar with question counter
- Conditional timer (timed mode only)
- Per-answer explanations with correct/wrong highlighting

### 4. Results Screen
- Score display
- Question-by-question review
- Retake/Upload New actions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set Claude API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

3. Run:
```bash
streamlit run app.py
```
