import os
import sys
import streamlit as st

# personality_diagnosis_appディレクトリをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 相対インポートを使用
try:
    from personality_diagnosis_app.app import main
    st.success("モジュールのインポートに成功しました")
except ImportError as e:
    st.error(f"インポートエラー: {e}")
    st.info("インストールされているパッケージを確認中...")
    import subprocess
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    st.code(result.stdout)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.write("ディレクトリ構造:")
        st.code(os.listdir(current_dir)) 