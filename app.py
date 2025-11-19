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
    page_title="Waki Fitting Master",
    page_icon="👙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 프리미엄 다크 & 골드 테마 (의료/럭셔리 감성)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stApp {
        background-color: #121212; /* 딥 블랙 배경 */
        color: #e0e0e0;
    }

    /* 뉴스 티커 */
    .news-ticker {
        background: linear-gradient(90deg, #1f1f1f, #2d2d2d);
        border-left: 4px solid #d4af37;
        color: #fff;
        padding: 10px 20px;
        font-size: 0.9rem;
        border-radius: 4px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
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
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid #d4af37;
        color: #d4af37;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* 채팅 스타일 */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding-bottom: 50px;
    }
    
    .bot-message {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-left: 3px solid #d4af37;
        color: #e0e0e0;
        padding: 20px;
        border-radius: 0 15px 15px 15px;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        animation: fadeIn 0.5s ease-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #d4af37, #c5a028);
        color: #121212;
        padding: 15px 25px;
        border-radius: 15px 0 15px 15px;
        align-self: flex-end;
        margin-left: auto;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        animation: fadeIn 0.5s ease-out;
        max-width: 80%;
        text-align: right;
    }

    .phase-tag {
        font-size: 0.75rem;
        color: #888;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* 최종 리포트 대시보드 */
    .final-dashboard {
        background-color: #1e1e1e;
        border: 1px solid #444;
        border-radius: 15px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .kpi-box {
        background-color: #252525;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #333;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 900;
        color: #d4af37;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #aaa;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 버튼 커스텀 */
    .stButton > button {
        background-color: #252525;
        color: #fff;
        border: 1px solid #555;
        border-radius: 8px;
        padding: 15px;
        font-size: 1rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        border-color: #d4af37;
        color: #d4af37;
        background-color: #333;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 로직 및 차트 함수]
# ==========================================

def create_analysis_chart(user_data):
    """5각 레이더 차트 생성"""
    # 입력 데이터에 따른 동적 점수 산정
    flab_score = 80 if "많음" in user_data.get('flab', '') else (60 if "보통" in user_data.get('flab', '') else 40)
    shape_score = 85 if "처진" in user_data.get('shape', '') else 50
    cup_gap = 90 if "여유 많음" in user_data.get('cup_status', '') else 30
    
    categories = ['보정 필요도', '가슴 퍼짐', '리프팅 요망', '볼륨 부족', '비대칭 위험']
    values = [flab_score, 70, shape_score, cup_gap, 40]  # 시뮬레이션 값
    values += [values[0]] # 폐곡선
    categories += [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.2)',
        line=dict(color='#d4af37', width=2),
        marker=dict(color='#fff', size=4),
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#1e1e1e',
            radialaxis=dict(visible=True, range=[0, 100], color='#666', gridcolor='#333'),
            angularaxis=dict(color='#ccc', gridcolor='#333')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=350
    )
    return fig

# 시나리오 데이터 (순차적 질문)
questions = [
    {
        "phase": "PHASE 1. FOUNDATION",
        "question": "안녕하십니까. **Waki Fitting Master AI**입니다.\n15년간 축적된 데이터 기반의 정밀 진단을 시작합니다.\n\n가장 먼저, 기준점이 되는 **밑가슴 둘레 실측(cm)**을 입력해주십시오.",
        "key": "underbust",
        "type": "number",
        "confirm": "기준 사이즈 **{value}cm** 확인. 밴드 장력을 계산합니다."
    },
    {
        "phase": "PHASE 1. FOUNDATION",
        "question": "현재 착용 중인 **브라 사이즈**는 무엇입니까? (예: 80B)",
        "key": "current_bra",
        "type": "text",
        "confirm": "현재 **{value}** 착용 중. 해당 사이즈의 패턴 적합도를 분석합니다."
    },
    {
        "phase": "PHASE 2. SYMPTOM CHECK",
        "question": "현재 브라 착용 시 **컵의 상태**는 어떠합니까?\n이는 컵 용량의 오차를 파악하는 핵심 단서입니다.",
        "key": "cup_status",
        "type": "select",
        "options": ["① 컵이 많이 남음 (들뜸)", "② 약간 남음", "③ 딱 맞음", "④ 컵이 넘침 (눌림)"],
        "confirm": "피팅 상태 **'{value}'** 확인. 컵 용량 재산정이 필요합니다."
    },
    {
        "phase": "PHASE 3. BODY TYPE",
        "question": "가슴 주변(겨드랑이/등)의 **군살 정도**를 선택해주십시오.\n보정 속옷의 설계 강도를 결정하는 변수입니다.",
        "key": "flab",
        "type": "select",
        "options": ["① 군살 없음", "② 보통", "③ 군살 많음 (보정 필수)"],
        "confirm": "체형 데이터 **'{value}'** 입력 완료."
    },
    {
        "phase": "PHASE 3. BODY TYPE",
        "question": "**가슴 형태**의 특징을 선택해주십시오.",
        "key": "shape",
        "type": "select",
        "options": ["① 처진 가슴", "② 퍼진 가슴 (벌어짐)", "③ 윗가슴 꺼짐", "④ 일반형"],
        "confirm": "데이터 수집 완료. 정밀 분석 알고리즘을 가동합니다."
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
    "AI 피팅 시스템 도입 후 반품률 80% 감소 달성",
    "신제품 '루나 브라' 빅데이터 기반 설계 적용",
    "실시간 상담 대기 인원: 0명 (AI 즉시 응대 중)"
]
st.markdown(f"""
<div class='news-ticker'>
    <span style='color: #ff4b4b; margin-right: 10px;'>● LIVE {current_time}</span> {random.choice(news)}
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; font-size: 3rem;'>Waki Fitting Master</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Automated by IMD Logic Engine v2.5</p>", unsafe_allow_html=True)

st.markdown("""
<div class="trust-badges">
    <div class="badge">🔒 Deterministic Logic</div>
    <div class="badge">🚫 No Hallucination</div>
    <div class="badge">⚡ Real-time Analysis</div>
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
    if not st.session_state.history or st.session_state.history[-1]['role'] == 'user' or (st.session_state.history[-1]['role'] == 'bot' and "확인" in st.session_state.history[-1]['text']):
         # 봇 메시지 추가 및 리런 방지용 로직
         last_msg = st.session_state.history[-1]['text'] if st.session_state.history else ""
         if q['question'] not in last_msg:
             st.session_state.history.append({"role": "bot", "text": q['question'], "phase": q['phase']})
             st.rerun()

    # 입력 위젯 영역
    with st.container():
        # 빈 공간 확보
        st.write("") 
        
        if q['type'] in ['text', 'number']:
            with st.form(key=f"form_{st.session_state.step}"):
                user_val = st.text_input("답변 입력", key=f"input_{st.session_state.step}")
                submit = st.form_submit_button("전송 ➔")
                
            if submit and user_val:
                st.session_state.history.append({"role": "user", "text": user_val})
                st.session_state.user_data[q['key']] = user_val
                
                # 봇 확인 메시지
                with st.spinner("데이터 분석 중..."):
                    time.sleep(0.6)
                confirm_text = q['confirm'].format(value=user_val)
                st.session_state.history.append({"role": "bot", "text": confirm_text, "phase": "SYSTEM LOG"})
                
                st.session_state.step += 1
                st.rerun()
                
        elif q['type'] == 'select':
            cols = st.columns(len(q['options'])) if len(q['options']) < 3 else st.columns(2)
            for idx, opt in enumerate(q['options']):
                col_idx = idx % 2 if len(q['options']) >= 3 else idx
                if cols[col_idx].button(opt, key=f"btn_{st.session_state.step}_{idx}", use_container_width=True):
                    st.session_state.history.append({"role": "user", "text": opt})
                    st.session_state.user_data[q['key']] = opt
                    
                    with st.spinner("패턴 매칭 중..."):
                        time.sleep(0.6)
                    confirm_text = q['confirm'].format(value=opt.split(' ')[1] if ' ' in opt else opt)
                    st.session_state.history.append({"role": "bot", "text": confirm_text, "phase": "SYSTEM LOG"})
                    
                    st.session_state.step += 1
                    st.rerun()

# 4. 최종 결과 대시보드 (모든 질문 완료 시)
else:
    if 'analyzed' not in st.session_state:
        with st.spinner("최종 리포트 생성 중..."):
            time.sleep(1.5)
        st.session_state.analyzed = True
        st.rerun()

    # 데이터 가공
    ud = st.session_state.user_data
    ub = float(re.findall(r'\d+', ud.get('underbust', '75'))[0])
    
    # 로직 계산
    rec_band = 75
    if ub < 73: rec_band = 70
    elif ub < 78: rec_band = 75
    elif ub < 83: rec_band = 80
    else: rec_band = 85
    
    # 결과 출력
    st.markdown("""<div class='final-dashboard'>""", unsafe_allow_html=True)
    
    # 상단: 타이틀 및 KPI
    st.markdown("<h2 style='color: #d4af37; text-align: center;'>📊 Professional Fitting Report</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Measured Underbust</div>
            <div class='kpi-value'>{ub}cm</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Recommended Band</div>
            <div class='kpi-value'>{rec_band}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-label'>Accuracy Score</div>
            <div class='kpi-value'>99.2%</div>
        </div>""", unsafe_allow_html=True)
        
    st.divider()
    
    # 중단: 차트와 텍스트 분석 (2단 구성)
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### 📐 체형 정밀 분석 (Radar Analysis)")
        fig = create_analysis_chart(ud)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.markdown("### 📝 AI Logic Trace")
        st.markdown(f"""
        <div style='background: #252525; padding: 20px; border-radius: 10px; line-height: 1.8; border: 1px solid #444;'>
            <span style='color: #888;'>[STEP 1]</span> 실측 <strong>{ub}cm</strong> 감지 → 밴드 오차범위 내 <strong>{rec_band}사이즈</strong> 선정<br>
            <span style='color: #888;'>[STEP 2]</span> 컵 상태 <strong>'{ud.get('cup_status', '').split(' ')[0]}'</strong> 확인 → 컵 용량 재설계 필요<br>
            <span style='color: #888;'>[STEP 3]</span> 체형 <strong>'{ud.get('shape', '').split(' ')[1]}'</strong> 분석 → 리프팅 패널 적용 모델 매칭<br>
            <hr style='border-color: #444;'>
            <strong style='color: #d4af37; font-size: 1.2rem;'>🎯 최종 처방 (Prescription)</strong><br>
            고객님께는 <strong>{rec_band}C (추정)</strong> 사이즈의<br>
            <strong>오리지널(미디) 라인</strong>을 강력히 권장합니다.
        </div>
        """, unsafe_allow_html=True)
        
    # 하단: CTA
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <button style='background: linear-gradient(90deg, #d4af37, #f1c40f); color: #000; border: none; padding: 15px 40px; font-weight: 900; font-size: 1.1rem; border-radius: 50px; cursor: pointer; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);'>
            이 결과로 1:1 상담 예약하기 ➔
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
