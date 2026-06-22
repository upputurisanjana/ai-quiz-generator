# AI-Powered Quiz Generator — Specification

**Course:** AI Application Development — Academic Year 2025–26
**Type:** Student Homework Build
**Status:** Draft v1.0

---

## 1. Overview

The AI Quiz Generator is a web application that transforms any PowerPoint (`.pptx`) file into an interactive, scored multiple-choice quiz. The system extracts text content from uploaded slides, sends it to an LLM to generate well-formed MCQs at a chosen difficulty, presents them through an interactive quiz UI, and scores the user's answers with AI-generated explanations for incorrect responses.

### 1.1 Problem Statement

- **Manual effort** — creating quiz questions from slides by hand is slow and tedious for educators.
- **No feedback loop** — students get a score but no explanation of *why* an answer was wrong.
- **One-size-fits-all** — most tools don't support adaptive difficulty levels.

### 1.2 Goals

| # | Goal |
|---|------|
| 1 | Accept a `.pptx` file as the AI input source |
| 2 | Let users choose number of questions (5–30) |
| 3 | Support three difficulty levels: Simple, Medium, Complex |
| 4 | Generate well-formed MCQs via AI (exactly 4 options each) |
| 5 | Deliver an interactive, single-question-at-a-time quiz interface |
| 6 | Score answers and explain *why* incorrect options are wrong |

---

## 2. Scope

### 2.1 In Scope
- PPT/PPTX file upload and parsing
- AI-driven MCQ generation
- Difficulty level filtering (Simple / Medium / Complex)
- Timed, interactive quiz UI
- Score calculation + detailed AI feedback on wrong answers

### 2.2 Out of Scope
- Video/audio file inputs
- Essay or open-ended question types
- User authentication / accounts
- Multi-language support

---

## 3. Application Workflow

```
1. Upload PPT        → User uploads a .pptx file
2. Configure Quiz    → User selects question count & difficulty
3. AI Generates MCQs → LLM reads extracted slide text, crafts questions + 4 options
4. Take Quiz         → User answers each question interactively
5. Results & Feedback→ Score shown + correct answers + AI explains errors
```

### 3.1 Key Technical Considerations
- Parse PowerPoint content using `python-pptx` (or equivalent) to extract slide text.
- Use an LLM (e.g., Claude, GPT, or an OpenRouter free-tier model) to generate MCQs of varying difficulty from the extracted text.
- Build a responsive front-end (React or HTML/CSS, or Streamlit for rapid prototyping) with real-time quiz interaction and feedback display.

---

## 4. Functional Requirements

### FR-01 — PPT File Input
- Accept `.pptx` uploads via a file picker (drag-and-drop and "browse" click).
- Reject non-`.pptx` files with a clear, visible error state.
- Enforce a max file size (recommended: 25 MB).
- Extract all text content from every slide.
- Display slide count and a content preview before proceeding.
- Disable the "Continue" action until parsing succeeds.

### FR-02 — Quiz Configuration
- Numeric input or slider for number of questions, clamped to **min 5 / max 30**.
- Difficulty selector: **Simple / Medium / Complex** (single-select).
- "Generate Quiz" button triggers AI processing using slide text + selected settings.
- Show the active source file (filename + slide count) for context.

### FR-03 — MCQ Generation
- AI generates questions relevant to the actual slide content (no generic filler).
- Each question has **exactly 4 options (A–D)**.
- Exactly **one correct answer**; the remaining three are plausible distractors.
- Question difficulty should visibly map to the selected level (recall vs. scenario-based reasoning).
- Display a loading indicator while generation is in progress.

### FR-04 — Quiz Interface
- Display **one question at a time** (or paginated equivalent).
- Show progress (e.g., "Question 3 of 10") and an optional countdown timer.
- Allow exactly one answer selection per question; highlight the chosen option.
- Provide Previous / Next navigation; final question shows a Submit action.

### FR-05 — Scoring & Feedback
- On completion, show final score as **X / Total** and a percentage.
- For each question, display the user's selected answer vs. the correct answer.
- For every incorrect answer, show an AI-generated explanation of *why* the chosen option is wrong and why the correct option is right.
- Offer "Retake Quiz" and "Upload New PPT" actions.

