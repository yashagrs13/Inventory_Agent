# src/llm_config.py
import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

# Using Groq's LLaMA 3.3 70B — free tier, fast, no quota issues
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.environ.get("GROQ_API_KEY"),
    max_retries=3
)
