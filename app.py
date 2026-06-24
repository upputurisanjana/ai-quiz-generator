import streamlit as st

upload  = st.Page("pages/upload.py",    title="Upload",    icon="📜")
config  = st.Page("pages/configure.py", title="Configure", icon="⚙️")
loading = st.Page("pages/loading.py",   title="Loading",   icon="⏳")
quiz    = st.Page("pages/quiz.py",      title="Quiz",      icon="📝")
results = st.Page("pages/results.py",   title="Results",   icon="🏆")

pg = st.navigation([upload, config, loading, quiz, results], position="hidden")
pg.run()
