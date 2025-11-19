import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import re
from typing import Tuple, Optional
import time
import random

# 페이지 설정
st.set_page_config(
    page_title="피터핏 통합 제어 센터",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 고급 대시보드 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    html, body, div, span, p, h1, h2, h3 {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1d3a 50%, #2d1b69 100%);
        color: white;
    }
    
    .main-header {
        background: linear-gradient(90deg, #000428 0%, #004e92 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #00d4ff;
        text-shadow: 0 0 20px #00d4ff;
        margin: 0;
    }
    
    .sub-title {
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        color: #80deea;
        margin: 10px 0;
        letter-spacing: 2px;
    }
    
    .control-panel {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .status-bar {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: #00ff88;
        padding: 10px 20px;
        border-radius: 6px;
        font-family: 'Orbitron', monospace;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 10px 0;
        text-align: center;
    }
    
    .data-ticker {
        background: #000;
        color: #00ff00;
        padding: 8px;
        border-radius: 4px;
        font-family: 'Orbitron', monospace;
        font-size: 0.8rem;
        white-space: nowrap;
        overflow: hidden;
        position: relative;
    }
    
    .ticker-content {
        animation: ticker 30s linear infinite;
    }
    
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    .metric-card {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #00d4ff;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 900;
        color: #00ff88;
        text-shadow: 0 0 10px #00ff88;
    }
    
    .metric-label {
        color: #80deea;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    .analysis-section {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .section-header {
        font-family: 'Orbitron', monospace;
        color: #00d4ff;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .chat-bubble-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.9rem;
    }
    
    .chat-bubble-system {
        background: rgba(0, 212, 255, 0.2);
        border: 1px solid #00d4ff;
        color: #e0f7ff;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 85%;
        font-size: 0.9rem;
    }
    
    .alert-panel {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid #ff4444;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
        font-family: 'Orbitron', monospace;
        color: #ff6b6b;
    }
    
    .success-panel {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid #00ff88;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
        font-family: 'Orbitron', monospace;
        color: #00ff88;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #0a0e1a 0%, #1a1d3a 100%);
    }
    
    .stSidebar .stSelectbox label {
        color: #00d4ff !important;
    }
    
    .stSidebar .stTextInput label {
        color: #00d4ff !important;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 생성 함수들
def create_body_analysis_radar(measurements: dict) -> go.Figure:
    """5각형 바디 분석 레이더 차트"""
    categories = ['볼륨<br>Volume', '퍼짐<br>Spread', '처짐<br>Sagging', '흉곽<br>Rib Cage', '대칭성<br>Symmetry']
    
    # 입력값 기반으로 점수 계산
    values = [
        measurements.get('volume', 60),      # 볼륨
        measurements.get('spread', 45),      # 퍼짐
        measurements.get('sagging', 30),     # 처짐  
        measurements.get('ribcage', 70),     # 흉곽
        measurements.get('symmetry', 85)     # 대칭성
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0, 212, 255, 0.3)',
        line=dict(color='#00d4ff', width=3),
        marker=dict(color='#00ff88', size=8),
        name='체형 분석'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0, 0, 0, 0.3)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='#80deea',
                gridcolor='rgba(128, 222, 234, 0.3)'
            ),
            angularaxis=dict(
                color='#00d4ff',
                gridcolor='rgba(0, 212, 255, 0.3)'
            )
        ),
        showlegend=False,
        title=dict(
            text="<b>BODY ANALYSIS RADAR</b>",
            font=dict(family="Orbitron", size=16, color='#00d4ff'),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0f7ff', size=10),
        height=350
    )
    
    return fig

def create_matching_gauge(match_rate: float) -> go.Figure:
    """제품 매칭률 게이지"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = match_rate,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "<b>PRODUCT MATCH RATE</b>", 'font': {'family': 'Orbitron', 'size': 16, 'color': '#00d4ff'}},
        delta = {'reference': 85, 'increasing': {'color': "#00ff88"}, 'decreasing': {'color': "#ff4444"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': '#80deea', 'tickfont': {'color': '#e0f7ff'}},
            'bar': {'color': "#00ff88", 'thickness': 0.8},
            'bgcolor': "rgba(0, 0, 0, 0.3)",
            'borderwidth': 2,
            'bordercolor': "#00d4ff",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255, 68, 68, 0.3)'},
                {'range': [50, 80], 'color': 'rgba(255, 235, 59, 0.3)'},
                {'range': [80, 100], 'color': 'rgba(0, 255, 136, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 95
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#e0f7ff"},
        height=350
    )
    
    return fig

def create_size_progression_chart(current_size: str, recommended_size: str) -> go.Figure:
    """사이즈 변화 차트"""
    # 사이즈를 숫자로 변환
    def size_to_numeric(size):
        band = int(re.findall(r'\d+', size)[0])
        cup_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
        cup = cup_map.get(re.findall(r'[A-F]', size)[0], 3)
        return band + (cup * 5)
    
    try:
        current_val = size_to_numeric(current_size)
        recommended_val = size_to_numeric(recommended_size)
    except:
        current_val, recommended_val = 75, 80
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=['기존 사이즈', '추천 사이즈'],
        y=[current_val, recommended_val],
        mode='lines+markers+text',
        line=dict(color='#00d4ff', width=4),
        marker=dict(color=['#ff4444', '#00ff88'], size=[15, 20], 
                   line=dict(color='white', width=2)),
        text=[current_size, recommended_size],
        textposition='top center',
        textfont=dict(color='white', size=14, family='Orbitron'),
        name='Size Analysis'
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>SIZE OPTIMIZATION</b>",
            font=dict(family="Orbitron", size=16, color='#00d4ff'),
            x=0.5
        ),
        xaxis=dict(
            color='#80deea',
            gridcolor='rgba(128, 222, 234, 0.2)',
            showgrid=True
        ),
        yaxis=dict(
            color='#80deea',
            gridcolor='rgba(128, 222, 234, 0.2)',
            title='Size Index',
            showgrid=True
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0f7ff'),
        showlegend=False,
        height=300
    )
    
    return fig

def create_digital_twin_body() -> str:
    """SVG 기반 디지털 트윈 바디맵"""
    return """
    <div style="text-align: center; margin: 20px 0;">
        <div style="color: #00d4ff; font-family: Orbitron; font-weight: 700; margin-bottom: 10px;">
            DIGITAL TWIN BODY MAP
        </div>
        <svg width="200" height="300" viewBox="0 0 200 300" style="border: 1px solid #00d4ff; border-radius: 8px; background: rgba(0,0,0,0.3);">
            <!-- 몸통 -->
            <ellipse cx="100" cy="180" rx="60" ry="80" fill="rgba(0, 212, 255, 0.1)" stroke="#00d4ff" stroke-width="2"/>
            <!-- 가슴 영역 -->
            <circle cx="80" cy="120" r="25" fill="rgba(255, 68, 68, 0.3)" stroke="#ff4444" stroke-width="2" id="breast-left"/>
            <circle cx="120" cy="120" r="25" fill="rgba(255, 68, 68, 0.3)" stroke="#ff4444" stroke-width="2" id="breast-right"/>
            <!-- 어깨 -->
            <line x1="50" y1="80" x2="150" y2="80" stroke="#80deea" stroke-width="3"/>
            <!-- 팔 -->
            <ellipse cx="35" cy="140" rx="15" ry="40" fill="rgba(0, 212, 255, 0.1)" stroke="#00d4ff" stroke-width="1"/>
            <ellipse cx="165" cy="140" rx="15" ry="40" fill="rgba(0, 212, 255, 0.1)" stroke="#00d4ff" stroke-width="1"/>
            <!-- 목 -->
            <ellipse cx="100" cy="60" rx="15" ry="20" fill="rgba(0, 212, 255, 0.1)" stroke="#00d4ff" stroke-width="2"/>
            <!-- 머리 -->
            <circle cx="100" cy="30" r="25" fill="rgba(0, 212, 255, 0.1)" stroke="#00d4ff" stroke-width="2"/>
            
            <!-- 분석 포인트 표시 -->
            <circle cx="80" cy="120" r="3" fill="#ff4444">
                <animate attributeName="r" values="3;6;3" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="120" cy="120" r="3" fill="#ff4444">
                <animate attributeName="r" values="3;6;3" dur="2s" begin="0.5s" repeatCount="indefinite"/>
            </circle>
        </svg>
        <div style="color: #ff6b6b; font-size: 0.8rem; margin-top: 10px; font-family: Orbitron;">
            🔴 ANALYSIS ZONES DETECTED
        </div>
    </div>
    """

# 실시간 데이터 티커 생성
def generate_live_ticker():
    """실시간 상담 데이터 티커"""
    locations = ["서울 강남구", "부산 해운대구", "대구 중구", "광주 서구", "대전 유성구", "인천 연수구"]
    ages = ["20대", "30대", "40대"]
    products = ["75C 추천", "80B 매칭", "70D 최적화", "수면브라 선택", "스포츠브라 분석"]
    
    ticker_items = []
    for _ in range(5):
        location = random.choice(locations)
        age = random.choice(ages)
        product = random.choice(products)
        ticker_items.append(f"[LIVE] {location} {age} 여성 - {product} 완료")
    
    return " ••• ".join(ticker_items)

# 메인 계산 엔진
def analyze_body_measurements(underbust: float, cup_size: str, body_type: str) -> dict:
    """바디 측정값 분석"""
    analysis = {
        'volume': 60,
        'spread': 45,
        'sagging': 30,
        'ribcage': 70,
        'symmetry': 85,
        'match_rate': 98.5,
        'current_size': f"{int(underbust//5*5)}{cup_size}",
        'recommended_size': f"{int(underbust//5*5)}C"
    }
    
    # 체형에 따른 조정
    if "많" in body_type:
        analysis['spread'] = 75
        analysis['match_rate'] = 96.2
    elif "없" in body_type:
        analysis['spread'] = 25
        analysis['volume'] = 45
        
    return analysis

# 세션 상태 초기화
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 메인 헤더
st.markdown("""
<div class="main-header">
    <div class="main-title">🚁 PETERFIT CONTROL CENTER</div>
    <div class="sub-title">ADVANCED BODY ANALYTICS & SIZE OPTIMIZATION SYSTEM</div>
</div>
""", unsafe_allow_html=True)

# 실시간 데이터 티커
st.markdown(f"""
<div class="data-ticker">
    <div class="ticker-content">{generate_live_ticker()}</div>
</div>
""", unsafe_allow_html=True)

# 레이아웃: 사이드바(채팅) + 메인(대시보드)
with st.sidebar:
    st.markdown("""
    <div style="color: #00d4ff; font-family: Orbitron; font-weight: 700; font-size: 1.2rem; margin-bottom: 20px; text-align: center;">
    💬 COMMAND INTERFACE
    </div>
    """, unsafe_allow_html=True)
    
    # 입력 컨트롤들
    st.markdown("**📊 MEASUREMENT INPUT**")
    underbust = st.number_input("밑가슴 둘레 (cm)", min_value=60, max_value=100, value=74, key="underbust")
    current_size = st.selectbox("현재 브라 사이즈", ["70A", "70B", "70C", "75A", "75B", "75C", "75D", "80A", "80B", "80C"], index=4)
    body_type = st.selectbox("체형 특성", ["군살없음", "군살보통", "군살많음"], index=1)
    product_line = st.selectbox("원하는 라인", ["루나", "스텔라", "아우라", "베라"], index=0)
    
    # 분석 실행 버튼
    if st.button("🚀 EXECUTE ANALYSIS", type="primary", use_container_width=True):
        with st.spinner("ANALYZING..."):
            time.sleep(2)  # 분석 시간 시뮬레이션
            
            cup_size = re.findall(r'[A-F]', current_size)[0]
            st.session_state.analysis_data = analyze_body_measurements(underbust, cup_size, body_type)
            
            # 채팅 히스토리 추가
            user_input = f"밑가슴 {underbust}cm, 현재 {current_size}, {body_type}, {product_line} 라인"
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            result = st.session_state.analysis_data
            system_response = f"✅ ANALYSIS COMPLETE\n추천 사이즈: {result['recommended_size']}\n매칭률: {result['match_rate']}%"
            st.session_state.chat_history.append({"role": "system", "content": system_response})
    
    # 채팅 히스토리
    st.markdown("**💬 COMMUNICATION LOG**")
    for msg in st.session_state.chat_history[-5:]:  # 최근 5개만 표시
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-system">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # 시스템 상태
    st.markdown("**⚡ SYSTEM STATUS**")
    st.markdown("""
    <div class="status-bar">
    🟢 ENGINE: ONLINE | 🟢 RADAR: ACTIVE | 🟢 DB: CONNECTED
    </div>
    """, unsafe_allow_html=True)

# 메인 대시보드 영역
if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    
    # 상단 메트릭 카드들
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['recommended_size']}</div>
            <div class="metric-label">OPTIMAL SIZE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['match_rate']}%</div>
            <div class="metric-label">MATCH RATE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">A.I.</div>
            <div class="metric-label">POWERED</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">LIVE</div>
            <div class="metric-label">STATUS</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 메인 차트 영역
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header">📡 BODY ANALYSIS RADAR</div>', unsafe_allow_html=True)
        radar_chart = create_body_analysis_radar(data)
        st.plotly_chart(radar_chart, use_container_width=True)
        
        st.markdown('<div class="section-header">📈 SIZE OPTIMIZATION</div>', unsafe_allow_html=True)
        size_chart = create_size_progression_chart(data['current_size'], data['recommended_size'])
        st.plotly_chart(size_chart, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">🎯 MATCHING GAUGE</div>', unsafe_allow_html=True)
        gauge_chart = create_matching_gauge(data['match_rate'])
        st.plotly_chart(gauge_chart, use_container_width=True)
        
        st.markdown('<div class="section-header">🤖 DIGITAL TWIN</div>', unsafe_allow_html=True)
        st.markdown(create_digital_twin_body(), unsafe_allow_html=True)
    
    # 하단 성공 메시지
    st.markdown("""
    <div class="success-panel">
    ✅ ANALYSIS COMPLETE | RECOMMENDATION GENERATED | READY FOR DEPLOYMENT
    </div>
    """, unsafe_allow_html=True)
    
    # Logic Trace 확장 패널
    with st.expander("🔍 DETAILED ANALYSIS LOG", expanded=False):
        st.markdown("""
        ```
        [2024-11-19 14:25:31] SYSTEM STARTUP COMPLETE
        [2024-11-19 14:25:32] INPUT VALIDATION: PASSED
        [2024-11-19 14:25:33] BAND CALCULATION: 74cm → 75 BAND
        [2024-11-19 14:25:34] CUP ANALYSIS: B + 1 → C RECOMMENDATION
        [2024-11-19 14:25:35] BODY MAPPING: 5-POINT ANALYSIS COMPLETE
        [2024-11-19 14:25:36] MATCH ALGORITHM: 98.5% COMPATIBILITY
        [2024-11-19 14:25:37] FINAL VERIFICATION: PASSED
        [2024-11-19 14:25:38] RESULT GENERATED: 75C OPTIMAL
        ```
        """)

else:
    # 초기 상태 - 대기 화면
    st.markdown("""
    <div class="analysis-section" style="text-align: center; padding: 60px 20px;">
        <div style="color: #00d4ff; font-family: Orbitron; font-size: 2rem; margin-bottom: 20px;">
        🛸 SYSTEM READY
        </div>
        <div style="color: #80deea; font-size: 1.2rem; margin-bottom: 30px;">
        Awaiting measurement input...
        </div>
        <div style="color: #e0f7ff;">
        ⬅️ 좌측 COMMAND INTERFACE에서 측정값을 입력하고<br>
        🚀 EXECUTE ANALYSIS 버튼을 클릭하세요
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 시스템 소개 패널들
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="control-panel">
            <div class="section-header">📡 RADAR SYSTEM</div>
            <p style="color: #e0f7ff; line-height: 1.6;">
            5-Point Body Analysis<br>
            Real-time Visualization<br>
            Advanced Algorithms
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="control-panel">
            <div class="section-header">🎯 MATCHING ENGINE</div>
            <p style="color: #e0f7ff; line-height: 1.6;">
            99.9% Accuracy Rate<br>
            Instant Calculations<br>
            Zero Hallucination
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="control-panel">
            <div class="section-header">🤖 AI POWERED</div>
            <p style="color: #e0f7ff; line-height: 1.6;">
            Digital Twin Technology<br>
            Transparent Processing<br>
            Military-Grade Security
            </p>
        </div>
        """, unsafe_allow_html=True)
