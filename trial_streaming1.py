
import chainlit as cl
from src.llm1 import llm_model


@cl.on_chat_start
async def factory():
    llm_obj = llm_model()
    print("Creating LLM Object...")
    storage_context, nodes = llm_obj.read_data_and_build_context()
    print("Built Storage Context and Nodes...")
    custom_retriever = llm_obj.build_index_and_retriever(storage_context, nodes)
    print("Built Index and Retriever...")
    query_engine = llm_obj.build_queryengine(custom_retriever)
    print("Built Query Engine...")
    llm_obj.set_callback_handler(cl.LlamaIndexCallbackHandler())
    cl.user_session.set("query_engine", query_engine)


@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")
    response = await cl.make_async(query_engine.query)(message.content)
    #print(f"response: {response}")
    msg = cl.Message(content="")
    await msg.send()

    for res in response.response_gen:
        print(f"response: {res}")
        await msg.stream_token(res)
    if response.response_txt:
        msg.content = response.response_txt

    await msg.send()
