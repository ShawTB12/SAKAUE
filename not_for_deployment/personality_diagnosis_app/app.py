import streamlit as st
import datetime
import time
import random
from personality_diagnosis_app.utils import date_utils, display_utils
from personality_diagnosis_app.fortune_systems import shichuu_suimei, onmyo_gogyo, shukuyo, western_astrology, animal_fortune, kyusei_kigaku
import streamlit.components.v1 as components

# カスタムCSS
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap');
    
    :root {
        --primary: #6C63FF;
        --secondary: #6EC5FF;
        --accent: #FF6584;
        --background: #111132;
        --text: #E8F3F6;
        --card-bg: rgba(18, 18, 60, 0.6);
        --card-border: rgba(108, 99, 255, 0.3);
    }
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
        color: var(--text);
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--background), #232351);
    }
    
    /* カスタムフォントヘッダー */
    h1, h2, h3, h4 {
        font-family: 'Noto Sans JP', sans-serif;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 15px rgba(108, 99, 255, 0.4);
    }
    
    h1 {
        font-size: 3rem !important;
        letter-spacing: -0.5px;
        background: linear-gradient(to right, #FFFFFF, #6EC5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0 !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        opacity: 0.9;
    }
    
    h3 {
        font-size: 1.5rem !important;
        color: white;
        margin-top: 2rem !important;
    }
    
    /* 診断ボタン */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 50px;
        font-weight: 500;
        font-size: 1.1rem;
        box-shadow: 0 6px 15px rgba(108, 99, 255, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(108, 99, 255, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* 日付入力 */
    .date-picker-container {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    
    /* 結果カード */
    .result-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(to right, var(--primary), var(--secondary));
        border-radius: 18px 18px 0 0;
    }
    
    .result-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    .result-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .result-content {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* プログレスバー */
    .stProgress > div > div {
        background-color: var(--primary);
        border-radius: 100px;
        height: 8px;
    }
    
    .stProgress {
        height: 8px;
    }
    
    /* パーティクルコンテナ */
    .particles-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
    }
    
    /* 結果表示用 - ゴーストアニメーションを削除 */
    .result-element {
        opacity: 1; /* 常に表示 */
        margin-bottom: 20px;
    }
    
    /* 結果ヘッダー装飾 */
    .result-header {
        text-align: center;
        margin: 40px 0;
        position: relative;
    }
    
    .result-header::before, .result-header::after {
        content: "";
        position: absolute;
        top: 50%;
        width: 100px;
        height: 2px;
        background: linear-gradient(to right, rgba(108, 99, 255, 0), rgba(108, 99, 255, 0.8));
    }
    
    .result-header::before {
        left: 20%;
    }
    
    .result-header::after {
        right: 20%;
        background: linear-gradient(to left, rgba(108, 99, 255, 0), rgba(108, 99, 255, 0.8));
    }
    
    /* DateInputのスタイル上書き */
    .stDateInput > div {
        background-color: rgba(30, 30, 70, 0.5) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(108, 99, 255, 0.3) !important;
        color: white !important;
    }
    
    .stDateInput input {
        color: white !important;
    }
    
    /* データポイント */
    .data-point {
        margin-bottom: 12px;
        display: flex;
        align-items: center;
    }
    
    .data-label {
        font-weight: 500;
        margin-right: 10px;
        color: rgba(255, 255, 255, 0.7);
    }
    
    .data-value {
        font-weight: 700;
        font-size: 1.1rem;
        color: white;
    }
    
    /* アニメーションコンテナ */
    .animation-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(17, 17, 50, 0.95);
        z-index: 9999;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    /* アニメーションコンテンツ */
    .animation-content {
        text-align: center;
    }
    
    /* 分析テキスト */
    .analysis-text {
        font-size: 1.5rem;
        font-weight: 500;
        color: white;
        margin-top: 20px;
    }
    
    .shimmer {
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.8) 50%, rgba(255,255,255,0) 100%);
        background-size: 200% auto;
        animation: shimmer 2s infinite linear;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    @keyframes shimmer {
        0% {background-position: -100% 0;}
        100% {background-position: 100% 0;}
    }
    
    /* グロー効果 */
    .glow {
        text-shadow: 0 0 5px rgba(108, 99, 255, 0.8), 0 0 10px rgba(108, 99, 255, 0.5);
    }
    
    /* セクションセパレーター */
    .section-divider {
        display: flex;
        align-items: center;
        margin: 2rem 0;
    }
    
    .section-divider::before, .section-divider::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(to right, rgba(108, 99, 255, 0), rgba(108, 99, 255, 0.5), rgba(108, 99, 255, 0));
    }
    
    .section-divider span {
        padding: 0 1rem;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }
    
    /* フッター */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 50px;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
    }

    /* 結果表示用フラグ表示 */
    .debug-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.8rem;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# パーティクルアニメーション用JS
