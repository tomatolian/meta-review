import sys
import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="Streamlit App", page_icon=":shark:")

question_input = st.Page(page="pages/question_input.py", title="質問入力画面")
chat = st.Page(page="pages/chatpage.py", title="chat", icon=":material/home:")
confirm = st.Page(page="pages/confirm.py", title="確認", icon=":material/check:")


pg = st.navigation([question_input,chat,confirm])


pg.run()