import streamlit as st
from pptx import Presentation
import os
import json
import time
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ============================================================================
# DESIGN SYSTEM
# ============================================================================
ACCENT = "#FF6B4A"
LIGHT_BG = "#FAFAF8"
LIGHT_TEXT = "#1A1A1A"
DARK_BG = "#1C1E26"
DARK_TEXT = "#E8E8E8"
SUCCESS = "#00C48C"
ERROR = "#FF4757"

def inject_custom_css():
    theme = st.session_state.get("theme", "light")
    bg = LIGHT_BG if theme == "light" else DARK_BG
    text = LIGHT_TEXT if theme == "light" else DARK_TEXT
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp {{
        background: {bg};
        color: {text};
        font-family: 'Inter', sans-serif;
        transition: background 0.25s ease, color 0.25s ease;
    }}
    
    /* Typography hierarchy */
    .display {{
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.1;
        color: {text};
    }}
    
    .body {{
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.6;
        color: {text};
    }}
    
    .mono {{
        font-family: 'SF Mono', 'Consolas', monospace;
        font-variant-numeric: tabular-nums;
        letter-spacing: -0.01em;
    }}
    
    /* Accent button */
    .accent-btn {{
        background: {ACCENT};
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    
    .accent-btn:hover {{
        transform: scale(1.03);
    }}
    
    .accent-btn:active {{
        transform: scale(0.98);
    }}
    
    /* Card container */
    .card {{
        background: {"white" if theme == "light" else "#252830"};
        border: 1px solid {"#E8E8E8" if theme == "light" else "#3A3D4A"};
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 2px 8px {"rgba(0,0,0,0.04)" if theme == "light" else "rgba(0,0,0,0.2)"};
        transition: all 0.25s ease;
    }}
    
    /* Option button */
    .option {{
        background: {"white" if theme == "light" else "#252830"};
        border: 2px solid {"#E8E8E8" if theme == "light" else "#3A3D4A"};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.15s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-align: left;
    }}
    
    .option:hover {{
        border-color: {ACCENT};
        transform: translateX(4px);
    }}
    
    .option.selected {{
        border-color: {ACCENT};
        background: {ACCENT}15;
        transform: scale(1.03);
    }}
    
    .option.correct {{
        border-color: {SUCCESS};
        background: {SUCCESS}15;
    }}
    
    .option.incorrect {{
        border-color: {ERROR};
        background: {ERROR}15;
    }}
    
    /* Theme toggle */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: {"white" if theme == "light" else "#252830"};
        border: 1px solid {"#E8E8E8" if theme == "light" else "#3A3D4A"};
        border-radius: 8px;
        padding: 0.5rem;
        cursor: pointer;
        font-size: 1.25rem;
        transition: transform 0.15s ease;
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.1);
    }}
    
    /* Progress bar */
    .progress-container {{
        width: 100%;
        height: 6px;
        background: {"#E8E8E8" if theme == "light" else "#3A3D4A"};
        border-radius: 3px;
        overflow: hidden;
        margin: 1rem 0;
    }}
    
    .progress-bar {{
        height: 100%;
        background: {ACCENT};
        transition: width 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    
    /* Explanation panel */
    .explanation {{
        background: {"#F5F5F3" if theme == "light" else "#1A1C22"};
        border-left: 4px solid {ACCENT};
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        animation: slideDown 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    
    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* Timer warning */
    .timer-warning {{
        color: {ERROR};
        animation: pulse 1s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}
    
    /* Reduce motion support */
    @media (prefers-reduced-motion: reduce) {{
        * {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "screen" not in st.session_state:
    st.session_state.screen = "upload"
if "ppt_data" not in st.session_state:
    st.session_state.ppt_data = None
if "quiz_config" not in st.session_state:
    st.session_state.quiz_config = {}
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def parse_pptx(uploaded_file):
    """Extract text from PPTX"""
    prs = Presentation(uploaded_file)
    slides = []
    for i, slide in enumerate(prs.slides):
        text = []
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
        slides.append({"slide_num": i + 1, "content": "\n".join(text)})
    return {
        "filename": uploaded_file.name,
        "slide_count": len(slides),
        "word_count": sum(len(s["content"].split()) for s in slides),
        "slides": slides
    }

def generate_questions(ppt_data, num_questions, difficulty, timed):
    """Generate MCQs using OpenRouter API"""
    from openai import OpenAI
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        st.error("OPENROUTER_API_KEY not found. Check your .env file.")
        st.stop()
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

    all_text = "\n\n".join([f"Slide {s['slide_num']}: {s['content']}" for s in ppt_data["slides"]])

    prompt = f"""Generate {num_questions} multiple-choice questions from this PowerPoint content at {difficulty} difficulty level.

Content:
{all_text}

Return ONLY a valid JSON array, no markdown, no explanation.
IMPORTANT: explanation_wrong must contain keys for ALL 3 incorrect options.
[{{
  "id": "q1",
  "question_text": "...",
  "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
  "correct_answer": "A",
  "source_slide": 1,
  "explanation_correct": "Why A is right...",
  "explanation_wrong": {{"B": "Why B is wrong...", "C": "Why C is wrong...", "D": "Why D is wrong..."}}
}}]"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content
    json_start = content.find("[")
    json_end = content.rfind("]") + 1
    return json.loads(content[json_start:json_end])

def calculate_time_estimate(num_questions, difficulty):
    """Calculate total quiz time"""
    time_per_q = {"simple": 35, "medium": 67, "complex": 105}[difficulty.lower()]
    total_seconds = num_questions * time_per_q
    minutes = total_seconds // 60
    return minutes

# ============================================================================
# SCREEN: UPLOAD & PARSE
# ============================================================================
def screen_upload():
    st.markdown('<div class="display">Upload Presentation</div>', unsafe_allow_html=True)
    st.markdown('<p class="body">Drop your .pptx file to generate quiz questions</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a PPTX file", type=["pptx"], label_visibility="collapsed")
    
    if uploaded_file:
        with st.spinner("Parsing slides..."):
            ppt_data = parse_pptx(uploaded_file)
            st.session_state.ppt_data = ppt_data
        
        st.markdown(f"""
        <div class="card" style="margin-top: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; font-size: 1.1rem;">{ppt_data['filename']}</div>
                    <div class="mono" style="color: {ACCENT}; margin-top: 0.5rem; font-size: 0.9rem;">
                        {ppt_data['slide_count']} slides · {ppt_data['word_count']} words
                    </div>
                </div>
                <div style="background: {ACCENT}15; color: {ACCENT}; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                    ✓ Ready
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue to Configuration →", type="primary", use_container_width=True):
            st.session_state.screen = "configure"
            st.rerun()

# ============================================================================
# SCREEN: CONFIGURE QUIZ
# ============================================================================
def screen_configure():
    st.markdown('<div class="display">Configure Quiz</div>', unsafe_allow_html=True)
    
    ppt = st.session_state.ppt_data
    st.markdown(f"""
    <div style="background: {ACCENT}15; padding: 0.75rem 1rem; border-radius: 12px; margin: 1rem 0;">
        <span style="font-weight: 600;">{ppt['filename']}</span>
        <span class="mono" style="margin-left: 1rem; color: {ACCENT};">
            {ppt['slide_count']} slides
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_questions = st.slider("Number of Questions", 5, 30, 10, key="num_q")
    
    with col2:
        difficulty = st.selectbox("Difficulty", ["Simple", "Medium", "Complex"], key="diff")
    
    # Timed/Untimed toggle
    st.markdown("### Quiz Mode")
    timed_mode = st.radio("", ["Timed", "Untimed"], horizontal=True, label_visibility="collapsed")
    is_timed = timed_mode == "Timed"
    
    if is_timed:
        time_estimate = calculate_time_estimate(num_questions, difficulty)
        st.markdown(f"""
        <div class="mono" style="color: {ACCENT}; font-size: 1.25rem; margin-top: 1rem;">
            ≈ {time_estimate} min
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("Generate Quiz", type="primary", use_container_width=True):
        with st.spinner("AI is crafting questions..."):
            questions = generate_questions(ppt, num_questions, difficulty, is_timed)
            st.session_state.questions = questions
            st.session_state.quiz_config = {
                "num_questions": num_questions,
                "difficulty": difficulty,
                "timed": is_timed,
                "time_per_question": {"simple": 35, "medium": 67, "complex": 105}[difficulty.lower()] if is_timed else None
            }
            st.session_state.screen = "quiz"
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.timer_start = time.time() if is_timed else None
            st.rerun()

# ============================================================================
# SCREEN: QUIZ
# ============================================================================
def screen_quiz():
    q_idx = st.session_state.current_question
    question = st.session_state.questions[q_idx]
    config = st.session_state.quiz_config
    total = len(st.session_state.questions)
    
    # Progress bar
    progress = (q_idx + 1) / total * 100
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="mono" style="font-size: 0.9rem; color: {ACCENT};">Question {q_idx + 1} of {total}</div>', unsafe_allow_html=True)
    
    with col2:
        if config["timed"]:
            elapsed = int(time.time() - st.session_state.timer_start)
            q_time = config["time_per_question"]
            remaining = q_time - (elapsed % q_time)
            warning_class = "timer-warning" if remaining <= q_time * 0.1 else ""
            st.markdown(f'<div class="mono {warning_class}" style="text-align: right; font-size: 0.9rem;">{remaining}s</div>', unsafe_allow_html=True)
    
    # Question card
    st.markdown(f"""
    <div class="card" style="margin: 2rem 0;">
        <div class="body" style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1.5rem;">
            {question['question_text']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Options
    selected = st.session_state.user_answers.get(question["id"])

    for opt_key, opt_text in question["options"].items():
        is_selected = selected == opt_key
        if st.button(f"{opt_key}. {opt_text}", key=f"opt_{opt_key}", use_container_width=True):
            st.session_state.user_answers[question["id"]] = opt_key
            st.rerun()

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if q_idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    with col2:
        if q_idx < total - 1:
            if st.button("Next →", type="primary", use_container_width=True, disabled=not selected):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("Submit Quiz →", type="primary", use_container_width=True, disabled=not selected):
                st.session_state.screen = "results"
                st.rerun()

# ============================================================================
# SCREEN: RESULTS
# ============================================================================
def screen_results():
    questions = st.session_state.questions
    answers = st.session_state.user_answers
    
    correct_count = sum(1 for q in questions if answers.get(q["id"]) == q["correct_answer"])
    total = len(questions)
    percentage = int(correct_count / total * 100)
    
    st.markdown('<div class="display">Results</div>', unsafe_allow_html=True)
    
    # Score display
    st.markdown(f"""
    <div class="card" style="text-align: center; margin: 2rem 0;">
        <div class="mono" style="font-size: 4rem; font-weight: 700; color: {ACCENT};">
            {correct_count}/{total}
        </div>
        <div class="mono" style="font-size: 1.5rem; color: {st.session_state.theme == 'light' and '#666' or '#999'};">
            {percentage}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Question review
    st.markdown("### Question Review")
    
    for i, q in enumerate(questions):
        user_ans = answers.get(q["id"])
        correct_ans = q["correct_answer"]
        is_correct = user_ans == correct_ans
        
        with st.expander(f"{'✓' if is_correct else '✗'} Question {i + 1}: {q['question_text'][:60]}..."):
            if is_correct:
                st.markdown(f"**Your answer:** ✓ {user_ans}. {q['options'][user_ans]}")
                st.success(q['explanation_correct'])
            else:
                st.markdown(f"**Your answer:** ✗ {user_ans}. {q['options'].get(user_ans, '—')}")
                st.markdown(f"**Correct answer:** ✓ {correct_ans}. {q['options'][correct_ans]}")
                st.error(q['explanation_wrong'].get(user_ans, '—'))
                st.success(q['explanation_correct'])
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retake Quiz", use_container_width=True):
            st.session_state.screen = "quiz"
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.show_explanation = False
            st.session_state.timer_start = time.time() if st.session_state.quiz_config["timed"] else None
            st.rerun()
    
    with col2:
        if st.button("Upload New PPT", type="primary", use_container_width=True):
            st.session_state.screen = "upload"
            st.session_state.ppt_data = None
            st.session_state.questions = []
            st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    st.set_page_config(page_title="AI Quiz Generator", layout="wide", initial_sidebar_state="collapsed")
    inject_custom_css()
    
    # Theme toggle
    theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
    if st.button(theme_icon, key="theme_toggle"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()
    
    # Route to appropriate screen
    if st.session_state.screen == "upload":
        screen_upload()
    elif st.session_state.screen == "configure":
        screen_configure()
    elif st.session_state.screen == "quiz":
        screen_quiz()
    elif st.session_state.screen == "results":
        screen_results()

if __name__ == "__main__":
    main()
