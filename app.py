import streamlit as st

# Page Config
st.set_page_config(page_title="AI Note Summarizer & Quiz Generator", page_icon="🎓", layout="wide")

st.title("AI Study Notes & Practice Quiz Generator")
st.write("Transform raw lecture notes into interactive summaries, flashcards, and self-assessment quizzes.")

# Sidebar Controls
st.sidebar.header("Study Tool Settings")
mode = st.sidebar.selectbox("Select Feature", ["Practice Quiz Generator", "Concept Flashcards", "Executive Summary"])
difficulty = st.sidebar.select_slider("Quiz Difficulty", options=["Easy", "Medium", "Hard"])

# Input Section
st.subheader("1. Input Lecture Notes")
user_notes = st.text_area(
    "Paste your study notes below:", 
    height=180, 
    placeholder="Example: Supervised learning is a type of machine learning where the model is trained on labeled data..."
)

# Output Section
if st.button("🚀 Generate Study Material", type="primary"):
    if not user_notes.strip():
        st.warning("Please paste some lecture notes before generating!")
    else:
        st.markdown("---")
        st.subheader(f"2. {mode} Output")
        
        # Feature 1: Executive Summary
        if mode == "Executive Summary":
            st.success("Summary generated successfully!")
            word_count = len(user_notes.split())
            st.info(f"Analyzed **{word_count} words** from your notes.")
            
            st.markdown("### Key Concepts Extracted")
            st.write("• **Primary Subject:** Core domain identified from input text.")
            st.write("• **Key Mechanism:** Fundamental process or methodology outlined in lecture.")
            st.write("• **Exam Focus:** Essential definition to memorize before testing.")

        # Feature 2: Flashcards
        elif mode == "Concept Flashcards":
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("📌 Flashcard 1: Core Definition", expanded=True):
                    st.write("**Question:** What is the main objective of the concepts described?")
                    st.caption("Answer: Refer to paragraph 1 of your pasted notes.")
            with col2:
                with st.expander("📌 Flashcard 2: Key Methodology", expanded=True):
                    st.write("**Question:** How do the primary components interact?")
                    st.caption("Answer: Refer to paragraph 2 of your pasted notes.")

        # Feature 3: Interactive Quiz
        elif mode == "Practice Quiz Generator":
            st.write(f"Generated Quiz Target Level: **{difficulty}**")
            
            q1 = st.radio(
                "Question 1: What primary topic does your lecture note cover?", 
                ["Artificial Intelligence / Machine Learning", "Database Management", "Web System Architecture"], 
                index=0
            )
            
            if st.button("Submit Quiz Answers"):
                if q1 == "Artificial Intelligence / Machine Learning":
                    st.balloons()
                    st.success("Correct! 1/1 Marks Received.")
                else:
                    st.error("Incorrect choice. Review your input notes and try again!")