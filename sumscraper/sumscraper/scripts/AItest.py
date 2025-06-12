from ollama import chat
from ollama import ChatResponse


response: ChatResponse = chat(model="Mistral:7B", messages= [
        {
        'role': 'user',
        'content': 'What are the first 5 prime numbers?',
        },
    ])
print(response['message']['content'])