from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class CompanyRequest(BaseModel):
    company: str

@app.get("/")
def read_root():
    return {"status": "Enterprise Intel App is running"}

@app.post("/research")
def research_company(request: CompanyRequest):
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Give me a structured company brief on {request.company}. Include: what they do, recent news, business model, and key facts."}
        ]
    )
    return {"brief": message.content[0].text}