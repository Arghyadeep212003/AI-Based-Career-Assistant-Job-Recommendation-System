🤖 AI Career Assistant & Job Recommendation System

An AI-powered career assistance platform that analyzes resumes and recommends relevant job opportunities using Natural Language Processing (NLP) and semantic similarity search.

The system also includes a resume scoring module and a career FAQ chatbot to help users improve their resumes and get answers to career-related questions.

⚠️ Project Status: 🚧 Currently in progress – deployment has not been completed yet.

📌 Project Overview

This project aims to build an intelligent system that can:

1️⃣ Analyze a user's resume content
2️⃣ Recommend relevant job opportunities
3️⃣ Evaluate the strength of a resume
4️⃣ Provide career-related answers through a chatbot

The system uses modern AI techniques such as Sentence Transformers and FAISS vector search for efficient job matching.

✨ Key Features
1️⃣ Job Recommendation System

📄 Recommends jobs based on resume content

🧠 Uses Sentence Transformers (BERT embeddings) for text representation

⚡ Uses FAISS vector similarity search for fast job matching

📊 Filters the most relevant job roles from a dataset

2️⃣ Resume Scoring System

📝 Evaluates resumes based on multiple factors:

✔️ Skills

✔️ Education

✔️ Experience

✔️ Certifications

📈 Generates a resume strength score (0–100)

💡 Helps users understand how strong their resume is

3️⃣ Career FAQ Chatbot

💬 Answers career-related questions

🔍 Uses semantic search to find the best answer

📚 Matches user questions with stored FAQ data

4️⃣ Streamlit Web Interface

🌐 Interactive Streamlit-based UI

👨‍💻 Easy-to-use interface for:

Resume analysis

Job recommendations

Chatbot interaction

🛠️ Tech Stack
💻 Programming & Framework

🐍 Python

🌐 Streamlit

🤖 AI / NLP

Sentence Transformers (BERT)

FAISS Similarity Search

📊 Data Processing

Pandas

NumPy

Scikit-learn

📂 Project Structure
📦 AI-Career-Assistant
│
├── chatbot.py            # Career FAQ chatbot
├── model.py              # Job recommendation system
├── resume_scorer.py      # Resume scoring module
├── test.py               # Streamlit application
├── requirements.txt      # Project dependencies
│
├── career_faq.csv        # FAQ dataset
├── JobsFE.csv            # Job dataset
│
└── CleanedJobs.ipynb     # Data preprocessing notebook
⚙️ Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-career-assistant.git
cd ai-career-assistant
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
streamlit run test.py
🚀 Future Improvements

Planned improvements for upcoming versions:

🔹 Deploy the application online
🔹 Improve resume parsing accuracy
🔹 Add more job datasets
🔹 Integrate advanced NLP models
🔹 Improve Streamlit UI/UX
🔹 Add user authentication system
🔹 Enable real-time job scraping

📊 Project Status

🚧 Currently Under Development

This project is still progressing and not yet deployed.
Additional features and improvements will be added in future updates.
