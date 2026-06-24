import streamlit as st
import time
from utils import inject_css, init_state, _TIME_PER_Q

st.set_page_config(page_title="Scholarium — Configure", page_icon="📜", layout="wide")
init_state()
inject_css()

if not st.session_state.ppt_data:
    st.switch_page("pages/upload.py")

ppt = st.session_state.ppt_data
cfg = st.session_state.quiz_config
diff = cfg.get("difficulty", "Medium")
is_timed = cfg.get("timed", False)

st.markdown(f'<div class="ac-chip">📎 &nbsp;{ppt["filename"]}</div>', unsafe_allow_html=True)
st.markdown("""
<div class="ac-overline" style="margin-bottom:8px">Volume II</div>
<div class="ac-h1">Configure<br><em>Your Examination</em></div>
<div class="ac-sub">Set the breadth, rigour, and conditions of the test.</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([2, 1], gap="large")
with c1:
    st.markdown('<div class="ac-overline" style="margin-bottom:12px">Number of Questions</div>', unsafe_allow_html=True)
    num_q = st.slider("", 1, 30, cfg.get("num_questions", 10), key="cfg_n", label_visibility="collapsed")

    st.markdown('<div class="ac-overline" style="margin-top:24px;margin-bottom:12px">Difficulty</div>', unsafe_allow_html=True)
    dc = st.columns(3)
    for i, d in enumerate(["Simple", "Medium", "Complex"]):
        with dc[i]:
            if st.button(d, key=f"d_{d}", use_container_width=True,
                         type="primary" if d == diff else "secondary"):
                st.session_state.quiz_config["difficulty"] = d; st.rerun()

    st.markdown('<div class="ac-overline" style="margin-top:24px;margin-bottom:12px">Examination Mode</div>', unsafe_allow_html=True)
    tc = st.columns(2)
    for mode_label, mode_val, col in [("⏱  Timed", True, tc[0]), ("∞  Untimed", False, tc[1])]:
        with col:
            if st.button(mode_label, key=f"m_{mode_val}", use_container_width=True,
                         type="primary" if is_timed == mode_val else "secondary"):
                st.session_state.quiz_config["timed"] = mode_val; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Compose the Examination →", use_container_width=True, type="primary"):
        fd = cfg.get("difficulty", "Medium")
        ft = cfg.get("timed", False)
        st.session_state.quiz_config.update({
            "num_questions": num_q, "difficulty": fd, "timed": ft,
            "time_per_question": _TIME_PER_Q[fd] if ft else None,
        })
        st.session_state.current_question = 0
        st.session_state.user_answers = {}
        st.session_state.confirmed_answers = {}
        st.session_state.timer_start = time.time() if ft else None
        st.switch_page("pages/loading.py")

with c2:
    fd = cfg.get("difficulty", "Medium")
    ft = cfg.get("timed", False)
    tpq = _TIME_PER_Q[fd]
    total_s = num_q * tpq
    m_t, s_t = divmod(total_s, 60)
    st.markdown(f"""<div class="ac-inset">
  <div class="ac-overline" style="margin-bottom:14px">Duration Estimate</div>
  <div style="font-family:var(--fh);font-size:40px;font-weight:400;color:var(--ac);line-height:1">
    {m_t:02d}<span style="font-family:var(--fd);font-size:13px;color:var(--mfg)"> min </span>{s_t:02d}<span style="font-family:var(--fd);font-size:13px;color:var(--mfg)"> sec</span>
  </div>
  <div style="font-family:var(--fb);font-size:13px;color:var(--mfg);margin-top:6px">{'Timed' if ft else 'Untimed'} &middot; {tpq}s per question</div>
  <div class="ac-div" style="margin:18px 0"></div>
  <div style="font-family:var(--fb);font-size:14px;color:var(--mfg);line-height:2">
    Simple &nbsp;<span style="font-family:var(--fh);color:var(--fg)">~ 35 s/q</span><br>
    Medium &nbsp;<span style="font-family:var(--fh);color:var(--fg)">~ 67 s/q</span><br>
    Complex <span style="font-family:var(--fh);color:var(--fg)">~ 105 s/q</span>
  </div>
</div>""", unsafe_allow_html=True)
