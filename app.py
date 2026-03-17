import streamlit as st
import os
import re
from typing import Optional, Dict
from openai import OpenAI
from dotenv import load_dotenv
from textblob import TextBlob

load_dotenv()
try:
  client = OpenAI(api_key = os.getenv("GROQ_API_KEY"), base_url = "https://api.groq.com/openai/v1")
except Exception as e:
  st.error(f"Can't Initialise the AI Client: {e}") 

MODEL = "llama-3.3-70b-versatile"
EXIT_KEYWORDS = {"exit", "quit", 'bye', 'goodbye', "terminate", "cancel"}

FIELDS = [
  {"key" : "Full Name", "prompt": "What is your Full Name?"},
  {"key" : "Email Address", "prompt" : "Please provide your Email Id"},
  {"key" : "Phone Number", "prompt" : "Please provide your Phone Number"},
  {"key" : "Year of Experience", "prompt" : "How many Years of Experience do you have ? "},
  {"key" : "Desired Position", "prompt" : "Which Position is desired by you ?"},
  {"key" : "Current Location", "prompt" : "What is your current location ? "},
  {"key" : "Tech Stack", "prompt":"Please list your Tech Stack. (e.g. Python, MySQL)"}
]



def sentiment(text):
  polarity = TextBlob(text).sentiment.polarity
  if polarity < -0.2:
    return "Negative"
  elif polarity > 0.3:
    return "Positive"
  return "Neutral"


def validate_input(field_key, user_input):
  user_input = user_input.strip()
  if field_key == "Email Address":
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+$"
    if not re.match(pattern, user_input):
      return False, "Please enter a valid email."

  elif field_key == "Year of Experience":
    if not any(ch.isdigit() for ch in user_input):
      return False, "Please include number for your years of experience."

  return True, ""


def generate_tech_questions(tech_stack, experience):
  system_prompt = """ You are a Senior Technical Engineering Manager. Your goal is to screen a candidate strictly based on provided information about them.
  Rules to generate questions:
  1. Generate 4 technical questions.
  2. Calibrate the difficulty to match the year of experience.
  3. Focus exclusively on the technologies provided in the Tech Stack.
  4. Do not provide answers or any hint.
  5. Be professional, encouraging, and concise.
  6. CRITICAL: Separate each question with '###'.
  7. Output ONLY the questions. No introductory or concluding text.
  Example: Question 1?###Question 2###Question 3###Question 4
  """

  user_prompt = f"Candidate Experience: {experience}\n Candidate Tech stack: {tech_stack}\n Please Generate the screening questions."

  try:
    response = client.chat.completions.create(model=MODEL, messages = [
      {"role": "system","content":system_prompt},
      {"role":"user", "content":user_prompt}
    ], temperature=0.2)

    return response.choices[0].message.content
  except Exception as e :
    return f"Error: {e}"


def init_state():
  if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content" : f"Hello, I am TalentScout -AI HIRING ASSISTANT. \n\n{FIELDS[0]['prompt']}"}]
  if "user_data" not in st.session_state:
    st.session_state.user_data = {}
  if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0
  if "is_completed" not in st.session_state:
    st.session_state.is_completed = False
  if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
  if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0    


init_state()

st.set_page_config(page_title="Talent Scout", layout="wide")

with st.sidebar:
  st.title("Application Tracker")
  progress = int((st.session_state.step_idx / len(FIELDS)) * 100)
  st.progress(progress, text=f"Completion: {progress}%")

  st.markdown("### Profile Information")
  for i, field_dict in enumerate(FIELDS):
    key = field_dict["key"]
    if key in st.session_state.user_data:
      st.success(f"{key} {st.session_state.user_data[key]}")
    else:
      st.caption(f"{key}")

  if any(k.startswith("Answer to Question") for k in st.session_state.user_data):
    st.divider()
    for k, v in st.session_state.user_data.items():
      if k.startswith("Answer to Question"):
        st.info(f"{k}\n{v}")


  st.divider()

  if st.session_state.messages:
    user_msg = [m["content"] for m in st.session_state.messages if m["role"] == "user"] 
    if user_msg:
      s = sentiment(user_msg[-1])
      st.info(f"Candidate :{s}")

  with st.expander("Data Privacy Policy"):
    st.caption("All data is processed locally in temporary session memory. The data is handled in compilance with data privacy standards(GDPR)")


st.title("TalentScout AI Recruiter")
for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])



if not st.session_state.is_completed:
    if user_input := st.chat_input("Enter your response..."):
      
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        if user_input.lower().strip() in EXIT_KEYWORDS:
            exit_msg = "Thank you for your time. You may close this window." 
            st.session_state.messages.append({"role":"assistant", "content":exit_msg})
            st.session_state.is_completed = True
            st.rerun()

        current_idx = st.session_state.step_idx
        if current_idx < len(FIELDS):
            current_field_key = FIELDS[current_idx]["key"]
            is_valid, error_msg = validate_input(current_field_key, user_input)

            if not is_valid:
                st.session_state.messages.append({"role":"assistant", "content":error_msg})
            else:
                st.session_state.user_data[current_field_key] = user_input.strip()
                st.session_state.step_idx += 1

                if st.session_state.step_idx < len(FIELDS):
                    next_prompt = FIELDS[st.session_state.step_idx]['prompt']
                    st.session_state.messages.append({"role": "assistant", "content": next_prompt})
                else:
                    with st.spinner("Generating Interview Questions..."):
                        raw_q = generate_tech_questions(st.session_state.user_data["Tech Stack"], st.session_state.user_data["Year of Experience"])
                        st.session_state.tech_questions = [q.strip() for q in raw_q.split('###') if q.strip()]

                    if st.session_state.tech_questions:
                        first_q = st.session_state.tech_questions[0] 
                        st.session_state.messages.append({"role":"assistant", "content":f"Perfect. Let's start the technical screening:\n\n{first_q}"})
                    else:
                        st.session_state.messages.append({"role":"assistant", "content":"I encountered an error generating questions. Please try again."})
                        st.session_state.is_completed = True
            st.rerun()
        else:
            q_num = st.session_state.q_idx + 1
            st.session_state.user_data[f"Answer to Question {q_num}"] = user_input
            st.session_state.q_idx += 1

            if st.session_state.q_idx < len(st.session_state.tech_questions):
                next_q = st.session_state.tech_questions[st.session_state.q_idx]
                st.session_state.messages.append({"role":"assistant", "content":next_q})
            else:
                final_msg = "Thank you for your responses! The technical screening is now complete. We will reach out within 48 hours."
                st.session_state.messages.append({"role":"assistant", "content":final_msg})
                st.session_state.is_completed = True
            st.rerun()

else:
    st.info("The screening session is completed.")