### FR-06 — UX Requirements
- Clean, mobile-friendly, responsive UI across all screens.
- Clear loading indicators during AI generation steps.
- No dead ends — every screen has a clear next action.

---

## 5. Question Design Guidelines

All AI-generated questions should satisfy the following to ensure they test genuine understanding rather than memorization:

1. **Plausible options** — every option should carry enough surface correctness that it can't be dismissed outright, yet only one is fully defensible.
2. **Balanced length & specificity** — the correct answer should not always be the longest or most detailed option.
3. **"Best among goods" ambiguity** — multiple options may seem reasonable, but only one is most defensible given the question's constraints.
4. **Subtle distinctions** — telling options apart should require real subject-matter understanding, not just careful reading.
5. **Full syllabus coverage** — questions should be distributed across all slides/topics, not clustered on a few.
6. **Scenario-based preference** — favor qualitative, judgment-based questions over simple factual recall where possible.
7. **Verified answer key** — the marked-correct answer must be unambiguously correct with no defensible alternate interpretation.

**The goal:** reward genuine reasoning, not memorization — a well-prepared student should still have to think.

---

## 6. UI Reference Mockups

The build must match the layout, controls, states, and feedback patterns of these four reference screens:

| Screen | Key Elements |
|--------|-------------|
| **1. Upload & Parse PPT** | Drag-and-drop file picker, `.pptx`-only validation, parse confirmation (slide count + word count), disabled Continue until ready |
| **2. Configure Quiz** | Source file summary, question-count slider (5–30), difficulty toggle (Simple/Medium/Complex), "Generate Quiz" CTA |
| **3. Take the Quiz** | One question + 4 options (A–D), single selection with highlight, progress bar + timer, Previous/Next navigation |
| **4. Results & Feedback** | Score ring (X/Total + %), correct/wrong counts, per-question review with AI explanations on misses, Retake/Upload New actions |

---

## 7. Data Model (Suggested)

```python
# Question object
{
  "id": str,
  "question_text": str,
  "options": {"A": str, "B": str, "C": str, "D": str},
  "correct_answer": str,        # one of "A" | "B" | "C" | "D"
  "difficulty": str,            # "simple" | "medium" | "complex"
  "source_slide": int,          # slide number referenced
  "explanation": str            # why correct answer is right (used for feedback)
}

# Quiz session
{
  "source_file": str,
  "slide_count": int,
  "question_count": int,
  "difficulty": str,
  "questions": list[Question],
  "user_answers": dict[str, str],   # question_id -> selected option
  "score": int,
  "total": int
}
```

---

## 8. Evaluation Criteria

| Evaluation Area | Weight | Success Criterion |
|---|---|---|
| PPT Parsing & Input | 15% | Accurate text extraction from all slides |
| AI MCQ Generation | 25% | Relevant, well-formed questions at correct difficulty |
| Quiz UI / UX | 20% | Responsive, intuitive, error-free interface |
| Scoring Accuracy | 15% | Correct score computation and answer display |
| AI Feedback Quality | 15% | Clear, meaningful explanations for wrong answers |
| Code Quality & Docs | 10% | Clean code, README, inline comments |

---

## 9. Deliverables

- [ ] Source code (GitHub repository)
- [ ] Working demo / deployed URL
- [ ] Project report (PDF)
- [ ] 5-minute video demo

---

## 10. Open Questions / Assumptions

- **Front-end framework:** mockups suggest a web app; Streamlit is an acceptable rapid-build alternative to React/HTML-CSS for this homework context.
- **Timer behavior:** spec marks the countdown timer as optional ("Show position... and an optional countdown") — confirm whether it's required for full UX credit.
- **LLM provider:** any capable LLM is acceptable per the brief (Claude, GPT, or free-tier OpenRouter models); confirm rate limits are sufficient for batch MCQ generation up to 30 questions.
- **Distractor verification:** consider a validation pass (rule-based or a second LLM call) to confirm exactly one unambiguous correct answer per question before presenting it to the user.