def add_particles():
    particles_js = """
    <div class="particles-container" id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            particlesJS("particles-js", {
                "particles": {
                    "number": {
                        "value": 80,
                        "density": {
                            "enable": true,
                            "value_area": 800
                        }
                    },
                    "color": {
                        "value": ["#6C63FF", "#6EC5FF", "#A594F9"]
                    },
                    "shape": {
                        "type": "circle",
                        "stroke": {
                            "width": 0,
                            "color": "#000000"
                        }
                    },
                    "opacity": {
                        "value": 0.3,
                        "random": true,
                        "anim": {
                            "enable": true,
                            "speed": 1,
                            "opacity_min": 0.1,
                            "sync": false
                        }
                    },
                    "size": {
                        "value": 3,
                        "random": true,
                        "anim": {
                            "enable": true,
                            "speed": 2,
                            "size_min": 0.1,
                            "sync": false
                        }
                    },
                    "line_linked": {
                        "enable": true,
                        "distance": 150,
                        "color": "#6C63FF",
                        "opacity": 0.2,
                        "width": 1
                    },
                    "move": {
                        "enable": true,
                        "speed": 1,
                        "direction": "none",
                        "random": true,
                        "straight": false,
                        "out_mode": "out",
                        "bounce": false,
                        "attract": {
                            "enable": false,
                            "rotateX": 600,
                            "rotateY": 1200
                        }
                    }
                },
                "interactivity": {
                    "detect_on": "canvas",
                    "events": {
                        "onhover": {
                            "enable": true,
                            "mode": "grab"
                        },
                        "onclick": {
                            "enable": true,
                            "mode": "push"
                        },
                        "resize": true
                    },
                    "modes": {
                        "grab": {
                            "distance": 140,
                            "line_linked": {
                                "opacity": 0.4
                            }
                        },
                        "push": {
                            "particles_nb": 4
                        }
                    }
                },
                "retina_detect": true
            });
        });
    </script>
    """
    st.markdown(particles_js, unsafe_allow_html=True)

# 分析アニメーション
def show_analysis_animation():
    animation_html = """
    <div class="animation-container" id="analysis-animation">
        <div class="animation-content">
            <div style="width: 200px; height: 200px;">
                <svg width="200" height="200" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="40" stroke="#6C63FF" stroke-width="2" fill="none" stroke-dasharray="200" stroke-dashoffset="0">
                        <animate attributeName="stroke-dashoffset" from="0" to="600" dur="3s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="50" cy="50" r="30" stroke="#6EC5FF" stroke-width="2" fill="none" stroke-dasharray="150" stroke-dashoffset="0">
                        <animate attributeName="stroke-dashoffset" from="0" to="450" dur="3s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="50" cy="50" r="20" stroke="#FF6584" stroke-width="2" fill="none" stroke-dasharray="100" stroke-dashoffset="0">
                        <animate attributeName="stroke-dashoffset" from="0" to="300" dur="3s" repeatCount="indefinite" />
                    </circle>
                </svg>
            </div>
            <div class="analysis-text">
                <span id="analysis-message" class="shimmer">データ解析中...</span>
            </div>
        </div>
    </div>

    <script>
        // 分析メッセージを変更するアニメーション
        const messages = [
            "データ解析中...",
            "パターン分析中...",
            "特性抽出中...",
            "プロファイル作成中...",
            "結果生成中..."
        ];
        
        let currentIndex = 0;
        const messageElement = document.getElementById("analysis-message");
        
        const intervalId = setInterval(() => {
            if (messageElement) {
                messageElement.textContent = messages[currentIndex];
                currentIndex = (currentIndex + 1) % messages.length;
            }
        }, 1500);

        // 5秒後にアニメーションを非表示
        setTimeout(() => {
            const animation = document.getElementById("analysis-animation");
            if (animation) {
                animation.style.opacity = "0";
                animation.style.transition = "opacity 0.5s ease";
                
                setTimeout(() => {
                    if (animation) {
                        animation.style.display = "none";
                    }
                    clearInterval(intervalId);
                }, 500);
            }
        }, 4000); // 少し短くして4秒に変更
    </script>
    """
    components.html(animation_html, height=0)
    time.sleep(4.5)  # アニメーション時間に合わせて調整

