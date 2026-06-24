import streamlit as st
from utils import inject_css, init_state, parse_pptx

st.set_page_config(page_title="Scholarium — Upload", page_icon="📜", layout="wide")
init_state()
inject_css()

ppt = st.session_state.ppt_data

st.markdown("""
<div class="ac-overline" style="margin-bottom:8px">Volume I</div>
<div class="ac-h1">Upload Your<br><em>Lecture Deck</em></div>
<div class="ac-sub">Present a <code style="font-family:var(--fb);background:var(--muted);padding:1px 6px;border-radius:2px">.pptx</code> — the scholar's engine shall compose your examination.</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([2, 1], gap="large")
with c1:
    if ppt is None:
        st.markdown("""<div class="ac-drop">
  <div class="ac-arch" aria-hidden="true">📜</div>
  <div style="font-family:var(--fh);font-size:22px;font-weight:400;color:var(--fg);margin-bottom:6px">Choose a file or drag it here</div>
  <div style="font-family:var(--fb);font-size:14px;color:var(--mfg)">.pptx manuscripts only</div>
</div>""", unsafe_allow_html=True)
    up = st.file_uploader("Upload", type=["pptx"], label_visibility="collapsed")
    if up and ppt is None:
        with st.spinner(""):
            st.session_state.ppt_data = parse_pptx(up)
        st.rerun()
    if ppt:
        st.markdown(f"""<div class="ac-card ac-anim" style="margin-top:16px">
  <div class="ac-overline" style="margin-bottom:12px">Manuscript received</div>
  <div style="font-family:var(--fh);font-size:26px;font-weight:400;color:var(--fg);margin-bottom:18px">{ppt['filename']}</div>
  <div class="ac-div"></div>
  <div style="display:flex;gap:28px;margin-top:18px">
    <div><div class="ac-overline" style="margin-bottom:4px">Folios</div><div style="font-family:var(--fh);font-size:32px;color:var(--ac)">{ppt['slides']}</div></div>
    <div><div class="ac-overline" style="margin-bottom:4px">Words</div><div style="font-family:var(--fh);font-size:32px;color:var(--ac)">{ppt['words']:,}</div></div>
    <div><div class="ac-overline" style="margin-bottom:4px">Status</div><div style="font-family:var(--fh);font-size:32px;color:#7AAF95">&#x2713;</div></div>
  </div>
</div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Proceed to Configuration →", use_container_width=True):
            st.switch_page("pages/configure.py")

with c2:
    st.markdown("""<div class="ac-inset">
  <div class="ac-overline" style="margin-bottom:16px">The Method</div>
  <div style="display:flex;flex-direction:column;gap:18px">
    <div style="display:flex;gap:14px;align-items:flex-start">
      <div style="font-family:var(--fd);font-size:11px;color:var(--ac);padding-top:2px;flex-shrink:0">I</div>
      <div style="font-family:var(--fb);font-size:15px;color:var(--mfg);line-height:1.55">Upload your <em>.pptx</em> — every text shape is extracted and catalogued</div>
    </div>
    <div style="display:flex;gap:14px;align-items:flex-start">
      <div style="font-family:var(--fd);font-size:11px;color:var(--ac);padding-top:2px;flex-shrink:0">II</div>
      <div style="font-family:var(--fb);font-size:15px;color:var(--mfg);line-height:1.55">Set the difficulty, question count, and examination mode</div>
    </div>
    <div style="display:flex;gap:14px;align-items:flex-start">
      <div style="font-family:var(--fd);font-size:11px;color:var(--ac);padding-top:2px;flex-shrink:0">III</div>
      <div style="font-family:var(--fb);font-size:15px;color:var(--mfg);line-height:1.55">The AI composes MCQs with detailed per-option elucidations</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
