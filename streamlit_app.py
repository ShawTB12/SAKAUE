import os
import sys

# personality_diagnosis_appディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), "personality_diagnosis_app"))

# app.pyのmain関数を実行
from personality_diagnosis_app.app import main

if __name__ == "__main__":
    main() 