import json
from typing import Optional

from decouple import config
from groq import Groq
from pydantic import BaseModel

# Set up the Groq client
client = Groq(api_key=config("GROQ_API_KEY"))

class Chat(BaseModel):
    text: str
    comments: Optional[str] = None

def groq_chat(query):
    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that speaks fluent Thai. "
                           f"You will only reply with the text and nothing else in JSON. "
                           f"The JSON object must use the schema: {json.dumps(Chat.model_json_schema(), indent=2)}"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        # เปลี่ยน Model ID ตาม console.groq.com/docs/models
        model="llama3-8b-8192",  
        temperature=0.2,
        max_tokens=1024,
        stream=False,
        response_format={"type": "json_object"},
    )
    # Return the translated text
    return Chat.model_validate_json(chat_completion.choices[0].message.content)