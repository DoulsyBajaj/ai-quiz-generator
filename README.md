# AI Study Notes and Interactive Quiz Generator

A Streamlit application powered by Google Gemini API that converts lecture notes or uploaded PDFs into structured study guides or interactive multiple-choice quizzes.

Live App: https://ai-quiz-generator-zb4ysykdxbezfjyxganqt7.streamlit.app/

---

## Features

* Multi-Source Input: Upload PDF or TXT files, or paste lecture notes directly into the application.
* Detailed Study Notes: Generates formatted summaries, key terms, concept breakdowns, and core takeaways.
* Interactive Quizzes: Generates multiple-choice practice questions with custom question counts, difficulty levels, automated grading, and explanations.

## Tech Stack

* Framework: Streamlit
* AI Model: Google Gemini API
* PDF Parser: PyPDF
* Language: Python 3.8+

## Local Setup

1. Clone the repository:
   git clone https://github.com/DoulsyBajaj/ai-quiz-generator.git
   cd ai-quiz-generator

2. Install dependencies:
   pip install -r requirements.txt

3. Set up local secrets:
   Create a folder named .streamlit and add a secrets.toml file inside:
   GEMINI_API_KEY = "your_gemini_api_key_here"

4. Launch the application:
   streamlit run app.py

## Usage

1. Select a mode from the sidebar: "Detailed Study Notes" or "Practice Quiz Generator".
2. Upload a PDF/TXT file or paste raw text into the input box.
3. If generating a quiz, select your desired number of questions and difficulty level (Easy, Medium, Hard).
4. Click "Generate Material" to view your study notes or start your quiz.

## Troubleshooting and Notes

* Scanned PDFs: Image-based or scanned PDFs cannot be read by PyPDF. Paste the text directly into the text box if text extraction returns zero words.
* API Key Secrets: When deploying to Streamlit Cloud, store your key in the app Settings under Secrets using the variable name GEMINI_API_KEY.
* Large Documents: For large files, consider uploading smaller sections at a time for optimal generation quality.

## Security and Privacy

Do not upload sensitive or private personal data. Information processed by the app is sent to Google Gemini API for generation. Always keep your API keys private and never commit your secrets.toml file to GitHub.
