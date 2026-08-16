import json
import google.generativeai as genai
import pypdf
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="AI Note Summarizer & Quiz Generator",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 AI Study Notes & Interactive Quiz Generator")
st.write(
    "Upload your lecture PDFs/text notes or paste text to generate detailed"
    " study guides and interactive practice quizzes!"
)

# 2. Configure Gemini API from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
  st.error(
      "⚠️ Gemini API Key not found in Streamlit Secrets! Please add"
      " GEMINI_API_KEY in your Streamlit Cloud settings."
  )

# 3. Sidebar Controls
st.sidebar.header("⚙️ Study Tool Settings")
mode = st.sidebar.selectbox(
    "Select Feature", ["Practice Quiz Generator", "Detailed Study Notes"]
)
num_questions = st.sidebar.slider(
    "Number of Quiz Questions", min_value=3, max_value=30, value=5
)
difficulty = st.sidebar.select_slider(
    "Quiz Difficulty", options=["Easy", "Medium", "Hard"]
)

# 4. Input Section (File Upload OR Text Area)
st.subheader("1. Input Study Material")
col1, col2 = st.columns(2)

with col1:
  uploaded_file = st.file_uploader(
      "📁 Upload a PDF or TXT file", type=["pdf", "txt"]
  )

with col2:
  user_notes = st.text_area(
      "✍️ Or paste your lecture notes directly:",
      height=150,
      placeholder="Paste your notes or textbook content here...",
  )


# Helper function to extract text from file or text box
def get_source_text():
  if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
      pdf_reader = pypdf.PdfReader(uploaded_file)
      extracted = ""
      for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
          extracted += text + "\n"
      return extracted
    elif uploaded_file.name.endswith(".txt"):
      return uploaded_file.read().decode("utf-8")
  elif user_notes.strip():
    return user_notes.strip()
  return ""


source_text = get_source_text()

if source_text:
  word_count = len(source_text.split())
  st.info(f"📖 Loaded Study Material: **{word_count} words** detected.")

# 5. Initialize Session States
if "quiz_data" not in st.session_state:
  st.session_state.quiz_data = None
if "notes_data" not in st.session_state:
  st.session_state.notes_data = None
if "submitted" not in st.session_state:
  st.session_state.submitted = False

# 6. AI Generation Trigger
if st.button("🚀 Generate Material", type="primary"):
  if not source_text:
    st.warning("Please upload a file or paste some lecture notes first!")
  else:
    st.session_state.submitted = False
    available_models = [
    m.name
    model = genai.GenerativeModel("gemini-3.5-flash")

    with st.spinner("AI is reading your content and generating material..."):
      try:
        if mode == "Detailed Study Notes":
          prompt = f"""
                    You are an expert academic tutor. Analyze the following study material and generate highly detailed, comprehensive study notes formatted cleanly in Markdown.
                    Include the following sections:
                    - **Executive Summary** (Overview of main topics)
                    - **Key Terms & Definitions**
                    - **Detailed Concept Breakdown** (In-depth explanation of core mechanisms/ideas)
                    - **Key Takeaways & Exam Tips**

                    Study Material:
                    {source_text}
                    """
          response = model.generate_content(prompt)
          st.session_state.notes_data = response.text
          st.session_state.quiz_data = None

        elif mode == "Practice Quiz Generator":
          prompt = f"""
                    Generate exactly {num_questions} multiple choice questions at {difficulty} difficulty based on the study material below.

                    You MUST return ONLY a raw JSON array of objects without markdown formatting or code blocks.
                    Each object in the array must have these exact keys:
                    - "question": (string)
                    - "options": (array of 4 distinct string choices)
                    - "answer": (string matching exactly one of the options)
                    - "explanation": (string explaining why this answer is correct)

                    Study Material:
                    {source_text}
                    """
          response = model.generate_content(prompt)

          # Clean potential markdown formatting from JSON output
          raw_text = response.text.strip()
          if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
          if raw_text.startswith("```"):
            raw_text = raw_text[3:]
          if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

          quiz_json = json.loads(raw_text.strip())
          st.session_state.quiz_data = quiz_json
          st.session_state.notes_data = None

      except Exception as e:
        st.error(
            f"An error occurred while generating content: {e}. Please try"
            " again."
        )

# 7. Render Output Section
st.markdown("---")

# Render Detailed Notes
if mode == "Detailed Study Notes" and st.session_state.notes_data:
  st.subheader("📝 Generated Detailed Notes")
  st.markdown(st.session_state.notes_data)

# Render Practice Quiz Form
elif mode == "Practice Quiz Generator" and st.session_state.quiz_data:
  st.subheader(
      f"🧠 Interactive Quiz ({len(st.session_state.quiz_data)} Questions -"
      f" {difficulty} Difficulty)"
  )

  with st.form("quiz_form"):
    user_answers = {}
    for idx, item in enumerate(st.session_state.quiz_data):
      st.markdown(f"#### Question {idx+1}: {item['question']}")
      user_answers[idx] = st.radio(
          "Choose an option:",
          options=item["options"],
          key=f"q_{idx}",
          index=None,  # No option pre-selected
      )
      st.write("")

    submit_quiz = st.form_submit_button("Submit Quiz Answers")

  if submit_quiz:
    st.session_state.submitted = True

  # 8. Quiz Results & Grading
  if st.session_state.submitted:
    st.markdown("### 📊 Quiz Results & Feedback")
    score = 0
    total = len(st.session_state.quiz_data)

    for idx, item in enumerate(st.session_state.quiz_data):
      selected = user_answers.get(idx)
      correct = item["answer"]
      explanation = item.get("explanation", "")

      if selected == correct:
        score += 1
        st.success(f"**Q{idx+1}: Correct!** You selected: *{selected}*")
      elif selected is None:
        st.warning(
            f"**Q{idx+1}: Unanswered.** The correct answer was: **{correct}**"
        )
      else:
        st.error(
            f"**Q{idx+1}: Incorrect.** You selected *'{selected}'*, but the"
            f" correct answer is **'{correct}'**."
        )

      if explanation:
        st.caption(f"💡 *Explanation:* {explanation}")
      st.divider()

    percentage = round((score / total) * 100)
    if percentage >= 70:
      st.balloons()
      st.success(f"🎉 **Great job! Your Score: {score}/{total} ({percentage}%)**")
    else:
      st.info(
          f"📚 **Keep practicing! Your Score: {score}/{total} ({percentage}%)**"
      )