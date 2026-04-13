# src/llm_config.py
import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

# llama-3.3-70b-versatile handles agent tool-use prompts reliably on Groq's free tier.
# max_tokens prevents the LLM from returning None due to context overflow.
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
    max_tokens=2048,
    max_retries=3
)
