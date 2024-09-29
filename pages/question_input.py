import streamlit as st
from datetime import datetime

def main():
    user_id="test_user1"
    # 大カテゴリ、中カテゴリ、小カテゴリの階層構造
    category_dict = {
        'フロントエンド': {
            'JavaScript': ['構文エラー', '未定義変数', 'プロミスの未解決'],
            'React': ['フックの誤用', 'ステートの同期ミス', 'コンポーネントのレンダリングエラー'],
            'Vue.js': ['ライフサイクルフックの問題', 'ディレクティブエラー', 'テンプレートバインディングの誤り'],
            'HTML': ['タグの閉じ忘れ', '要素のネスト不正'],
            'CSS': ['セレクタの競合', 'レスポンシブデザインの崩れ']
        },
        'バックエンド': {
            'Python': ['ImportError', 'TypeError', 'データベース接続エラー'],
            'Java': ['NullPointerException', 'ClassNotFoundException', 'メモリリーク'],
            'Node.js': ['非同期処理エラー', 'モジュール未定義エラー', '環境変数の設定ミス'],
            'Ruby': ['NoMethodError', 'Gemfileの依存関係エラー'],
            'Go': ['構文エラー', 'パッケージインポートエラー', 'goroutineのデッドロック']
        },
        'データベース': {
            'SQL': ['クエリエラー', 'デッドロック', '結合の誤り'],
            'MongoDB': ['接続エラー', 'クエリパフォーマンス問題'],
            'PostgreSQL': ['権限エラー', 'インデックスの設定ミス']
        },
        'DevOps': {
            'Docker': ['コンテナ起動エラー', 'イメージビルド失敗', 'ネットワーク設定エラー'],
            'Kubernetes': ['ポッド作成失敗', 'ノード接続エラー'],
            'CI/CD': ['パイプラインエラー', 'デプロイ失敗'],
            'Terraform': ['プロバイダの設定ミス', 'リソース作成エラー']
        }
    }

    # 大カテゴリを選択
    main_category = st.selectbox('大カテゴリを選択してください:', list(category_dict.keys()))

    # 中カテゴリを動的に設定
    sub_category = st.selectbox('中カテゴリを選択してください:', list(category_dict[main_category].keys()))

    # 小カテゴリを動的に設定
    small_category = st.selectbox('小カテゴリを選択してください:', category_dict[main_category][sub_category])

    user_question = st.text_input("質問内容")
    
    if st.button('送信'):
        if not user_question:
            st.error("エラー内容は必須です。入力してください。")
        else:
            st.write(f'選択した大カテゴリ: {main_category}')
            st.write(f'選択した中カテゴリ: {sub_category}')
            st.write(f'選択した小カテゴリ: {small_category}')
            st.write(f'エラー内容: {user_question}')
            chat_log = {
            "user_id": user_id,
            "chat_history":[{"user":user_question, "assistant":None,"timestamp":datetime.now(), "main":main_category, "sub":sub_category,"small":small_category}],
            "timestamp": datetime.now()
        }
            st.session_state["session_info"]=chat_log
            st.switch_page("pages/chatpage.py")
main()
