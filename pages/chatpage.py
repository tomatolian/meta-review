from datetime import datetime
import os
import openai
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import streamlit as st
from pymongo import MongoClient
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import Tool

MONGO_URI = st.secrets["section1"]["MONGO_URI"]
api_key = st.secrets["section1"]["OPENAI_API_KEY"]

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)    

client = init_connection()
db = client.mito
collection = db.chat_sessions    

def main():
    user_id="test_user"
    chat_sessions = collection.find({"user_id": user_id})
    session_num=len(list(collection.find({"user_id": user_id})))
    if session_num != 0:
        sec_chat={}
        for session in chat_sessions:
            session_id = session["_id"]
            sec_chat[session_id]=session['chat_history']
            user_question = sec_chat[session_id][0]["user"]
            title = user_question[:15] if len(user_question)>15 else user_question
            st.sidebar.button(title, key=str(session_id))
    
    if st.button("解決"):
        chat_log = {
            "user_id": "test_user",
            "chat_history": st.session_state["session_info"]['chat_history'],
            "timestamp": datetime.now(),
            "solve":True
        }
        st.session_state["session_info"]["chat_log"]=chat_log
        st.switch_page("pages/confirm.py")



    if st.button("未解決"):
        chat_log = {
            "user_id": "test_user",
            "chat_history": st.session_state["session_info"]['chat_history'],
            "timestamp": datetime.now(),
            "solve":False
        }
        st.session_state["session_info"]["chat_log"]=chat_log
        st.switch_page("pages/confirm.py")


    # OpenAIのLLMを初期化
    llm = ChatOpenAI(temperature=0,openai_api_key=api_key,streaming=True)

    # プロンプトテンプレートを作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは親切なアシスタントです。日本語で応答してください。"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="chat_history"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    # ダミーのツールを作成
    tools = [
        Tool(
            name="dummy",
            func=lambda x: "dummy",
            description="ダミーツール"
        )
    ]

    # エージェントの初期化
    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # AgentExecutorの作成
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    # 過去のチャット履歴をページに表示
    for session in st.session_state["session_info"]['chat_history']:
        user_message = session["user"]
        assistant_message = session["assistant"]
        st.chat_message("user").write(user_message)
        if assistant_message:
            st.chat_message("assistant").write(assistant_message)

    # チャット履歴を正しい形式に変換する関数
    def convert_history_to_messages(history):
        messages = []
        for msg in history:
            if msg["user"]:
                messages.append({
                    "role": "user",
                    "content": msg["user"]
                })
            if msg["assistant"]:
                messages.append({
                    "role": "assistant",
                    "content": msg["assistant"]
                })
        return messages

    # アシスタントの応答を取得
    if st.session_state["session_info"]['chat_history'][0]["assistant"] == None:
        prompt = st.session_state["session_info"]['chat_history'][0]["user"]

        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            chat_history = convert_history_to_messages(st.session_state["session_info"]['chat_history'])
            response = agent_executor.invoke(
                {
                    "input": prompt + "応答は日本語で答えてください。",
                    "chat_history": chat_history,
                    "agent_scratchpad": []
                },
                config={"callbacks": [st_callback]}
            )
            st.write(response["output"])

            # チャット履歴にアシスタントの応答を追加
            st.session_state["session_info"]['chat_history'][-1] = {
                "user": prompt,
                "assistant": response["output"],
                "timestamp": datetime.now()
            }

main()
