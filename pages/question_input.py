import streamlit as st
from datetime import datetime

def main():
    user_id="test_user"
    # 大カテゴリ、中カテゴリ、小カテゴリの階層構造
    categories = [f"プログラミング基礎第{i}回".format(i) for i in range(1,9)]

    # 大カテゴリを選択
    category = st.selectbox('大カテゴリを選択してください:', list(categories))

    user_question = st.text_input("質問内容")
    
    if st.button('送信'):
        if not user_question:
            st.error("エラー内容は必須です。入力してください。")
        else:
            st.write(f'選択した大カテゴリ: {category}')
            st.write(f'エラー内容: {user_question}')
            chat_log = {
            "user_id": user_id,
            "chat_history":[{"user":user_question, "assistant":None,"timestamp":datetime.now()}],
            "category":category,
            "timestamp": datetime.now()
        }
            st.session_state["session_info"]=chat_log
            st.switch_page("pages/chatpage.py")
main()
