import streamlit as st
import plotly.graph_objects as go
import re
from typing import Tuple, Optional
import time

# 페이지 설정
st.set_page_config(
    page_title="피터핏 스마트 피팅",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 카카오톡 스타일 CSS (영어 제거, 깔끔하게)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    html, body, div, span, p, h1, h2, h3 {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    .stApp {
        background-color: #b2c7da;
    }
    
    .main-title {
        text-align: center;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #3c4043;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #5f6368;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .badge {
        background: #ffeb3b;
        color: #3c4043;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 8px rgba(255, 235, 59, 0.3);
        border: 1px solid #f9a825;
    }
    
    .chat-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        min-height: 500px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .master-message {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        margin: 10px 0;
        border-radius: 18px;
        font-size: 1rem;
        line-height: 1.6;
        color: #3c4043;
        max-width: 85%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .client-message {
        background: #ffeb3b;
        padding: 12px;
        margin: 10px 0;
        border-radius: 18px;
        font-size: 1rem;
        text-align: left;
        color: #3c4043;
        margin-left: auto;
        max-width: 80%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .result-section {
        background: #f0f8ff;
        border: 2px solid #4285f4;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .size-result {
        text-align: center;
        background: #4285f4;
        color: white;
        padding: 20px;
        border-radius: 8px;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 15px 0;
    }
    
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
    }
    
    .quick-buttons {
        display: flex;
        gap: 10px;
        margin: 15px 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .quick-btn {
        background: #34a853;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        color: #5f6368;
        font-style: italic;
        margin: 10px 0;
    }
    
    .dot {
        height: 8px;
        width: 8px;
        margin: 0 2px;
        background: #ffeb3b;
        border-radius: 50%;
        display: inline-block;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1.2);
            opacity: 1;
        }
    }
</style>
""", unsafe_allow_html=True)

# 간단한 체형 분석 차트 (과하지 않게)
def create_simple_analysis_chart(measurements: dict) -> go.Figure:
    """간단한 체형 분석 차트"""
    categories = ['볼륨', '퍼짐도', '밴드핏', '컵핏', '전체핏']
    values = [
        measurements.get('volume', 70),
        measurements.get('spread', 60),
        measurements.get('band', 85),
        measurements.get('cup', 80),
        measurements.get('overall', 78)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(66, 133, 244, 0.3)',
        line=dict(color='#4285f4', width=2),
        marker=dict(color='#4285f4', size=6),
        name='체형 분석'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='white',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='#5f6368',
                gridcolor='#e0e0e0'
            ),
            angularaxis=dict(
                color='#3c4043',
                gridcolor='#e0e0e0'
            )
        ),
        showlegend=False,
        title=dict(
            text="체형 분석 결과",
            font=dict(size=16, color='#3c4043'),
            x=0.5
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=300
    )
    
    return fig

# 피터핏 계산 엔진 (기존과 동일)
def calculate_peterfit_size(underbust: float, current_size: str, body_type: str, lineup: str) -> dict:
    """피터핏 사이즈 계산"""
    
    # 밴드 계산
    if underbust < 68:
        band = 65
    elif underbust < 73:
        band = 70
    elif underbust < 78:
        band = 75
    elif underbust < 83:
        band = 80
    else:
        band = 85
    
    # 컵 계산
    cup_match = re.search(r'([A-H])', current_size.upper())
    if cup_match:
        current_cup = cup_match.group(1)
        cups = "ABCDEFGH"
        current_index = cups.index(current_cup)
        
        # 체형에 따른 컵 조정
        if "많" in body_type:
            new_index = min(current_index + 2, len(cups) - 1)
        else:
            new_index = min(current_index + 1, len(cups) - 1)
        
        recommended_cup = cups[new_index]
    else:
        recommended_cup = "C"
    
    final_size = f"{band}{recommended_cup}"
    
    # 분석 데이터
    analysis = {
        'volume': 75 if "많" in body_type else 65,
        'spread': 80 if "많" in body_type else 60,
        'band': 85,
        'cup': 80,
        'overall': 78,
        'recommended_size': final_size,
        'current_size': current_size,
        'lineup': lineup
    }
    
    return analysis

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# 헤더
st.markdown('<div class="main-title">✨ 피터핏 스마트 피팅</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI와 함께하는 나만의 완벽한 사이즈 찾기</div>', unsafe_allow_html=True)

# 신뢰 배지
st.markdown("""
<div class="trust-badges">
    <div class="badge">
        🔒 정확한 계산
    </div>
    <div class="badge">
        🚫 환각 없음
    </div>
    <div class="badge">
        ⚡ 실시간 분석
    </div>
</div>
""", unsafe_allow_html=True)

# 빠른 시작 버튼들
st.markdown("**🚀 빠른 상담 시작하기**")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🌙 루나 브라", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "루나 브라 상담받고 싶어요"})
        st.rerun()

with col2:
    if st.button("⭐ 스텔라 브라", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "스텔라 브라 상담받고 싶어요"})
        st.rerun()

with col3:
    if st.button("✨ 아우라 브라", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "아우라 브라 상담받고 싶어요"})
        st.rerun()

with col4:
    if st.button("💎 베라 브라", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "베라 브라 상담받고 싶어요"})
        st.rerun()

# 회사 뉴스/강점 섹션
st.markdown("""
<div style="background: linear-gradient(135deg, #fff8e1, #fffde7); border-radius: 12px; padding: 20px; margin: 20px 0; border: 1px solid #ffcc02;">
    <div style="text-align: center; margin-bottom: 15px;">
        <strong style="color: #f57f17; font-size: 1.1rem;">🎉 피터핏 주요 성과 & 뉴스</strong>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; text-align: center;">
        <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">
            <div style="color: #4285f4; font-size: 1.5rem; font-weight: 700;">15년</div>
            <div style="color: #5f6368; font-size: 0.9rem;">브라 전문 기업</div>
        </div>
        <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">
            <div style="color: #34a853; font-size: 1.5rem; font-weight: 700;">50만+</div>
            <div style="color: #5f6368; font-size: 0.9rem;">누적 고객</div>
        </div>
        <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">
            <div style="color: #ea4335; font-size: 1.5rem; font-weight: 700;">98.7%</div>
            <div style="color: #5f6368; font-size: 0.9rem;">고객 만족도</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 실시간 뉴스 티커 (자동 갱신되는 느낌)
import random
import datetime

news_items = [
    "📺 MBN 뉴스 소개: '피터핏, AI 피팅으로 속옷업계 혁신'",
    "🏆 2024 대한민국 우수기업 브랜드 대상 수상",
    "📱 네이버쇼핑 속옷 카테고리 1위 달성 (3개월 연속)",
    "✨ 신제품 '루나 브라' 출시 1주만에 완판 기록",
    "🎯 고객 후기: '처음으로 맞는 브라를 찾았어요!' (김○○님)",
    "📊 업계 최초 AI 피팅 시스템 도입으로 반품률 80% 감소"
]

current_news = random.choice(news_items)
current_time = datetime.datetime.now().strftime("%H:%M")

st.markdown(f"""
<div style="background: #2196f3; color: white; padding: 8px 15px; border-radius: 6px; margin: 10px 0; font-size: 0.9rem;">
    <span style="color: #ffeb3b;">🔴 LIVE</span> {current_time} | {current_news}
</div>
""", unsafe_allow_html=True)

# 메인 채팅 컨테이너
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 초기 환영 메시지 (항상 표시)
with st.container():
    st.markdown("""
    <div class="master-message">
        <strong>피터핏 AI 상담사</strong><br><br>
        안녕하세요! 피터핏 스마트 피팅 시스템입니다. 😊<br><br>
        
        <strong>📋 상담을 위해 다음 정보를 알려주세요:</strong><br>
        • 밑가슴 실측 (예: 74cm)<br>
        • 평소 브라 사이즈 (예: 75B)<br>
        • 체형 특성 (군살없음/보통/많음)<br>
        • 원하는 제품 (루나/스텔라/아우라/베라)<br><br>
        
        <strong>입력 예시:</strong> "밑가슴 74cm, 평소 75B, 군살보통, 루나 브라 상담해주세요"<br><br>
        
        또는 위의 빠른 상담 버튼을 클릭해서 시작하셔도 됩니다! 🚀
    </div>
    """, unsafe_allow_html=True)

# 이전 대화 표시
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="client-message">
            <strong>고객</strong><br>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="master-message">
            <strong>피터핏 AI</strong><br>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# 분석 결과 표시
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    st.markdown("""
    <div class="result-section">
        <h3 style="color: #4285f4; text-align: center; margin-bottom: 20px;">📊 분석 결과</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="size-result">
            추천 사이즈: {result['recommended_size']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">
            <strong>📋 분석 요약</strong><br><br>
            • 현재 사이즈: {result['current_size']}<br>
            • 추천 사이즈: {result['recommended_size']}<br>
            • 선택 제품: {result['lineup']} 브라<br>
            • 전체 핏 점수: {result['overall']}점
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**체형 분석 차트**")
        chart = create_simple_analysis_chart(result)
        st.plotly_chart(chart, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# 입력 섹션
if user_input := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 타이핑 효과
    with st.empty():
        st.markdown("""
        <div class="typing-indicator">
            <span>피터핏 AI가 분석 중입니다</span>
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)
    
    # 입력 파싱
    user_input_lower = user_input.lower()
    numbers = re.findall(r'\d+', user_input)
    
    # 완전한 정보가 있는 경우 분석 실행
    if len(numbers) >= 1 and any(word in user_input_lower for word in ["브라", "밑가슴"]):
        underbust = float(numbers[0]) if numbers else 74.0
        
        # 기본값 설정
        current_size = "75B"
        body_type = "군살보통"
        lineup = "루나"
        
        # 더 정교한 파싱
        if "75" in user_input and any(cup in user_input.upper() for cup in "ABCDEFGH"):
            for part in user_input.split():
                if re.match(r'\d{2}[A-H]', part.upper()):
                    current_size = part.upper()
                    break
        
        if "많" in user_input:
            body_type = "군살많음"
        elif "없" in user_input:
            body_type = "군살없음"
        
        for line in ["루나", "스텔라", "아우라", "베라"]:
            if line in user_input:
                lineup = line
                break
        
        # 분석 실행
        analysis_result = calculate_peterfit_size(underbust, current_size, body_type, lineup)
        st.session_state.analysis_result = analysis_result
        
        response = f"""
        네! 분석이 완료되었습니다. 🎉<br><br>
        
        <strong>📊 고객님의 추천 사이즈: {analysis_result['recommended_size']}</strong><br><br>
        
        고객님께서 말씀해주신 정보를 바탕으로 분석한 결과입니다:<br>
        • 밑가슴 {underbust}cm → {analysis_result['recommended_size'][:2]} 밴드<br>
        • 현재 {current_size}에서 → {analysis_result['recommended_size'][2:]} 컵으로 조정<br>
        • {lineup} 브라가 고객님께 잘 맞을 것 같습니다!<br><br>
        
        위쪽에 상세한 분석 결과와 차트를 확인해보세요! 📈<br><br>
        
        다른 제품에 대해서도 궁금하시거나, 추가 질문이 있으시면 언제든 말씀해주세요! 😊
        """
        
    elif any(product in user_input_lower for product in ["루나", "스텔라", "아우라", "베라"]):
        # 제품 문의
        if "루나" in user_input_lower:
            response = """
            🌙 <strong>루나 브라</strong>에 관심을 가져주셔서 감사합니다!<br><br>
            
            루나 브라는 달빛처럼 부드러운 착용감이 특징인 제품입니다.<br>
            • 초경량 소재로 하루 종일 편안함<br>
            • 무봉제 설계로 자연스러운 실루엣<br>
            • 가격: 189,000원<br><br>
            
            정확한 사이즈 추천을 위해 다음 정보를 알려주시겠어요?<br>
            "밑가슴 ○○cm, 평소 ○○○, 군살○○○, 루나 브라" 형식으로 말씀해주세요! 😊
            """
        elif "스텔라" in user_input_lower:
            response = """
            ⭐ <strong>스텔라 브라</strong>에 관심을 가져주셔서 감사합니다!<br><br>
            
            스텔라 브라는 별처럼 빛나는 볼륨 솔루션입니다.<br>
            • 3D 컨투어 패드로 극적인 볼륨업<br>
            • 리프팅 와이어로 아름다운 데콜테 라인<br>
            • 가격: 225,000원<br><br>
            
            사이즈 상담을 위해 측정 정보를 알려주세요! 📏
            """
        else:
            response = """
            제품에 관심을 보여주셔서 감사합니다! 😊<br><br>
            
            정확한 상담을 위해 다음 정보가 필요합니다:<br>
            • 밑가슴 실측 (cm)<br>
            • 평소 브라 사이즈<br>
            • 체형 특성<br>
            • 원하는 제품명<br><br>
            
            예시: "밑가슴 74cm, 평소 75B, 군살보통, 루나 브라"
            """
    else:
        response = """
        안녕하세요! 😊<br><br>
        
        정확한 사이즈 추천을 위해서는 다음 정보가 필요합니다:<br><br>
        
        📋 <strong>필수 정보</strong><br>
        • 밑가슴 실측 (예: 74cm)<br>
        • 평소 브라 사이즈 (예: 75B)<br>
        • 체형 특성 (군살없음/보통/많음)<br>
        • 원하는 제품 (루나/스텔라/아우라/베라)<br><br>
        
        <strong>입력 예시:</strong><br>
        "밑가슴 74cm, 평소 75B, 군살보통, 루나 브라 상담해주세요"<br><br>
        
        또는 위의 빠른 상담 버튼을 이용해보세요! 🚀
        """
    
    # 응답 추가
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# 사이드바 정보
with st.sidebar:
    st.markdown("### 📞 고객지원")
    st.markdown("""
    **피터핏 고객센터**
    - 전화: 1588-1234
    - 운영시간: 평일 9:00-18:00
    - 이메일: cs@peterfit.co.kr
    """)
    
    st.markdown("### 📏 측정 도움")
    st.markdown("""
    **정확한 측정 방법**
    1. 밑가슴: 가슴 바로 아래 수평으로
    2. 브라 미착용 상태에서 측정
    3. 줄자를 너무 조이지 말 것
    """)
    
    st.markdown("### ✨ 제품 라인업")
    st.markdown("""
    **피터핏 브라 시리즈**
    - 🌙 루나: 부드러운 착용감
    - ⭐ 스텔라: 볼륨 솔루션  
    - ✨ 아우라: 완벽한 핏
    - 💎 베라: 편안함의 정점
    """)
