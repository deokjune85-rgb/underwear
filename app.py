import streamlit as st
import plotly.graph_objects as go
import time
import re
import random
import datetime

# ==========================================
# [1. 시스템 설정 및 디자인]
# ==========================================
st.set_page_config(
    page_title="IMD 스마트 피팅 마스터",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 카카오톡 친숙한 감성 + IMD 브랜딩 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stApp {
        background-color: #e6e6e6; /* 카톡 배경색 */
        color: #333333;
    }

    /* 뉴스 티커 */
    .news-ticker {
        background: #f7e600; /* 카톡 노랑 */
        border-left: 4px solid #ccab00; /* 진한 노랑 */
        color: #3c4043;
        padding: 10px 20px;
        font-size: 0.9rem;
        border-radius: 4px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 신뢰 배지 */
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .badge {
        background: #ffe656; /* 카톡 노랑 */
        border: 1px solid #ccab00;
        color: #3c4043;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* 채팅 스타일 */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 15px; /* 간격 조절 */
        padding-bottom: 50px;
    }
    
    .bot-message {
        background-color: #ffffff; /* 흰색 말풍선 */
        border: 1px solid #e0e0e0;
        border-radius: 15px 15px 15px 0; /* 카톡 좌측 말풍선 */
        color: #333333;
        padding: 15px;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        animation: fadeIn 0.5s ease-out;
        max-width: 85%;
    }
    
    .user-message {
        background: #f7e600; /* 카톡 사용자 말풍선 */
        color: #3c4043;
        padding: 15px 20px;
        border-radius: 15px 15px 0 15px; /* 카톡 우측 말풍선 */
        align-self: flex-end;
        margin-left: auto;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-out;
        max-width: 80%;
        text-align: right;
    }

    .phase-tag {
        font-size: 0.75rem;
        color: #888;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 최종 리포트 대시보드 */
    .final-dashboard {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 15px;
        padding: 25px;
        margin-top: 25px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .kpi-box {
        background-color: #f7f7f7;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 900;
        color: #1a73e8; /* 구글 블루 */
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #5f6368;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 버튼 커스텀 */
    .stButton > button {
        background-color: #f7e600; /* 카톡 노랑 */
        color: #3c4043;
        border: 1px solid #ccab00;
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #ffe656;
        border-color: #bfa000;
    }
    /* 최종 CTA 버튼 */
    .final-cta-button {
        background: linear-gradient(90deg, #1a73e8, #4285f4); /* 구글 블루 그라데이션 */
        color: #fff;
        border: none;
        padding: 15px 40px;
        font-weight: 900;
        font-size: 1.1rem;
        border-radius: 50px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4);
        transition: background 0.3s, transform 0.2s;
    }
    .final-cta-button:hover {
        background: linear-gradient(90deg, #4285f4, #1a73e8);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 로직 및 차트 함수]
# ==========================================

def create_analysis_chart(user_data):
    """5각 레이더 차트 생성 (카카오톡 감성 색상)"""
    # 입력 데이터에 따른 동적 점수 산정
    flab_score = 80 if "많음" in user_data.get('flab', '') else (60 if "보통" in user_data.get('flab', '') else 40)
    shape_score = 85 if "처진" in user_data.get('shape', '') else (70 if "퍼진" in user_data.get('shape', '') else 50)
    cup_gap = 90 if "여유 많음" in user_data.get('cup_status', '') else (70 if "넘침" in user_data.get('cup_status', '') else 30)
    
    categories = ['군살 보정', '가슴 퍼짐', '리프팅', '볼륨 부족', '비대칭']
    values = [flab_score, 70, shape_score, cup_gap, 40]  # 시뮬레이션 값
    values += [values[0]] # 폐곡선
    categories += [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 235, 59, 0.4)', # 카톡 노랑 투명
        line=dict(color='#f7e600', width=2), # 카톡 노랑
        marker=dict(color='#3c4043', size=4), # 진한 회색
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#ffffff', # 흰색 배경
            radialaxis=dict(visible=True, range=[0, 100], color='#a0a0a0', gridcolor='#e0e0e0'),
            angularaxis=dict(color='#3c4043', gridcolor='#e0e0e0')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=350,
        title=dict(
            text="IMD AI 체형 분석",
            font=dict(size=16, color='#3c4043'),
            x=0.5
        ),
    )
    return fig

# IMD 가상 제품 라인업
imd_products = {
    "포근핏": {
        "desc": "매일 입어도 편안한 데일리 브라. 부드러운 소재와 와이어리스 설계로 몸의 곡선을 자연스럽게 감싸줍니다.",
        "features": ["와이어리스", "데일리", "편안함", "자연스러운 핏"],
        "price": "89,000원"
    },
    "퍼펙트핏": {
        "desc": "빈틈없이 완벽한 핏을 선사하는 보정 브라. 넓은 날개와 사이드 패널이 군살을 효과적으로 정리하고 가슴을 안정적으로 잡아줍니다.",
        "features": ["군살 정리", "탄탄한 지지", "완벽한 보정", "활동성"],
        "price": "129,000원"
    },
    "볼륨업핏": {
        "desc": "놀라운 볼륨감을 선사하는 브라. 특수 패드와 리프팅 설계로 밋밋한 가슴도 드라마틱하게 연출해줍니다.",
        "features": ["볼륨업", "가슴골 연출", "리프팅 효과", "자신감 상승"],
        "price": "119,000원"
    },
    "슬림핏": {
        "desc": "가볍고 시원하게 몸에 착 감기는 슬림 브라. 얇은 두께와 통기성 소재로 답답함 없이 매끄러운 실루엣을 만들어줍니다.",
        "features": ["얇고 가벼움", "통기성", "매끄러운 실루엣", "여름용"],
        "price": "99,000원"
    }
}


# 시나리오 데이터 (순차적 질문)
questions = [
    {
        "phase": "1단계: 기본 정보 입력",
        "question": "안녕하세요! 고객님의 완벽한 핏을 찾아드리는 **IMD 피팅 마스터 AI**입니다.\n15년간 축적된 데이터로 정밀 진단을 시작합니다.\n\n먼저, **밑가슴 둘레 실측 사이즈(cm)**를 알려주세요. 줄자로 갈비뼈 바로 아랫부분을 수평으로 타이트하게 측정해주시면 됩니다.",
        "key": "underbust",
        "type": "number",
        "confirm": "네, 밑가슴 둘레 **{value}cm** 확인했습니다. 밴드 사이즈를 계산합니다."
    },
    {
        "phase": "2단계: 현재 브라 상태",
        "question": "현재 가장 자주 착용하시는 **일반 브라 사이즈**는 어떻게 되시나요? (예: 80B, 75A)",
        "key": "current_bra",
        "type": "text",
        "confirm": "현재 착용 사이즈 **{value}**를 기준으로 고객님의 컵 적합도를 분석하겠습니다."
    },
    {
        "phase": "3단계: 컵 피팅 진단",
        "question": "지금 브라를 착용했을 때, **컵의 상태**는 어떠신가요?\n(컵이 남거나 넘치는 것은 현재 브라가 가슴 형태와 맞지 않는다는 신호입니다.)",
        "key": "cup_status",
        "type": "select",
        "options": ["① 컵이 많이 남음 (들뜸)", "② 약간 남음", "③ 딱 맞음", "④ 컵이 넘침 (눌림)"],
        "confirm": "컵 피팅 상태 **'{value}'** 확인했습니다. 컵 용량 재산정이 필요합니다."
    },
    {
        "phase": "4단계: 체형 특성 분석",
        "question": "가슴 주변(겨드랑이, 등)의 **군살 정도**를 선택해주세요.\n이는 보정력이 필요한 제품 선택에 중요한 기준이 됩니다.",
        "key": "flab",
        "type": "select",
        "options": ["① 군살 거의 없음", "② 약간 있음", "③ 보통", "④ 군살 많음"],
        "confirm": "고객님의 체형 특성 **'{value}'** 데이터를 입력했습니다."
    },
    {
        "phase": "5단계: 가슴 형태 확인",
        "question": "고객님의 **가슴 형태**에 가장 해당되는 특징을 모두 선택해주세요. (중복 선택 가능)",
        "key": "shape",
        "type": "multiselect", # 다중 선택으로 변경
        "options": ["① 처진 가슴", "② 퍼진 가슴 (벌어짐)", "③ 윗가슴 꺼짐", "④ 탄력 저하", "⑤ 일반/원형"],
        "confirm": "가슴 형태 데이터 **'{value}'**까지 모두 수집 완료되었습니다. 잠시만 기다려주시면 IMD AI가 최적의 결과를 브리핑하겠습니다."
    }
]

# ==========================================
# [3. 메인 실행 코드]
# ==========================================

# 세션 상태 관리
if 'step' not in st.session_state: st.session_state.step = 0
if 'history' not in st.session_state: st.session_state.history = []
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# 1. 헤더 영역 (뉴스 티커 + 배지)
current_time = datetime.datetime.now().strftime("%H:%M")
news = [
    "IMD AI, 고객별 맞춤형 추천으로 반품률 획기적 감소!",
    "이제 내 몸에 꼭 맞는 브라를 5분 안에! IMD 스마트 피팅",
    "수많은 고객들이 IMD AI로 인생 브라를 찾았습니다! 지금 바로 경험해보세요."
]
st.markdown(f"""
<div class='news-ticker'>
    <span style='color: #da3d3d; margin-right: 10px;'>⚡️ 실시간 혜택!</span> {random.choice(news)}
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #3c4043; font-size: 3rem; font-weight: 900;'>IMD 스마트 피팅 마스터</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5f6368;'>IMD 15년 노하우가 집약된 AI 피팅 엔진 v2.5</p>", unsafe_allow_html=True)

st.markdown("""
<div class="trust-badges">
    <div class="badge">✨ IMD만의 정밀 로직</div>
    <div class="badge">🛡️ 오류 없는 정확성</div>
    <div class="badge">🚀 5분 실시간 분석</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# 2. 채팅 인터페이스
chat_placeholder = st.container()

with chat_placeholder:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    # 히스토리 렌더링
    for msg in st.session_state.history:
        if msg['role'] == 'bot':
            st.markdown(f"""
            <div style='align-self: flex-start; max-width: 100%;'>
                <div class='phase-tag'>{msg.get('phase', '')}</div>
                <div class='bot-message'>{msg['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='user-message'>{msg['text']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3. 입력 처리 및 로직
if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    
    # 현재 질문 표시 (히스토리에 없을 때만)
    # 중복 방지 로직: 현재 스텝의 질문이 마지막 봇 메시지가 아니면 추가
    last_bot_msg_text = ""
    for m in reversed(st.session_state.history):
        if m['role'] == 'bot':
            last_bot_msg_text = m['text']
            break
    
    if q['question'] not in last_bot_msg_text:
        st.session_state.history.append({"role": "bot", "text": q['question'], "phase": q['phase']})
        st.rerun()

    # 입력 위젯 영역
    with st.container():
        st.write("") # 빈 공간 확보
        
        if q['type'] in ['text', 'number']:
            with st.form(key=f"form_{st.session_state.step}"):
                user_val = st.text_input("답변을 입력해주세요.", key=f"input_{st.session_state.step}")
                submit = st.form_submit_button("입력하기 ➔")
                
            if submit and user_val:
                st.session_state.history.append({"role": "user", "text": user_val})
                st.session_state.user_data[q['key']] = user_val
                
                with st.spinner("데이터 분석 중..."):
                    time.sleep(0.6)
                confirm_text = q['confirm'].format(value=user_val)
                st.session_state.history.append({"role": "bot", "text": confirm_text, "phase": "시스템 확인"})
                
                st.session_state.step += 1
                st.rerun()
                
        elif q['type'] == 'select':
            cols = st.columns(2) # 2열로 고정
            for idx, opt in enumerate(q['options']):
                with cols[idx % 2]: # 0, 1, 0, 1...
                    if st.button(opt, key=f"btn_{st.session_state.step}_{idx}", use_container_width=True):
                        st.session_state.history.append({"role": "user", "text": opt})
                        st.session_state.user_data[q['key']] = opt
                        
                        with st.spinner("피팅 로직 적용 중..."):
                            time.sleep(0.6)
                        confirm_text = q['confirm'].format(value=opt.split(' ')[0] if ' ' in opt else opt)
                        st.session_state.history.append({"role": "bot", "text": confirm_text, "phase": "시스템 확인"})
                        
                        st.session_state.step += 1
                        st.rerun()
        
        elif q['type'] == 'multiselect': # 다중 선택 처리
            selected_options = st.multiselect(
                "해당하는 모든 항목을 선택해주세요.",
                options=[o.split(' ')[1] if ' ' in o else o for o in q['options']],
                key=f"input_{st.session_state.step}"
            )
            submit_multi = st.button("선택 완료", key=f"submit_multi_{st.session_state.step}")

            if submit_multi and selected_options:
                user_val = ", ".join(selected_options)
                st.session_state.history.append({"role": "user", "text": user_val})
                st.session_state.user_data[q['key']] = user_val
                
                with st.spinner("데이터 분석 중..."):
                    time.sleep(0.6)
                confirm_text = q['confirm'].format(value=user_val)
                st.session_state.history.append({"role": "bot", "text": confirm_text, "phase": "시스템 확인"})
                
                st.session_state.step += 1
                st.rerun()


# 4. 최종 결과 대시보드 (모든 질문 완료 시)
else:
    if 'analyzed' not in st.session_state:
        with st.spinner("고객님만을 위한 맞춤형 리포트 생성 중..."):
            time.sleep(1.5)
        st.session_state.analyzed = True
        st.rerun()

    # 데이터 가공
    ud = st.session_state.user_data
    ub = float(re.findall(r'\d+', ud.get('underbust', '75'))[0])
    
    # 로직 계산 (간단화)
    rec_band = 75
    if ub < 73: rec_band = 70
    elif ub < 78: rec_band = 75
    elif ub < 83: rec_band = 80
    else: rec_band = 85

    # 컵 사이즈 추론 (예시 로직)
    recommended_cup_char = "B" # 기본값
    if "많이 남음" in ud.get('cup_status', ''):
        recommended_cup_char = "A"
    elif "넘침" in ud.get('cup_status', ''):
        recommended_cup_char = "C" # 보정력 필요 시 컵 상향
    
    # IMD 제품 라인업 추천 로직 (예시)
    rec_product_name = "포근핏"
    rec_product_desc = imd_products["포근핏"]["desc"]
    if "군살 많음" in ud.get('flab', ''):
        rec_product_name = "퍼펙트핏"
        rec_product_desc = imd_products["퍼펙트핏"]["desc"]
    elif "처진 가슴" in ud.get('shape', ''):
        rec_product_name = "볼륨업핏"
        rec_product_desc = imd_products["볼륨업핏"]["desc"]
    elif "윗가슴 꺼짐" in ud.get('shape', ''):
        rec_product_name = "볼륨업핏"
        rec_product_desc = imd_products["볼륨업핏"]["desc"]

    # 최종 추천 사이즈
    final_recommended_size = f"{rec_band}{recommended_cup_char}"

    # 결과 출력
    st.markdown("""<div class='final-dashboard'>""", unsafe_allow_html=True)
    
    # 상단: 타이틀 및 KPI
    st.markdown("<h2 style='color: #1a73e8; text-align: center;'>✨ 고객 맞춤 피팅 결과 리포트 ✨</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>측정 밑가슴 둘레</div>
            <div class='kpi-value'>{ub}cm</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>추천 밴드 사이즈</div>
            <div class='kpi-value'>{rec_band}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>IMD AI 정확도</div>
            <div class='kpi-value'>99.2%</div>
        </div>""", unsafe_allow_html=True)
        
    st.divider()
    
    # 중단: 차트와 텍스트 분석 (2단 구성)
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### 📊 IMD AI 체형 정밀 분석")
        fig = create_analysis_chart(ud)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.markdown("### 📝 IMD 피팅 로직 분석")
        st.markdown(f"""
        <div style='background: #f7f7f7; padding: 20px; border-radius: 10px; line-height: 1.8; border: 1px solid #e0e0e0; color: #3c4043;'>
            <span style='color: #888;'>[STEP 1]</span> 실측 <strong>{ub}cm</strong> 확인 → 밴드 사이즈 <strong>{rec_band}</strong>로 조정<br>
            <span style='color: #888;'>[STEP 2]</span> 현재 컵 상태 <strong>'{ud.get('cup_status', '').split(' ')[0]}'</strong> 분석 → 컵 용량 재조정 필요<br>
            <span style='color: #888;'>[STEP 3]</span> 체형 <strong>'{ud.get('flab', '').split(' ')[0]}'</strong> 및 형태 <strong>'{ud.get('shape', '').split(' ')[0]}'</strong> 고려 → 맞춤 패턴 매칭<br>
            <hr style='border-color: #ddd;'>
            <strong style='color: #1a73e8; font-size: 1.2rem;'>💡 최종 IMD AI 추천!</strong><br>
            고객님께 가장 적합한 사이즈는 <strong>{final_recommended_size} (예상)</strong> 이며,<br>
            <strong>[{rec_product_name}]</strong> 라인업을 강력히 추천합니다.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 💖 추천 제품 상세 정보")
    st.markdown(f"""
    <div style='background: #fffbe6; padding: 20px; border-radius: 10px; border: 1px solid #ffe082; color: #3c4043; margin-top: 20px;'>
        <h4 style='color: #f57f17; margin-top: 0;'>[{rec_product_name}]</h4>
        <p>{rec_product_desc}</p>
        <p style='font-weight: bold;'>주요 기능: {', '.join(imd_products[rec_product_name]['features'])}</p>
        <p style='font-weight: bold; color: #e53935;'>가격: {imd_products[rec_product_name]['price']}</p>
    </div>
    """, unsafe_allow_html=True)


    # 하단: CTA
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <button class='final-cta-button' onclick="window.location.href='https://example.com/consult_booking';">
            이 결과로 1:1 전문 상담 예약하기 ➔
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
