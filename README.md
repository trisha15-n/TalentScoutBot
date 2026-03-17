# TalentScoutBot
A professional, context-aware chatbot designed to streamline the initial recruitment process. This tool automates candidate information gathering and conducts a technical screening using Large Language Models.

PROJECT OVERVIEW :-
The Hiring Assistant chatbot is designed to assist in the initial screening of candidates by gathering essential information and posing relevant technical questions based on the candidate's declared tech stack.

Phase 1 : Information Gathering - Collects the information of candidate like Full Name, Email Address, Phone no., Desired position, Year of Experience, Current location, Tech Stack.
Phase 2 : Technical Screening - Dynamically generates technical questions based on their technical stack and the year of experience.
Phase 3 : Real time Progress Tracking - A dynamic sidebar updates as the candidate provides information.

INSTALLATION INSTRUCTIONS - 
This project uses uv for high-performance Python package management.
1. Clone the repository -
   git clone https://github.com/trisha15-n/TalentScoutBot.git
   cd TalentScoutBot
2. Environment Setup -
   GROQ_API_KEY=your_actual_api_key_here
3. Install Dependencies & Run -
   uv run streamlit run app.py

TECHNICAL STACK :-
i) Language - Python
ii) Frontend - Streamlit
iii) LLM API - Groq    

PROMPT DESIGN - 
1. LLM is initialised as a "Senior Technical Engineering Manager".
2. Rules to generate questions:
  1. Generate 4 technical questions.
  2. Calibrate the difficulty to match the year of experience.
  3. Focus exclusively on the technologies provided in the Tech Stack.
  4. Do not provide answers or any hint.
  5. Be professional, encouraging, and concise.
  6. CRITICAL: Separate each question with '###'.
  7. Output ONLY the questions. No introductory or concluding text.
  Example: Question 1?###Question 2###Question 3###Question 4

USAGE GUIDE -
1. Initialize - Start the process with providing your name.
2. Details - Follow the prompts to provide your professional details.
3. Interview - AI generates the questions one by one and you can answer them one by one.
4. Completion - After the technical questions are answered the conversation is concluded.
5. Review - The summary of the entire conversation will be provided in sidebar.
   


