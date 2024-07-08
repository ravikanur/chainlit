import chainlit as cl
from src.llm import ask_bot

@cl.on_message
async def main(message: cl.Message):
    
    # Your custom logic goes here...
    print(f"message from bot is {message}")

    response = ask_bot(message.content)

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {response}",
    ).send()