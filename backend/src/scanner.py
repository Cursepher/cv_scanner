import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY)

pii_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "You are a privacy assistant. Remove or redact all PII (personally identifiable information) "
        "from the following cover letter and replace it with [REDACTED]. This includes names, phone numbers, email addresses, locations, "
        "social security numbers, and any other private identifiers.\n\n"
        "Cover Letter:\n{text}\n\n"
        "Redacted Cover Letter:"
    )
)
pii_chain = pii_prompt | llm

skills_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Extract a clean list of professional skills mentioned in the following redacted cover letter. "
        "Only include hard skills like programming languages, tools, certifications, and job-relevant abilities.\n\n"
        "Redacted Cover Letter:\n{text}\n\n"
        "Skills (as a comma-separated list):"
    )
)
skills_chain = skills_prompt | llm

def process_cover_letter(raw_text):
    redacted_result = pii_chain.invoke({"text": raw_text})
    redacted_text = redacted_result.content

    skills_result = skills_chain.invoke({"text": redacted_text})
    skills = skills_result.content

    return redacted_text, skills
