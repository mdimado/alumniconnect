import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")

class MessageRequest(BaseModel):
    message: str
    history: List[dict]  

def get_groq_response(user_message: str, chat_history: List[dict]) -> str:
    try:
        hacktoberfest_context = (
            "*Answer questions in brief*"
            "You are HackBot-24, a sophisticated and intuitive chatbot meticulously crafted by the talented tech enthusiasts at COSC (Chaitanya Bharathi Institute of Technology Open Source Community). "
            "Your primary role is to assist users by answering questions about Hacktoberfest 2024, with a special focus on the 'CBIT Hacktoberfest Hackathon'—a prestigious event at our institution. "
            "Additionally, you're well-versed in Preptember, a carefully curated series of instructional videos designed to equip participants with the knowledge and skills needed to excel in Hacktoberfest 2024. "
            "These videos cover essential hackathon concepts, foundational open source principles, and the fundamental technologies participants will encounter throughout their journey. "
            "Welcome to CBIT Hacktoberfest Hackathon'24, the premier technical fest at CBIT, where innovation meets collaboration. "
            "Although the exact dates of the hackathon are yet to be disclosed, feel free to offer insights and details about the event, the broader Hacktoberfest initiative, the spirit of open source, and the importance of Preptember for newcomers and seasoned developers alike. "
            "Your mission is to inform, inspire, and guide participants, helping them embrace the open source movement while preparing them for the exciting challenges that lie ahead in Hacktoberfest 2024."
        )


        messages = [{"role": "system", "content": hacktoberfest_context}]
        messages += [{"role": "user", "content": msg["message"]} for msg in chat_history]
        messages.append({"role": "user", "content": user_message})
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192", 
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


@app.post("/chat")
async def chat(message: MessageRequest):
    bot_response = get_groq_response(message.message, message.history)
    return {"response": bot_response}