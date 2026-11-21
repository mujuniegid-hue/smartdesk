import time
import streamlit as st
from checks import find_setup_problems

st.set_page_config(page_title="SmartDesk", page_icon="💬")

problems = find_setup_problems()
if problems:
    st.error("SmartDesk is not set up correctly. Please fix:")
    for problem in problems:
        st.write("- " + problem)
    st.stop()

from config import get_setting
from assistant import load_documents
from triage import handle_message

MAX_LENGTH = 1000
MAX_REPLIES = 15

if "count" not in st.session_state:
    st.session_state.count = 0

business_name = get_setting("BUSINESS_NAME", "this business")
# TEMPORARY DEBUG: remove after fixing
_key = get_setting("GEMINI_API_KEY") or ""
st.sidebar.write("Key length:", len(_key))
st.sidebar.write("Starts with:", _key[:4], "| Ends with:", _key[-2:])
st.sidebar.write("Has space or quote:", any(c in _key for c in ' "\'\n'))

st.title("SmartDesk")
st.caption(f"AI customer support assistant for {business_name}")


@st.cache_data
def get_documents():
    return load_documents()


documents = get_documents()

message = st.text_area(
    "Customer message",
    placeholder="Example: Do you deliver?",
    max_chars=MAX_LENGTH,
)

if st.button("Get reply"):
    if not message.strip():
        st.warning("Please type a customer message first.")
    elif st.session_state.count >= MAX_REPLIES:
        st.warning("Demo limit reached for this session. Please contact the owner.")
    else:
        try:
            with st.spinner("Thinking..."):
                start = time.time()
                result = handle_message(message, documents)
                seconds = time.time() - start
        except Exception as error:
            print(f"SmartDesk error: {error}")
            st.error("Something went wrong. Please try again in a moment.")
            st.code(f"{type(error).__name__}: {error}")
            st.stop()

        st.session_state.count += 1

        if result.needs_owner:
            st.error("⚠️ Needs the owner's attention")
        else:
            st.success("✅ Handled automatically")

        col1, col2 = st.columns(2)
        col1.metric("Category", result.category)
        col2.metric("Urgency", result.urgency)

        st.write("**Why:**", result.reason)
        st.subheader("Reply to send")
        st.info(result.reply)
        st.caption(f"Answered in {seconds:.1f} seconds")