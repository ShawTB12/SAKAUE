import streamlit as st
import os
import sys

# アプリケーションディレクトリをPATHに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'personality_diagnosis_app'))

# メインアプリを実行
import app

# メイン関数を呼び出す
if __name__ == "__main__":
    app.main() 