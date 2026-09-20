import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kakadevops.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "IT-Support AI backend is running"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=(
            "You are IT-Support AI, a professional IT helpdesk assistant. "
            "Help users troubleshoot Windows, laptops, PCs, Wi-Fi, networking, "
            "printers, accounts, software and common IT problems. "
            "Give clear step-by-step instructions. "
            "Ask a short follow-up question when important information is missing. "
            "Never ask the user for passwords, API keys, or other secrets."
        ),
        input=request.message,
    )

    return {"reply": response.output_text}
