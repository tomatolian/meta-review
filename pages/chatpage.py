import os
from datetime import datetime
import openai
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from dotenv import load_dotenv
import asyncio
from pymongo import MongoClient
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
openai.api_key = os.getenv("OPENAI_API_KEY")

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)    

client = init_connection()
db = client.mito
collection = db.chat_sessions
        
def main():
    if st.button("チャット履歴を保存"):
        chat_log = {
            "user_id": "test_user",
            "chat_history": st.session_state['chat_history'],
            "timestamp": datetime.now()
        }
        collection.insert_one(chat_log)
        st.success("チャット履歴が保存されました！")
        st.session_state['chat_history']=[]


    # OpenAIのLLMを初期化
    llm = ChatOpenAI(temperature=0,streaming=True)

    # ツールなしでエージェントを初期化
    tools = [] 
    # ReActエージェントを、ツールなしでも動作可能なエージェントタイプに変更
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # エージェントタイプを変更
        verbose=True
    )

    # チャット履歴を管理するためのリストを用意
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # 過去のチャット履歴をページに表示
    for user_message, assistant_message,_ in st.session_state['chat_history']:
        st.chat_message("user").write(user_message)
        if assistant_message:
            st.chat_message("assistant").write(assistant_message)

    # 新しいメッセージを入力した場合
    if prompt := st.chat_input():
        # ユーザーのメッセージを表示
        st.chat_message("user").write(prompt)

        # チャット履歴を更新
        st.session_state['chat_history'].append({"user":prompt, "assistant":None,"timestamp":datetime.now()})  # Noneはアシスタントの返答のプレースホルダー

        # アシスタントの応答を取得
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())  # Streamlitのコールバックハンドラ
            response = agent.run(
                {
                    "input": prompt+"応答は日本語で答えてください。", 
                    "chat_history": st.session_state['chat_history']  # チャット履歴を渡す
                },
                callbacks=[st_callback]
            )

            # アシスタントの応答を表示
            st.write(response)

            # チャット履歴にアシスタントの応答を追加
            st.session_state['chat_history'][-1] = {"user":prompt, "assistant":response,"timestamp":datetime.now()}

main()