def main():
    # セッション状態を初期化
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False
        st.session_state.birth_date = None
    
    # CSSとパーティクルの読み込み
    load_css()
    add_particles()
    
    # ヘッダー（パルスアニメーション削除）
    st.markdown('<h1>性格診断システム</h1>', unsafe_allow_html=True)
    st.markdown('<h2>生年月日から導き出す、あなただけの個性</h2>', unsafe_allow_html=True)
    
    # 日付入力セクション
    st.markdown('<div class="date-picker-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        birth_date = st.date_input(
            "🌟 生年月日を選択",
            datetime.date(1990, 1, 1),
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.datetime.now().date()
        )
        
        if st.button("診断を開始"):
            # セッション状態に保存
            st.session_state.analyzed = True
            st.session_state.birth_date = birth_date
            
            show_analysis_animation()  # 分析アニメーション表示
            st.rerun()  # 画面を再読み込み
    
    with col2:
        st.markdown("""
        <div style="padding: 20px; background: rgba(108, 99, 255, 0.1); border-radius: 10px; border: 1px solid rgba(108, 99, 255, 0.2);">
            <h3 style="margin-top: 0; font-size: 1.3rem;">あなただけの個性を解き明かす</h3>
            <p>このシステムは生年月日をもとに、東洋と西洋の様々な伝統的手法を用いて、あなたの持つ才能や特性を多角的に分析します。</p>
            <p>職場でのコミュニケーションスタイルや、チームでの役割、理想の働き方まで、あなたの本質に迫ります。</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 分析済みフラグがあれば結果を表示
    if st.session_state.analyzed and st.session_state.birth_date:
        run_diagnosis(st.session_state.birth_date)
    
    # エレガントなフッター
    st.markdown("""
    <div class="footer">
        <p>© 2023 性格診断システム | 高精度アルゴリズムによる分析</p>
    </div>
    """, unsafe_allow_html=True)

def run_diagnosis(birth_date):
    # 結果ヘッダー
    st.markdown(f"""
    <div class="result-header result-element">
        <h2>{birth_date.year}年{birth_date.month}月{birth_date.day}日生まれの診断結果</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # セパレーター
    st.markdown('<div class="section-divider result-element"><span>診断結果</span></div>', unsafe_allow_html=True)
    
    # 2列レイアウトで結果表示
    col1, col2 = st.columns(2)
    
    with col1:
        # 四柱推命
        try:
            result = shichuu_suimei.diagnose(birth_date)
            st.markdown(f"""
            <div class="result-card result-element">
                <div class="result-title">四柱推命</div>
                <div class="result-content">
                    <div class="data-point">
                        <span class="data-label">日柱天干：</span>
                        <span class="data-value glow">{result.get('ten_kan', '不明')}</span>
                    </div>
                    <div class="data-point">
                        <span class="data-label">日柱十二運：</span>
                        <span class="data-value">{result.get('juu_ni_shi', '不明')}</span>
                    </div>
                    <div class="data-point">
                        <span class="data-label">月干の蔵干宿命星：</span>
                        <span class="data-value">{result.get('tsuhen_sei', '不明')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"四柱推命データ取得エラー: {str(e)}")
        
        # 宿曜
        try:
            result = shukuyo.diagnose(birth_date)
            st.markdown(f"""
            <div class="result-card result-element">
                <div class="result-title">宿曜</div>
                <div class="result-content">
                    <div class="data-point">
                        <span class="data-value glow">{result.get('shukuyo', '不明')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"宿曜データ取得エラー: {str(e)}")
        
        # 陰陽五行
        try:
            result = onmyo_gogyo.diagnose(birth_date)
            st.markdown(f"""
            <div class="result-card result-element">
                <div class="result-title">陰陽五行</div>
                <div class="result-content">
                    <div class="data-point">
                        <span class="data-value glow">{result.get('gogyo', '不明')}の{result.get('inyo', '不明')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"陰陽五行データ取得エラー: {str(e)}")
    
    with col2:
        # 九星気学
        try:
            result = kyusei_kigaku.diagnose(birth_date)
            st.markdown(f"""
            <div class="result-card result-element">
                <div class="result-title">九星気学</div>
                <div class="result-content">
                    <div class="data-point">
                        <span class="data-label">本命星：</span>
                        <span class="data-value glow">{result.get('honmei_sei', '不明')}</span>
                    </div>
                    <div class="data-point">
                        <span class="data-label">月命星：</span>
                        <span class="data-value">{result.get('getsu_mei_sei', '不明')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"九星気学データ取得エラー: {str(e)}")
        
        # 西洋占星術
        try:
            result = western_astrology.diagnose(birth_date)
            st.markdown(f"""
            <div class="result-card result-element">
                <div class="result-title">西洋占星術</div>
                <div class="result-content">
                    <div class="data-point">
                        <span class="data-label">太陽：</span>
                        <span class="data-value glow">{result.get('sun_sign', '不明')}</span>
                    </div>
                    <div class="data-point">
                        <span class="data-label">月：</span>
                        <span class="data-value">{result.get('moon_sign', '不明')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"西洋占星術データ取得エラー: {str(e)}")
        
        # 動物占い
        try:
            result = animal_fortune.diagnose(birth_date)
            st.markdown(f"""
            <div class="result-card result-element">
                <div class="result-title">動物占い</div>
                <div class="result-content">
                    <div class="data-point">
                        <span class="data-value glow">{result.get('type', '不明')}となる{result.get('animal', '不明')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"動物占いデータ取得エラー: {str(e)}")
    
    # シェアボタン（機能は付けていない）
    st.markdown("""
    <div style="text-align: center; margin-top: 40px;" class="result-element">
        <button style="background: linear-gradient(135deg, #6C63FF, #6EC5FF); color: white; border: none; padding: 10px 25px; border-radius: 50px; font-weight: 500; margin: 0 10px; box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);">
            結果を保存
        </button>
        <button style="background: rgba(255, 255, 255, 0.1); color: white; border: 1px solid rgba(255, 255, 255, 0.2); padding: 10px 25px; border-radius: 50px; font-weight: 500; margin: 0 10px;">
            結果をシェア
        </button>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 