import streamlit as st
import time
from utils import inject_css, init_state, _DEFAULTS

st.set_page_config(page_title="Scholarium — Results", page_icon="📜", layout="wide")
init_state()
inject_css()

if not st.session_state.questions:
    st.switch_page("pages/upload.py")

qs = st.session_state.questions
ans = st.session_state.user_answers
cfg = st.session_state.quiz_config
right = sum(1 for q in qs if ans.get(q["id"]) == q["correct_answer"])
total = len(qs)
pct = int(right / total * 100) if total else 0
grade = "Distinction" if pct >= 80 else ("Credit" if pct >= 60 else "Refer for Re-examination")

st.markdown("""
<div class="ac-overline" style="margin-bottom:8px">Volume IV</div>
<div class="ac-h1">Examination<br><em>Results</em></div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([2, 1], gap="large")
with c1:
    st.markdown(f"""<div class="ac-card ac-anim" style="margin-bottom:28px">
  <div style="display:flex;align-items:flex-start;justify-content:space-between">
    <div>
      <div class="ac-overline" style="margin-bottom:12px">Final Score</div>
      <div class="ac-score">{right}<span class="ac-score-denom"> / {total}</span></div>
      <div style="font-family:var(--fh);font-size:28px;color:var(--mfg);margin-top:8px">{pct}%</div>
    </div>
    <div style="text-align:right">
      <div class="ac-seal" title="{grade}" style="width:56px;height:56px;font-size:22px">
        {'★' if pct >= 80 else ('◆' if pct >= 60 else '◇')}
      </div>
      <div style="font-family:var(--fd);font-size:9px;color:var(--mfg);letter-spacing:.2em;margin-top:8px;text-transform:uppercase">{grade}</div>
    </div>
  </div>
  <div class="ac-div" style="margin:20px 0"></div>
  <div style="font-family:var(--fb);font-size:15px;color:var(--mfg);font-style:italic">
    {'A commendable performance — the scholar has demonstrated mastery of the subject.' if pct >= 80
     else ('A creditable result — further study of the weaker areas is advised.' if pct >= 60
           else 'The examination reveals gaps in understanding. A thorough review of the material is recommended.')}
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="ac-overline" style="margin-bottom:14px">Question Review</div>', unsafe_allow_html=True)
    for i, q in enumerate(qs):
        ua = ans.get(q["id"])
        ok = ua == q["correct_answer"]
        with st.expander(f"{'✓' if ok else '✗'}  Q{i+1}: {q['question_text'][:72]}{'…' if len(q['question_text']) > 72 else ''}"):
            if ok:
                st.markdown(f'<div class="ac-xrow xr-ok"><div class="ac-xlbl">Correct — {ua}: {q["options"].get(ua,"")}</div>{q["explanation_correct"]}</div>', unsafe_allow_html=True)
            else:
                we = q["explanation_wrong"].get(ua, "") if ua else ""
                st.markdown(f'<div class="ac-xrow xr-err" style="margin-bottom:6px"><div class="ac-xlbl">Your Answer — {ua}: {q["options"].get(ua,"—")}</div>{we}</div><div class="ac-xrow xr-ok"><div class="ac-xlbl">Correct Answer — {q["correct_answer"]}: {q["options"][q["correct_answer"]]}</div>{q["explanation_correct"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)
    with bc1:
        if st.button("Retake Examination", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.confirmed_answers = {}
            st.session_state.timer_start = time.time() if cfg.get("timed") else None
            st.switch_page("pages/quiz.py")
    with bc2:
        if st.button("Upload New Manuscript →", use_container_width=True):
            for k, v in _DEFAULTS.items():
                st.session_state[k] = v
            st.switch_page("pages/upload.py")

with c2:
    st.markdown(f"""<div class="ac-inset">
  <div class="ac-overline" style="margin-bottom:16px">Session Ledger</div>
  <div style="display:flex;flex-direction:column;gap:12px">
    <div style="display:flex;justify-content:space-between;align-items:baseline">
      <span style="font-family:var(--fb);font-size:14px;color:var(--mfg)">Difficulty</span>
      <span style="font-family:var(--fd);font-size:10px;color:var(--fg);letter-spacing:.1em">{cfg.get('difficulty','—')}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:baseline">
      <span style="font-family:var(--fb);font-size:14px;color:var(--mfg)">Mode</span>
      <span style="font-family:var(--fd);font-size:10px;color:var(--fg);letter-spacing:.1em">{'Timed' if cfg.get('timed') else 'Untimed'}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:baseline">
      <span style="font-family:var(--fb);font-size:14px;color:var(--mfg)">Questions</span>
      <span style="font-family:var(--fh);font-size:18px;color:var(--fg)">{total}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:baseline">
      <span style="font-family:var(--fb);font-size:14px;color:var(--mfg)">Correct</span>
      <span style="font-family:var(--fh);font-size:18px;color:var(--ac)">{right}</span>
    </div>
    <div class="ac-div"></div>
    <div style="display:flex;justify-content:space-between;align-items:baseline">
      <span style="font-family:var(--fb);font-size:14px;color:var(--mfg)">Verdict</span>
      <span style="font-family:var(--fd);font-size:9px;color:var(--ac);letter-spacing:.15em;text-transform:uppercase">{grade}</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
