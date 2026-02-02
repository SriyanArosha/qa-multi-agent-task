import streamlit as st
import os
import time
from utils.pdf_extract import extract_pdf_text
from agents.agent_a_extract import extract_requirements
from agents.agent_b_generate import generate_playwright_code
from agents.agent_c_review import review_code

st.set_page_config(page_title="PDF → Playwright Agent", layout="wide")

st.title("Playwright Test Generator")

uploaded_file = st.file_uploader("Upload requirements PDF", type=["pdf"])

if uploaded_file and st.button("Process PDF → Generate & Refine Tests"):

    with st.status("Processing...", expanded=True) as status:
        # Save file
        os.makedirs("temp", exist_ok=True)
        pdf_path = "temp/uploaded.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        status.write("Agent A — Extracting testable requirements …")
        pdf_text = extract_pdf_text(pdf_path)
        requirements = extract_requirements(pdf_text)
        st.session_state["requirements"] = requirements
        status.update(label="Requirements extracted", state="complete")
        st.markdown("### Extracted Requirements")
        st.markdown(requirements)

        code = ""
        feedback = ""

        for i in range(1, 6):
            status.write(f"Iteration {i} — Generating code …")
            code = generate_playwright_code(requirements, feedback)
            st.session_state[f"code_{i}"] = code
            st.code(code, language="python", line_numbers=True)

            status.write(f"Iteration {i} — Reviewing for issues …")
            feedback = review_code(code, requirements)
            st.session_state[f"feedback_{i}"] = feedback
            st.markdown(f"**Feedback iteration {i}**")
            st.markdown(feedback)

            if "no issues" in feedback.lower() or "perfect" in feedback.lower():
                status.update(label=f"Review passed at iteration {i}", state="complete")
                break

            time.sleep(0.8)

        status.update(label="Final result ready", state="complete")

    st.success("Processing finished!")
    st.download_button("Download final Playwright code", code, "tests_generated.py")

    # cleanup
    if os.path.exists(pdf_path):
        os.remove(pdf_path)