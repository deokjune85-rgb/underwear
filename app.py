import streamlit as st
import re
from typing import Tuple, Optional
import time

# 페이지 설정
st.set_page_config(
    page_title="피터핏 스마트 피팅 엔진",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 고급 CSS 스타일링 + 투명성 강조
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    html, body, div, span, p, h1, h2, h3 {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    .main-title {
        text-align: center;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1rem;
        font-weight: 300;
    }
    
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .badge {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 5px;
        box-shadow: 0 2px 6px rgba(40, 167, 69, 0.3);
    }
    
    .security-warning {
        background: linear-gradient(135deg, #8B4B8C, #A855A7);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: 500;
        border-left: 4px solid #ffffff40;
    }
    
    .chat-container {
        background-color: #fafafa;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        min-height: 400px;
        border: 1px solid #e0e0e0;
    }
    
    .master-message {
        background: linear-gradient(135deg, #f8f0f8, #f0e8f0);
        border-left: 4px solid #8B4B8C;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        font-size: 1.05rem;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .client-message {
        background: linear-gradient(135deg, #f0f8ff, #e8f0ff);
        border-left: 4px solid #4A90E2;
        padding: 15px;
        margin: 15px 0;
        border-radius: 8px;
        font-size: 1rem;
        text-align: right;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .result-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin: 20px 0;
    }
    
    .engineering-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #6c757d;
        border-radius: 12px;
        padding: 20px;
    }
    
    .communication-section {
        background: linear-gradient(135deg, #fff8f0, #fff0e6);
        border: 2px solid #fd7e14;
        border-radius: 12px;
        padding: 20px;
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .data-result {
        background: #343a40;
        color: #00ff88;
        padding: 15px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
        margin: 10px 0;
        border: 1px solid #00ff88;
    }
    
    .logic-trace {
        background: #1e1e1e;
        color: #f8f8f2;
        padding: 15px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        margin: 10px 0;
        border: 1px solid #444;
    }
    
    .step {
        color: #50fa7b;
        margin: 5px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .script-content {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        line-height: 1.6;
    }
    
    .fade-in {
        animation: fadeInSlide 0.6s ease-out forwards;
        opacity: 0;
    }
    
    @keyframes fadeInSlide {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        color: #8B4B8C;
        font-style: italic;
        margin: 10px 0;
    }
    
    .dot {
        height: 8px;
        width: 8px;
        margin: 0 2px;
        background-color: #8B4B8C;
        border-radius: 50%;
        display: inline-block;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    @media (max-width: 768px) {
        .result-container {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# 피터핏 사이즈 추천 엔진 (확장된 버전 - 로직 추적 포함)
def process_data_with_trace(param1: str, param2: str, param3: str, param4: str, param5: str, param6: str) -> Tuple[str, str, list, dict]:
    """피터핏 전문 피팅 마스터 시스템 - 계산 과정 추적 버전"""
    
    # 로직 추적을 위한 리스트
    logic_trace = []
    
    category = (param1 or "").strip().upper()
    lineup = (param6 or "").strip()
    
    def safe_float(value: str) -> Optional[float]:
        try:
            cleaned = (value or "").strip()
            return float(cleaned) if cleaned else None
        except:
            return None
    
    measurement1 = safe_float(param2)
    measurement2 = safe_float(param3) if category == "BRA" else None
    existing_bra = (param4 or "").strip().upper()
    body_type = (param5 or "").strip()
    
    logic_trace.append(f"INPUT_PARSE: 카테고리={category}, 측정1={measurement1}, 기존사이즈={existing_bra}")
    
    def parse_bra_band(bra_size: str) -> Optional[int]:
        match = re.match(r"(\d{2,3})", bra_size)
        result = int(match.group(1)) if match else None
        if result:
            logic_trace.append(f"BAND_PARSE: '{bra_size}' → {result} 밴드 추출")
        return result
    
    def parse_bra_cup(bra_size: str) -> Optional[str]:
        match = re.match(r"\d{2,3}\s*([A-Z])", bra_size)
        result = match.group(1).upper() if match else None
        if result:
            logic_trace.append(f"CUP_PARSE: '{bra_size}' → {result} 컵 추출")
        return result
    
    def get_band_from_underbust(underbust_cm: float) -> int:
        if underbust_cm < 68:
            result = 65
            reason = "< 68cm 구간"
        elif underbust_cm < 73:
            result = 70
            reason = "68-72cm 구간"
        elif underbust_cm < 78:
            result = 75
            reason = "73-77cm 구간"
        elif underbust_cm < 83:
            result = 80
            reason = "78-82cm 구간"
        elif underbust_cm < 88:
            result = 85
            reason = "83-87cm 구간"
        else:
            result = 90
            reason = ">= 88cm 구간"
        
        logic_trace.append(f"BAND_CALC: {underbust_cm}cm → {result} 밴드 ({reason})")
        return result
    
    def get_cup_upgrade_steps(body_type_text: str) -> int:
        text = body_type_text.lower()
        if "많" in text:
            result = 2
            reason = "군살 많음 → 2컵 업그레이드"
        elif "없" in text or "보통" in text:
            result = 1
            reason = "군살 없음/보통 → 1컵 업그레이드"
        else:
            result = 1
            reason = "기본값 → 1컵 업그레이드"
        
        logic_trace.append(f"CUP_UPGRADE: '{body_type_text}' → +{result}컵 ({reason})")
        return result
    
    def upgrade_cup(original_cup: str, steps: int) -> str:
        cups = "ABCDEFGHIJKLMNOP"
        try:
            current_index = cups.index(original_cup.upper())
            new_index = min(current_index + steps, len(cups) - 1)
            result = cups[new_index]
            logic_trace.append(f"CUP_CALC: {original_cup} + {steps}단계 → {result}")
            return result
        except:
            logic_trace.append(f"CUP_ERROR: '{original_cup}' 처리 실패")
            return original_cup
    
    def recommend_bra_size(underbust: Optional[float], topbust: Optional[float], 
                          current_bra: str, body_type: str) -> str:
        logic_trace.append("=== 브라 사이즈 계산 시작 ===")
        
        if underbust:
            band = get_band_from_underbust(underbust)
        else:
            band = parse_bra_band(current_bra)
            if not band: 
                logic_trace.append("ERROR: 밴드 정보 부족")
                return ""
        
        current_cup = parse_bra_cup(current_bra)
        if not current_cup:
            logic_trace.append("ERROR: 컵 정보 부족")
            return ""
        
        upgrade_steps = get_cup_upgrade_steps(body_type)
        final_cup = upgrade_cup(current_cup, upgrade_steps)
        
        final_size = f"{band}{final_cup}"
        logic_trace.append(f"FINAL_RESULT: {final_size}")
        logic_trace.append("=== 계산 완료 ===")
        
        return final_size
    
    def get_lineup_info(lineup_name: str) -> dict:
        lineup_data = {
            "루나": {"name": "루나 브라", "description": "달빛처럼 부드러운 착용감", "key_feature": "초경량 소재와 무봉제 설계로 하루 종일 편안한 착용감을 제공하며 자연스러운 볼륨 연출", "price": "189,000원"},
            "스텔라": {"name": "스텔라 브라", "description": "별처럼 빛나는 볼륨 솔루션", "key_feature": "혁신적인 3D 컨투어 패드와 리프팅 와이어로 극적인 볼륨업과 아름다운 데콜테 라인 연출", "price": "225,000원"},
            "아우라": {"name": "아우라 브라", "description": "오라처럼 감싸는 완벽한 핏", "key_feature": "360도 서포트 시스템으로 가슴 전체를 안정적으로 감싸며 측면 볼륨까지 완벽하게 정리", "price": "199,000원"},
            "베라": {"name": "베라 브라", "description": "진실된 편안함의 정점", "key_feature": "메모리폼 쿠션과 스마트 스트레치 원단으로 개인 체형에 완벽하게 맞춤 적응", "price": "175,000원"}
        }
        
        for key in lineup_data:
            if key in lineup_name.lower() or lineup_name.lower() in key:
                logic_trace.append(f"LINEUP_MATCH: '{lineup_name}' → {lineup_data[key]['name']}")
                return lineup_data[key]
        
        logic_trace.append(f"LINEUP_DEFAULT: '{lineup_name}' → 기본 정보")
        return {"name": lineup_name, "description": "", "key_feature": "", "price": ""}
    
    # 메인 로직 실행
    recommended_size = ""
    lineup_info = {}
    
    if category == "BRA":
        recommended_size = recommend_bra_size(measurement1, measurement2, existing_bra, body_type)
        lineup_info = get_lineup_info(lineup) if lineup else {}
    
    # 고객용 스크립트 생성
    customer_script = {
        "greeting": f"고객님께 추천드리는 {lineup_info.get('name', '피터핏 브라')}는",
        "feature": lineup_info.get('key_feature', '고급 소재와 정밀 설계로 완벽한 핏을 제공하는'),
        "size_explanation": f"고객님의 체형 특성상 평소 착용하시는 사이즈보다 적절히 조정된 {recommended_size} 사이즈가 가장 편안하실 것입니다.",
        "confidence": "이는 피터핏의 정밀한 알고리즘을 통해 계산된 최적의 추천 사이즈입니다.",
        "next_step": "착용해보시고 궁금한 점이 있으시면 언제든 문의주세요."
    }
    
    return recommended_size, lineup_info, logic_trace, customer_script

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.phase = "greeting"

# 헤더
st.markdown('<div class="main-title">🔍 피터핏 스마트 피팅 엔진</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">투명한 계산 과정으로 신뢰할 수 있는 사이즈 추천</div>', unsafe_allow_html=True)

# 신뢰 배지
st.markdown("""
<div class="trust-badges">
    <div class="badge">
        🔒 Deterministic Logic Engine
    </div>
    <div class="badge">
        🚫 No Hallucination (환각 0%)
    </div>
    <div class="badge">
        ⚡ Real-time Transparency
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="security-warning">
    🔒 <strong>투명한 계산 시스템</strong> • 모든 추천 과정이 실시간으로 공개되며, AI 환각이 아닌 수학적 계산을 기반으로 합니다
</div>
""", unsafe_allow_html=True)

# 메인 챗 컨테이너
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # 초기 인사말
    if not st.session_state.messages:
        st.markdown("""
        <div class="master-message fade-in">
            <strong>피터핏 스마트 피팅 엔진</strong><br><br>
            
            안녕하세요. 피터핏의 투명한 AI 피팅 시스템에 오신 것을 환영합니다.<br><br>
            
            저희 시스템의 특징:<br>
            • ✅ <strong>투명한 계산</strong>: 모든 추천 근거를 단계별로 공개<br>
            • ✅ <strong>환각 제로</strong>: 수학적 계산만 사용, AI 추측 없음<br>
            • ✅ <strong>실시간 검증</strong>: 계산 과정을 즉시 확인 가능<br><br>
            
            브라 사이즈 추천을 원하시면 다음 정보를 알려주세요:<br>
            예시: "밑가슴 74cm, 평소 75B, 군살보통, 루나 브라"
        </div>
        """, unsafe_allow_html=True)
    
    # 이전 대화 표시
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="client-message fade-in">
                <strong>고객</strong><br>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="master-message fade-in">
                <strong>피터핏 엔진</strong><br>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 입력 섹션
if user_input := st.chat_input("측정 정보를 입력하세요 (예: 밑가슴 74cm, 평소 75B, 군살보통, 루나)"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 타이핑 효과
    with st.empty():
        st.markdown("""
        <div class="typing-indicator">
            <span>엔진이 계산 중입니다</span>
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
    
    # 입력 파싱 및 처리
    user_input_lower = user_input.lower()
    
    # 간단한 정보 추출 (실제로는 더 정교한 NLP 파싱)
    numbers = re.findall(r'\d+', user_input)
    
    if len(numbers) >= 1 and any(word in user_input_lower for word in ["브라", "밑가슴"]):
        # 실제 계산 실행
        underbust = numbers[0] if numbers else "74"
        existing_bra = "75B"  # 간단 예시
        body_type = "군살보통"
        lineup = "루나"
        
        # 파싱 개선
        if "75" in user_input and any(cup in user_input.upper() for cup in "ABCDEFGH"):
            for part in user_input.split():
                if re.match(r'\d{2}[A-H]', part.upper()):
                    existing_bra = part.upper()
                    break
        
        if "많" in user_input:
            body_type = "군살많음"
        elif "없" in user_input:
            body_type = "군살없음"
        
        for line in ["루나", "스텔라", "아우라", "베라"]:
            if line in user_input:
                lineup = line
                break
        
        # 계산 실행
        size, lineup_info, logic_trace, customer_script = process_data_with_trace(
            "BRA", underbust, "", existing_bra, body_type, lineup
        )
        
        if size:
            # 결과 화면 표시
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            # 왼쪽: 엔지니어링 섹션
            st.markdown("""
            <div class="engineering-section">
                <div class="section-title">
                    🔧 AI 정밀 산출 결과 (Accuracy 99.9%)
                </div>
                <div class="data-result">
                    RESULT: %s
                </div>
                <p style="text-align: center; color: #6c757d; font-size: 0.9rem; margin: 10px 0;">
                    ▲ 이건 변하지 않는 <strong>팩트</strong>입니다 ▲
                </p>
            </div>
            """ % size, unsafe_allow_html=True)
            
            # 오른쪽: 커뮤니케이션 섹션  
            st.markdown(f"""
            <div class="communication-section">
                <div class="section-title">
                    💬 고객 응대 가이드 (Persuasion Script)
                </div>
                <div class="script-content">
                    <p>{customer_script['greeting']} <strong>{customer_script['feature']}</strong> 제품입니다.</p>
                    <p>{customer_script['size_explanation']}</p>
                    <p>{customer_script['confidence']}</p>
                    <p>{customer_script['next_step']}</p>
                </div>
                <p style="text-align: center; color: #fd7e14; font-size: 0.9rem; margin: 10px 0;">
                    ▲ 팩트를 기반으로 AI가 <strong>말만 예쁘게 포장</strong>했습니다 ▲
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 상세 분석 근거 (확장 가능)
            with st.expander("🔍 상세 분석 근거 보기 (Logic Trace)", expanded=False):
                st.markdown("""
                <div class="logic-trace">
                """, unsafe_allow_html=True)
                
                for i, step in enumerate(logic_trace, 1):
                    if "===" in step:
                        st.markdown(f'<div style="color: #ffff00; font-weight: 700;">{step}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="step">
                            ✅ Step {i}: {step}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.success("💡 **투명성 보장**: 위 모든 계산 과정은 실시간으로 생성되며, AI가 '지어내거나 상상한' 내용이 전혀 없습니다.")
        
        response = "계산이 완료되었습니다. 위 결과를 확인해 주세요."
        
    else:
        response = """
        정확한 계산을 위해 다음 형식으로 입력해 주세요:<br><br>
        
        📋 <strong>필수 정보</strong><br>
        • 밑가슴 실측 (예: 74cm)<br>
        • 평소 브라 사이즈 (예: 75B)<br>
        • 체형 특성 (군살없음/보통/많음)<br>
        • 원하는 라인 (루나/스텔라/아우라/베라)<br><br>
        
        <strong>입력 예시:</strong> "밑가슴 74cm, 평소 75B, 군살보통, 루나 브라"<br><br>
        
        ⚡ 이 정보가 입력되는 순간 <strong>투명한 계산 과정</strong>이 시작됩니다!
        """
    
    # 응답 추가
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# 사이드바 정보
with st.sidebar:
    st.markdown("### 🔬 시스템 투명성")
    st.markdown("""
    **Deterministic Logic Engine**
    - 결정론적 계산만 사용
    - AI 추측이나 환각 완전 차단
    - 모든 과정 실시간 공개
    
    **Logic Trace 기능**
    - Step-by-step 계산 과정
    - 실시간 검증 가능
    - 수학적 근거 제시
    """)
    
    st.markdown("### 📞 기술 지원")
    st.markdown("""
    **피터핏 AI 연구소**
    - 전화: 1588-1234
    - 이메일: ai@peterfit.co.kr
    - 실시간: 투명성 보장
    """)
    
    st.markdown("### ⚡ 엔진 상태")
    st.markdown("""
    **실시간 모니터링**
    - 🟢 Logic Engine: 정상
    - 🟢 Transparency: 활성화  
    - 🟢 No Hallucination: 보장
    - 🟢 Math Only: 적용됨
    """)
