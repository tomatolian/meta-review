from datetime import datetime
import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from pymongo import MongoClient
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

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
    print("session_info",st.session_state["session_info"])
    chat_log=st.session_state["session_info"]
    if st.button("解決"):
        chat_log["chat_history"]=st.session_state["session_info"]['chat_history']
        chat_log["solved"]=True
        st.session_state["session_info"]=chat_log
        st.switch_page("pages/confirm.py")



    if st.button("未解決"):
        chat_log["chat_history"]=st.session_state["session_info"]['chat_history']
        chat_log["solved"]=False
        st.session_state["session_info"]=chat_log
        st.switch_page("pages/confirm.py")


    # OpenAIのLLMを初期化
    llm = ChatOpenAI(temperature=0,openai_api_key=api_key,streaming=True)

    # ツールなしでエージェントを初期化
    # tools = [] 
    # ReActエージェントを、ツールなしでも動作可能なエージェントタイプに変更
    # agent = initialize_agent(
    #     tools=tools,
    #     llm=llm,
    #     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # エージェントタイプを変更
    #     verbose=True
    # )

    # 過去のチャット履歴をページに表示
    for session in st.session_state["session_info"]['chat_history']:
        user_message = session["user"]
        assistant_message = session["assistant"]
        st.chat_message("user").write(user_message)
        if assistant_message:
            st.chat_message("assistant").write(assistant_message)
    print(st.session_state["session_info"]['chat_history'])
    if st.session_state["session_info"]['chat_history'][0]["assistant"]==None:
        prompt = st.session_state["session_info"]['chat_history'][0]["user"]

        # アシスタントの応答を取得
        with st.chat_message("assistant"):
            # st_callback = StreamlitCallbackHandler(st.container())  # Streamlitのコールバックハンドラ
            messages = [SystemMessage(f"""
                                      応答は日本語で答えてください。
                                      chat_history:{st.session_state["session_info"]['chat_history'] }
                                      """),
                        HumanMessage(f"{prompt}")
                        ]
            response = llm.predict_messages(messages).content
            # アシスタントの応答を表示
            st.write(response)

            # チャット履歴にアシスタントの応答を追加
            st.session_state["session_info"]['chat_history'][-1] = {"user":prompt, "assistant":response,"timestamp":datetime.now()}
            
    # 新しいメッセージを入力した場合
    if (prompt := st.chat_input() ):
        # ユーザーのメッセージを表示
        st.chat_message("user").write(prompt)

        # チャット履歴を更新
        st.session_state["session_info"]['chat_history'].append({"user":prompt, "assistant":None,"timestamp":datetime.now()})  # Noneはアシスタントの返答のプレースホルダー

        # アシスタントの応答を取得
        with st.chat_message("assistant"):
            # st_callback = StreamlitCallbackHandler(st.container())  # Streamlitのコールバックハンドラ
            messages = [SystemMessage(f"""
                                      応答は日本語で答えてください。
                                      chat_history:{st.session_state["session_info"]['chat_history'] }
                                      """),
                        HumanMessage(f"{prompt}")
                        ]
            response = llm.predict_messages(messages).content
            # アシスタントの応答を表示
            st.write(response)

            # チャット履歴にアシスタントの応答を追加
            st.session_state["session_info"]['chat_history'][-1] = {"user":prompt, "assistant":response,"timestamp":datetime.now()}

main()
