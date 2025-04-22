# 性格診断システム

生年月日から導き出すあなただけの個性を分析するStreamlitアプリケーションです。

## 特徴

- 四柱推命、宿曜、陰陽五行、九星気学、西洋占星術、動物占いなど複数の占術システムを統合
- 美しいUI/UXデザイン
- インタラクティブな分析結果表示

## インストール方法

```bash
# リポジトリをクローン
git clone https://github.com/あなたのユーザー名/SAKAUE.git
cd SAKAUE

# 依存パッケージのインストール
pip install -r personality_diagnosis_app/requirements.txt
```

## 使い方

```bash
streamlit run personality_diagnosis_app/app.py
```

## Streamlit Cloudでのデプロイ方法

1. GitHubアカウントを使って[Streamlit Cloud](https://streamlit.io/cloud)にログイン
2. 「New app」をクリック
3. リポジトリ、ブランチ、メインファイルパスを設定:
   - リポジトリ: あなたのユーザー名/SAKAUE
   - ブランチ: main
   - パス: streamlit_app.py
4. 「Deploy」をクリック

## 必要環境

- Python 3.9以上
- 各種依存パッケージ（requirements.txtを参照） 