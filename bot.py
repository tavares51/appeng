from openai import OpenAI
import os
from dotenv import load_dotenv
from settings import ASSISTANT_ID, OPENAI_API_KEY

def process_message(message:str):
    load_dotenv()
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")
    assistant_id = ASSISTANT_ID
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for message in messages:
            assert message.content[0].type == "text"
            return {"message": message.content[0].text.value, "role": message.role}
    else:
        return {"message": message.content[0].text.value, "role": "erro"}
    
        
def run():
    print("Seja bem-vindo ao EngIA")
    while True:
        message = input("Digite a sua dúvida ou digite (sair) para encerrar o processo:\n ")
        if message.lower() in ('sair', 'exit'):
            break
        
        retorno = process_message(message)
        print(100*"-")
        print("user:", message)
        print(100*"-")
        print("bot:", retorno["message"])
        print(100*"-")

if __name__ == "__main__":
    run()