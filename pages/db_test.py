import os
import streamlit as st
import asyncio
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)
@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)    

client = init_connection()
db = client.mito
collection = db['chat_sessions'] 
def main():
    # Streamlitアプリの設定
    st.title("チャット履歴の読み込み")

    # ユーザーIDの入力
    user_id = st.text_input("ユーザーIDを入力してください:")

    if user_id:
        # user_idでチャットセッションを検索
        chat_sessions = collection.find({"user_id": user_id})
        chat_sessions = list(chat_sessions)
        print("aaaljgeo",chat_sessions)

        # セッションが存在するか確認
        if len(chat_sessions) == 0:
            st.write("このユーザーIDに該当するチャット履歴は見つかりませんでした。")
        else:
            # 各チャットセッションを表示
            for session in chat_sessions:
                st.write(f"セッション開始: {session['timestamp']}")
                print(session)
                for log in session['chat_history']:
                    print("log",log)
                    st.write(f"**ユーザー**: {log['user']}")
                    st.write(f"**アシスタント**: {log['assistant']}")
                    st.write(f"**タイムスタンプ**: {str(log['timestamp'])}")
                st.write("---")  # 区切り線

main()
