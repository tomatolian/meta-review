import sys
import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="Streamlit App", page_icon=":shark:")


chat = st.Page(page="pages/chatpage.py", title="chat", icon=":material/home:")
test = st.Page(page="pages/db_test.py", title="test")

if 'mongo_client' not in st.session_state:
    st.session_state['mongo_client'] = MongoClient(MONGO_URI)  # MongoDBのURLに置き換えてください
    st.session_state['db'] = st.session_state['mongo_client']['mito']  # データベース名
    st.session_state['collection'] = st.session_state['db']['chat_sessions']

pg = st.navigation([chat,test])



pg.run()