from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(prompt):

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
    )

    return completion.choices[0].message.content
def planner_agent(service):

    prompt = f"""
User wants help with (You are Yukti AI,the Indian Government representative): {service}

Explain:
1. Government form required
2. Documents needed
3. Application steps
4. Add relevant links to official government websites for more information.
"""

    return ask_ai(prompt)
def document_agent(service):

    prompt = f"""
For the government service: {service}

List required documents.

Then say:
- which documents are mandatory
- which are optional
"""

    return ask_ai(prompt)
def form_agent(service):

    prompt = f"""
For the service: {service}

Generate a list of form fields required to fill the application.
Example:
Name
Date of Birth
Address
ID Proof
Phone number
"""

    return ask_ai(prompt)
def validation_agent(service):

    prompt = f"""
User wants to apply for {service}.

Give a checklist before submitting the application.
"""

    return ask_ai(prompt)