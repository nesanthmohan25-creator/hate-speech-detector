import streamlit as st
import re

# -----------------------
# DEBUG (CONFIRM FILE RUNNING)
# -----------------------


# -----------------------
# PROFANITY PATTERNS
# -----------------------
patterns = [
    r"\bfuck\w*\b",
    r"\bshit\w*\b",
    r"\bbitch\w*\b",
    r"\basshole\w*\b",
    r"\bdumb\w*\b",
    r"\bstupid\w*\b",
    r"\bidiot\w*\b",
    r"\bcrap\w*\b",
    r"\bgarbage\w*\b",
    r"\buseless\w*\b",
    r"\bhell\w*\b",
    r"\bwtf\b",
]

# -----------------------
# FUNCTIONS
# -----------------------
def highlight_toxic(text):
    highlighted = text
    for pattern in patterns:
        highlighted = re.sub(
            pattern,
            lambda m: f"<span style='background-color:#ff4d4d; color:white; padding:4px; border-radius:5px'>{m.group(0)}</span>",
            highlighted,
            flags=re.IGNORECASE
        )
    return highlighted


def extract_toxic_words(text):
    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        found.update(matches)
    return list(found)

# -----------------------
# UI
# -----------------------
st.set_page_config(page_title="Hate Comment Detector", page_icon="💬")

st.title("💬 Hate Comment Detector")
st.write("Detects hate comments and highlights harmful words")

text = st.text_area("Enter a comment:")

# -----------------------
# ANALYZE
# -----------------------
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("⚠️ Please enter some text")

    else:
        # 🔥 DETECT WORDS FIRST
        toxic_found = extract_toxic_words(text)

        # 🔥 FINAL DECISION (RULE-BASED)
        is_toxic = len(toxic_found) > 0

        # -----------------------
        # RESULT
        # -----------------------
        st.subheader("Result:")

        if is_toxic:
            st.error("⚠️ Hate Comment")
        else:
            st.success("✅ Non-Hate Comment")

        # -----------------------
        # HIGHLIGHT TEXT
        # -----------------------
        st.subheader("Highlighted Text:")
        st.markdown(highlight_toxic(text), unsafe_allow_html=True)

        # -----------------------
        # WORD LIST
        # -----------------------
        st.subheader("Hate Speech Detected:")

        if toxic_found:
            st.error("🔴 " + ", ".join(toxic_found))
        else:
            st.success("No harmful words found")
