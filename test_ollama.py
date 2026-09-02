from ollama import chat


response = chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "What is FastAPI? Answer in 2 lines."
        }
    ]
)

print(response["message"]["content"])