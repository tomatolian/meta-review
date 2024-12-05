import os
from datetime import datetime

from dotenv import load_dotenv
import openai
from pymongo import MongoClient
import streamlit as st

load_dotenv()

MONGO_URI = st.secrets["section1"]["MONGO_URI"]
openai.api_key = st.secrets["section1"]["OPENAI_API_KEY"]

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)    

client = init_connection()
db = client.mito
collection = db.chat_sessions    

def create_tag_and_youyaku(chat_history):
    
    
    # OpenAIのAPIを使用してタグと要約を生成
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system", 
                "content": "あなたは質問内容からタグと要約を生成するアシスタントです。以下のJSONフォーマットで返答してください: {\"tags\": [\"タグ1\", \"タグ2\"], \"question_summary\": \"ユーザの質問を要約\", \"answer_summary\": \"アシスタントの回答を要約\"}"
            },
            {
                "role": "user",
                "content": f"以下の履歴から、関連するタグと質問要約,回答要約を生成してください。要約は、内容のみを端的に答えてください。履歴: { chat_history['chat_history'] }"
            }
        ]
    )

    # JSONレスポンスをパース
    import json
    result = json.loads(response.choices[0].message.content)
    tags = result["tags"]
    question_summary=result["question_summary"]
    answer_summary = result["answer_summary"]
    chat_history["tags"] =tags
    chat_history["question_summary"] = question_summary
    chat_history["answer_summary"] = answer_summary
    return chat_history



def confirm_page():
    st.title("チャット内容の確認")

    # st.session_stateからチャット履歴を取得
    chat_history = st.session_state.get("session_info", [])

    if chat_history:
        st.write("以下のチャット内容を確認してください：")
        for session in chat_history["chat_history"]:
            user_message = session["user"]
            assistant_message = session["assistant"]
            st.chat_message("user").write(user_message)
            if assistant_message:
                st.chat_message("assistant").write(assistant_message)

    else:
        st.write("チャット履歴がありません。")

    if st.button("確認完了"):
        st.success("チャット内容が確認されました。")
        chat_history = create_tag_and_youyaku(chat_history)
        st.success("タグ、要約が生成されました")
        collection.insert_one(chat_history)
        st.success("チャット内容が保存されました")

    if st.button("戻る"):
        st.switch_page("pages/chat")

confirm_page()

