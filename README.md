AI Career Assistant & Job Recommendation System

Overview

This project is an AI-powered Career Assistant that helps users analyze their resumes and receive relevant job recommendations. The system uses Natural Language Processing (NLP) and semantic similarity search to match resumes with suitable job roles.
The project also includes a resume scoring system and a career FAQ chatbot to assist users with career-related questions.

⚠️ Note: This project is currently under development and still progressing. Deployment has not been completed yet.


Features
1. Job Recommendation System
   
   Recommends jobs based on the content of a user's resume.
   
   Uses Sentence Transformers embeddings to represent job descriptions and resumes.
   
   Uses FAISS similarity search to find the most relevant jobs.

3. Resume Scoring
   
   Evaluates resumes based on:
   
   Skills
   
   Education
   
   Experience
   
   Certifications

   Generates a score to indicate resume strength.

4. Career FAQ Chatbot
   
   Answers career-related questions.
   
   Uses semantic search to match user questions with stored FAQs.

6. Streamlit Interface

   Simple user interface built with Streamlit.
   
   Allows users to interact with the recommendation system and chatbot.


Tech Stack

   Python
   
   Streamlit
   
   Sentence Transformers (BERT)
   
   FAISS
   
   Pandas
   
   NumPy

   Scikit-learn



Project Structure

├── chatbot.py              
├── model.py                
├── resume_scorer.py      
├── test.py                
├── requirements.txt       
├── career_faq.csv         
├── JobsFE.csv            
└── CleanedJobs.ipynb 


Installation

   Clone the repository:
   
   git clone https://github.com/your-username/ai-career-assistant.git
   cd ai-career-assistant
   
   Install dependencies:
   
   pip install -r requirements.txt
   
   Run Streamlit app:
   
   streamlit run test.py


Future Improvements:

   Deploy the application online
   
   Improve resume parsing
   
   Add more job datasets
   
   Implement advanced NLP models
   
   Improve UI/UX of the Streamlit interface
   
   Add user authentication


Status

🚧 Project Status: In Progress

The system is currently under development and testing. Deployment and additional features will be added in future updates.
