import streamlit as st
import time
from utils import inject_css, init_state, generate_questions

st.set_page_config(page_title="Scholarium — Loading", page_icon="📜", layout="wide")
init_state()
inject_css()

if not st.session_state.ppt_data:
    st.switch_page("pages/upload.py")

ppt = st.session_state.ppt_data
cfg = st.session_state.quiz_config
num_q = cfg["num_questions"]
fd = cfg["difficulty"]

status = st.empty()
for m in [f"Consulting {ppt['slides']} folios…", "Analysing scholarly content…",
          f"Composing {num_q} questions…", "Inscribing elucidations…"]:
    status.markdown(f"""<div style="height:80vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
  <div style="font-family:var(--fh);font-size:32px;font-weight:400;color:var(--fg);margin-bottom:8px">Composing your examination</div>
  <div style="font-family:var(--fb);font-size:15px;color:var(--mfg);margin-bottom:20px;font-style:italic">{m}</div>
  <div class="ac-lbar" style="max-width:320px;width:100%"><div class="ac-lbarf"></div></div>
</div>""", unsafe_allow_html=True)
    time.sleep(0.4)

st.session_state.questions = generate_questions(ppt, num_q, fd)
st.switch_page("pages/quiz.py")
