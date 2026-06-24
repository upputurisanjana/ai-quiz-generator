import streamlit as st
import time, math
from utils import inject_css, init_state

st.set_page_config(page_title="Scholarium — Quiz", page_icon="📜", layout="wide")
init_state()
inject_css()

if not st.session_state.questions:
    st.switch_page("pages/upload.py")

qs = st.session_state.questions
qi = st.session_state.current_question
q = qs[qi]
cfg = st.session_state.quiz_config
total = len(qs)
sel = st.session_state.user_answers.get(q["id"])
pct = (qi + 1) / total * 100

st.markdown(f"""<div style="display:flex;align-items:center;gap:16px;margin-bottom:28px">
  <div class="ac-prog" style="flex:1"><div class="ac-progf" style="width:{pct}%"></div></div>
  <div style="font-family:var(--fd);font-size:10px;font-weight:500;color:var(--mfg);white-space:nowrap;letter-spacing:.15em">{qi+1:02d} / {total:02d}</div>
</div>""", unsafe_allow_html=True)

c1, c2 = st.columns([2, 1], gap="large")
with c1:
    st.markdown(f"""<div class="ac-card" style="margin-bottom:18px">
  <div class="ac-overline" style="margin-bottom:10px">Question {qi+1}</div>
  <div style="font-family:var(--fh);font-size:24px;font-weight:400;line-height:1.3;color:var(--fg)">{q['question_text']}</div>
</div>""", unsafe_allow_html=True)

    with st.container(key="quiz_options"):
        for k, txt in q["options"].items():
            if st.button(f"{k}   {txt}", key=f"o_{qi}_{k}", use_container_width=True,
                         type="primary" if k == sel else "secondary"):
                st.session_state.user_answers[q["id"]] = k; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    nc1, nc2 = st.columns(2)
    with nc1:
        if qi > 0 and st.button("← Back", key=f"bk_{qi}", use_container_width=True):
            st.session_state.current_question -= 1; st.rerun()
    with nc2:
        if qi < total - 1:
            if st.button("Next →", key=f"nx_{qi}", use_container_width=True):
                st.session_state.current_question += 1; st.rerun()
        else:
            if st.button("View Results →", key="res", use_container_width=True):
                st.switch_page("pages/results.py")

with c2:
    if cfg.get("timed") and st.session_state.timer_start:
        elapsed = int(time.time() - st.session_state.timer_start)
        total_time = cfg["time_per_question"] * total
        rem = max(0, total_time - elapsed)
        frac = rem / total_time if total_time else 0
        urg = rem < 30
        mins, secs = divmod(rem, 60)
        R = 30; circ = 2 * math.pi * R; off = circ * (1 - frac)
        stk = "#B87070" if urg else "var(--ac)"
        st.markdown(f"""<div class="ac-inset" style="text-align:center;margin-bottom:14px">
  <div class="ac-overline" style="text-align:center;margin-bottom:12px">Time Remaining</div>
  <div class="ac-tw">
    <svg style="transform:rotate(-90deg)" width="72" height="72" viewBox="0 0 72 72">
      <circle fill="none" stroke="var(--muted)" stroke-width="3" cx="36" cy="36" r="{R}"/>
      <circle fill="none" stroke="{stk}" stroke-width="3" stroke-linecap="round"
        cx="36" cy="36" r="{R}" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{off:.1f}"
        style="transition:stroke-dashoffset .9s linear,stroke .3s ease"/>
    </svg>
    <div class="ac-tn {'urg' if urg else ''}">{mins:02d}:{secs:02d}</div>
  </div>
  <div style="font-family:var(--fd);font-size:9px;letter-spacing:.2em;color:var(--mfg)">REMAINING</div>
</div>""", unsafe_allow_html=True)
        if rem == 0:
            st.switch_page("pages/results.py")
        else:
            time.sleep(1); st.rerun()

    answered = st.session_state.user_answers
    st.markdown('<div class="ac-inset"><div class="ac-overline" style="margin-bottom:12px">Questions</div>', unsafe_allow_html=True)
    cols_per_row = 5
    for row_start in range(0, total, cols_per_row):
        row_qs = list(range(row_start, min(row_start + cols_per_row, total)))
        row_cols = st.columns(cols_per_row)
        for col_i in range(cols_per_row):
            with row_cols[col_i]:
                if col_i < len(row_qs):
                    i = row_qs[col_i]
                    is_cur = i == qi
                    is_ans = qs[i]["id"] in answered
                    with st.container(key=f"qngrid_{i}"):
                        label = f"◆{i+1}" if is_ans and not is_cur else str(i + 1)
                        if st.button(label, key=f"qn_{i}", use_container_width=True,
                                     type="primary" if is_cur else "secondary"):
                            st.session_state.current_question = i; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    src = q.get("source_slide")
    if src:
        st.markdown(f"""<div class="ac-inset" style="margin-top:12px">
  <div class="ac-overline" style="margin-bottom:8px">Source</div>
  <div style="font-family:var(--fh);font-size:28px;color:var(--fg)">Folio <span style="color:var(--ac)">{src:02d}</span></div>
</div>""", unsafe_allow_html=True)
