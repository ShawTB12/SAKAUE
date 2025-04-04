import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any

def display_common_header(title: str):
    """
    各占いの結果表示時の共通ヘッダーを表示
    """
    st.markdown(f"## {title}")
    st.markdown("---")

def create_radar_chart(categories: List[str], values: List[float], title: str):
    """
    レーダーチャートを作成する
    """
    # カテゴリ数を取得
    N = len(categories)
    
    # 角度を計算
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    
    # 閉じた図形にするため、最初の要素を最後にも追加
    values.append(values[0])
    angles.append(angles[0])
    categories.append(categories[0])
    
    # プロットの作成
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles), categories)
    ax.set_title(title, size=20, y=1.05)
    ax.grid(True)
    
    return fig

def display_personality_traits(traits: Dict[str, Any]):
    """
    性格特性を表示する
    """
    st.subheader("性格特性")
    
    for trait, value in traits.items():
        if isinstance(value, (int, float)):
            st.markdown(f"**{trait}**: {value}/10")
            st.progress(value / 10)
        else:
            st.markdown(f"**{trait}**: {value}")

def display_shichuu_result(result: Dict[str, Any]):
    """
    四柱推命の結果を表示
    """
    display_common_header("四柱推命")
    
    st.markdown(f"**日柱天干**: {result.get('ten_kan', '不明')}")
    st.markdown(f"**日柱十二運**: {result.get('juu_ni_shi', '不明')}")
    st.markdown(f"**月干の蔵干宿命星**: {result.get('tsuhen_sei', '不明')}")

def display_onmyo_result(result: Dict[str, Any]):
    """
    陰陽五行の結果を表示
    """
    display_common_header("陰陽五行")
    
    inyo = result.get('inyo', '不明')
    gogyo = result.get('gogyo', '不明')
    st.markdown(f"**{gogyo}の{inyo}**")

def display_shukuyo_result(result: Dict[str, Any]):
    """
    宿曜の結果を表示
    """
    display_common_header("宿曜")
    
    st.markdown(f"**{result.get('shukuyo', '不明')}**")

def display_western_result(result: Dict[str, Any]):
    """
    西洋占星術の結果を表示
    """
    display_common_header("西洋占星術")
    
    st.markdown(f"**太陽**: {result.get('sun_sign', '不明')}")
    st.markdown(f"**月**: {result.get('moon_sign', '不明')}")

def display_animal_result(result: Dict[str, Any]):
    """
    動物占いの結果を表示
    """
    display_common_header("動物占い")
    
    animal = result.get('animal', '不明')
    type_name = result.get('type', '不明')
    st.markdown(f"**{type_name}となる{animal}**")

def display_kyusei_result(result: Dict[str, Any]):
    """
    九星気学の結果を表示
    """
    display_common_header("九星気学")
    
    st.markdown(f"**本命星**: {result.get('honmei_sei', '不明')}")
    st.markdown(f"**月命星**: {result.get('getsu_mei_sei', '不明')}") 