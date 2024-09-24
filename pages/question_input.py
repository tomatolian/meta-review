import streamlit as st

def main():
    # Streamlitアプリの設定
    st.title("チャット履歴の読み込み")

    category_dict = {
        'フロントエンド': ['HTML', 'CSS', 'JavaScript', 'React', 'Vue.js'],
        'バックエンド': ['Python', 'Ruby', 'Java', 'Node.js', 'Go'],
        'データサイエンス': ['Python', 'R', 'SQL', 'Pandas', 'TensorFlow'],
        'DevOps': ['Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Ansible']
    }

    # 大カテゴリを選択
    main_category = st.selectbox('大カテゴリを選択してください:', list(category_dict.keys()))

    # 大カテゴリに対応する中カテゴリを動的に設定
    sub_category = st.selectbox('中カテゴリを選択してください:', category_dict[main_category])


    user_question = st.text_input("質問を入力してください")

    if user_question:
        st.write(f'選択した大カテゴリ: {main_category}')
        st.write(f'選択した中カテゴリ: {sub_category}')
        st.write(user_question)

main()
