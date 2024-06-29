import os
from phi.assistant import Assistant
from phi.llm.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.exa import ExaTools
import streamlit as st


groq_api_key = st.secrets["GROQ_API_KEY"]
exa_api_key = st.secrets["EXA_API_KEY"]


  
def ai(prompt, school):
    description = f"You are a College Enquiry chatbot,you provide the user with specific information about {school} requested by user."
    assistant = Assistant(
    llm=Groq(model="llama3-70b-8192",api_key=groq_api_key, max_tokens=6000),
    description=description,
    instructions=[
        "You search for the college's website",
        "All responses must come from the web search not your knowledge base"
        "Using the information from the website only, respond to the user.",
        "Ensure you always give a detailed response.",
        "Do not use this phrase 'According to the information yielded from the tool call'"
    ],
    tools=[DuckDuckGo(), ExaTools(api_key=exa_api_key)],
    debug_mode=True,
    )
    
    response = assistant.run(prompt, stream=False)
    return response
