import streamlit as st
import re
from typing import Tuple, Optional

# 페이지 설정
st.set_page_config(
    page_title="피터핏 스마트 피팅",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #8B4B8C;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f8f0f8;
        border: 2px solid #8B4B8C;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .size-highlight {
        font-size: 2rem;
        font-weight: bold;
        color: #8B4B8C;
        text-align: center;
    }
    .fitting-message {
        line-height: 1.6;
        font-size: 1.1rem;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 피터핏 사이즈 추천 엔진
def process_data(param1: str, param2: str, param3: str, param4: str, param5: str, param6: str) -> Tuple[str, str]:
    """피터핏 전문 피팅 마스터 시스템"""
    
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
    panty_size = param3.strip() if category == "PANTY" else ""
    
    def parse_bra_band(bra_size: str) -> Optional[int]:
        match = re.match(r"(\d{2,3})", bra_size)
        return int(match.group(1)) if match else None
    
    def parse_bra_cup(bra_size: str) -> Optional[str]:
        match = re.match(r"\d{2,3}\s*([A-Z])", bra_size)
        return match.group(1).upper() if match else None
    
    def get_band_from_underbust(underbust_cm: float) -> int:
        if underbust_cm < 68: return 65
        elif underbust_cm < 73: return 70
        elif underbust_cm < 78: return 75
        elif underbust_cm < 83: return 80
        elif underbust_cm < 88: return 85
        else: return 90
    
    def get_cup_upgrade_steps(body_type_text: str) -> int:
        text = body_type_text.lower()
        if "많" in text: return 2
        elif "없" in text or "보통" in text: return 1
        else: return 1
    
    def upgrade_cup(original_cup: str, steps: int) -> str:
        cups = "ABCDEFGHIJKLMNOP"
        try:
            current_index = cups.index(original_cup.upper())
            new_index = min(current_index + steps, len(cups) - 1)
            return cups[new_index]
        except:
            return original_cup
    
    def recommend_bra_size(underbust: Optional[float], topbust: Optional[float], 
                          current_bra: str, body_type: str) -> str:
        if underbust:
            band = get_band_from_underbust(underbust)
        else:
            band = parse_bra_band(current_bra)
            if not band: return ""
        
        current_cup = parse_bra_cup(current_bra)
        if not current_cup:
            if underbust and topbust:
                diff = topbust - underbust
                if diff < 10: cup = "A"
                elif diff < 12.5: cup = "B"
                elif diff < 15: cup = "C"
                elif diff < 17.5: cup = "D"
                elif diff < 20: cup = "E"
                else: cup = "F"
                return f"{band}{cup}"
            return ""
        
        upgrade_steps = get_cup_upgrade_steps(body_type)
        final_cup = upgrade_cup(current_cup, upgrade_steps)
        return f"{band}{final_cup}"
    
    def recommend_sleep_bra_size(underbust: Optional[float], current_bra: str) -> str:
        if underbust:
            if underbust < 70: base_size = "S"
            elif underbust < 75: base_size = "M"  
            elif underbust < 80: base_size = "L"
            else: base_size = "LL"
        else:
            band = parse_bra_band(current_bra)
            if not band: return ""
            if band <= 70: base_size = "S"
            elif band == 75: base_size = "M"
            elif band == 80: base_size = "L"
            else: base_size = "LL"
        
        current_cup = parse_bra_cup(current_bra)
        if current_cup and current_cup >= "G":
            size_order = ["S", "M", "L", "LL"]
            try:
                current_index = size_order.index(base_size)
                if current_index < len(size_order) - 1:
                    base_size = size_order[current_index + 1]
            except: pass
        return base_size
    
    def recommend_panty_size(hip_circumference: Optional[float], panty_number: str) -> str:
        if hip_circumference:
            if hip_circumference < 87: return "S"
            elif hip_circumference < 92: return "M"
            elif hip_circumference < 97: return "L"
            else: return "LL"
        
        number = panty_number.replace("호", "").strip()
        size_map = {"85": "S", "90": "M", "95": "L", "100": "LL"}
        return size_map.get(number, "")
    
    def get_lineup_info(lineup_name: str) -> dict:
        lineup_data = {
            "루나": {
                "name": "루나 브라",
                "description": "달빛처럼 부드러운 착용감",
                "key_feature": "초경량 소재와 무봉제 설계로 하루 종일 편안한 착용감을 제공하며 자연스러운 볼륨 연출",
                "price": "189,000원"
            },
            "스텔라": {
                "name": "스텔라 브라",
                "description": "별처럼 빛나는 볼륨 솔루션",
                "key_feature": "혁신적인 3D 컨투어 패드와 리프팅 와이어로 극적인 볼륨업과 아름다운 데콜테 라인 연출",
                "price": "225,000원"
            },
            "아우라": {
                "name": "아우라 브라",
                "description": "오라처럼 감싸는 완벽한 핏",
                "key_feature": "360도 서포트 시스템으로 가슴 전체를 안정적으로 감싸며 측면 볼륨까지 완벽하게 정리",
                "price": "199,000원"
            },
            "베라": {
                "name": "베라 브라",
                "description": "진실된 편안함의 정점",
                "key_feature": "메모리폼 쿠션과 스마트 스트레치 원단으로 개인 체형에 완벽하게 맞춤 적응",
                "price": "175,000원"
            },
            "세레나": {
                "name": "세레나 나이트케어",
                "description": "고요한 밤의 수면 케어",
                "key_feature": "수면 중 가슴 형태를 자연스럽게 유지하며 편안한 수면을 위한 특수 설계 나이트브라",
                "price": "129,000원"
            }
        }
        
        for key in lineup_data:
            if key in lineup_name.lower() or lineup_name.lower() in key:
                return lineup_data[key]
        return {"name": lineup_name, "description": "", "key_feature": "", "price": ""}
    
    def generate_fitting_master_message(category: str, recommended_size: str, measurement_data: dict, lineup_info: dict) -> str:
        messages = []
        messages.append("안녕하세요, 고객님! 피터핏 스마트 피팅 마스터입니다.")
        messages.append("")
        
        if category == "BRA":
            messages.append("📊 고객님의 체형 데이터 분석이 완료되었습니다.")
            
            data_summary = []
            if measurement_data.get("underbust"):
                data_summary.append(f"밑가슴 실측: {measurement_data['underbust']:.1f}cm")
            if measurement_data.get("topbust"):
                data_summary.append(f"윗가슴 실측: {measurement_data['topbust']:.1f}cm")
            if measurement_data.get("current_bra"):
                data_summary.append(f"평소 착용: {measurement_data['current_bra']}")
            if measurement_data.get("body_type"):
                data_summary.append(f"체형 특징: {measurement_data['body_type']}")
            
            if data_summary:
                messages.append("• " + " | ".join(data_summary))
                messages.append("")
            
            if recommended_size:
                messages.append(f"🎯 **최종 추천 사이즈: {recommended_size}**")
                messages.append("")
                
                if lineup_info.get("name"):
                    messages.append(f"✨ 추천 제품: **{lineup_info['name']}**")
                    if lineup_info.get("key_feature"):
                        messages.append(f"💎 핵심 기능: {lineup_info['key_feature']}")
                    messages.append("")
                
                messages.append("📋 **추천 근거**")
                messages.append("• 피터핏은 일반 브라보다 우수한 서포트 기능을 제공하므로")
                
                body_type_lower = measurement_data.get("body_type", "").lower()
                if "많" in body_type_lower:
                    messages.append("• 체형 특성상 평소 컵에서 2단계 크게")
                else:
                    messages.append("• 평소 컵에서 1단계 크게 선택하시는 것이 최적입니다")
                
                messages.append("• 고급 소재와 정밀 설계로 완벽한 핏을 제공합니다")
                messages.append("")
                
                messages.append("💡 **착용 가이드**")
                messages.append("• 처음 착용 시 약간의 서포트감이 있으나, 이는 정상적인 피팅 과정입니다")
                messages.append("• 2-3회 착용 후 원단이 체형에 적응하여 더욱 편안해집니다")
                messages.append("• 와이어가 가슴 라인에 정확히 맞고 측면이 깔끔하게 정리되면 완벽한 상태입니다")
                
            else:
                messages.append("❌ 현재 정보로는 정확한 추천이 어렵습니다.")
                messages.append("")
                messages.append("🔍 **필요한 정보**")
                messages.append("• 밑가슴 실측값 (가슴 바로 아래 둘레)")
                messages.append("• 평소 착용하시는 브라 사이즈")
                messages.append("• 체형 특성 정보")
                messages.append("")
                messages.append("정확한 데이터를 입력해주시면 맞춤형 사이즈를 추천해드리겠습니다!")
        
        elif category == "SLEEP_BRA":
            messages.append("🌙 수면 케어를 위한 세레나 나이트케어 분석 결과입니다.")
            messages.append("")
            
            if recommended_size:
                messages.append(f"🎯 **추천 사이즈: {recommended_size}**")
                messages.append("")
                messages.append("✨ **세레나 나이트케어 특징**")
                messages.append("• 수면 중 가슴 형태를 자연스럽게 유지하는 특수 설계")
                messages.append("• 무봉제 소프트 원단으로 수면의 질을 방해하지 않음")
                
                current_cup = parse_bra_cup(measurement_data.get("current_bra", ""))
                if current_cup and current_cup >= "G":
                    messages.append("• 볼륨이 큰 체형을 위해 한 사이즈 크게 추천드립니다")
                
                messages.append("")
                messages.append("💤 **수면 케어 효과**")
                messages.append("• 중력에 의한 가슴 변형 방지")
                messages.append("• 수면 중 자연스러운 가슴 형태 유지")
                messages.append("• 편안한 숙면과 뷰티 케어의 완벽한 조화")
            else:
                messages.append("❌ 나이트케어 추천을 위해 추가 정보가 필요합니다.")
                messages.append("• 밑가슴 실측값 또는 평소 브라 정보를 입력해주세요!")
        
        elif category == "PANTY":
            messages.append("👙 피터핏 팬티 라인 추천 분석 결과입니다.")
            messages.append("")
            
            if recommended_size:
                messages.append(f"🎯 **추천 사이즈: {recommended_size}**")
                messages.append("")
                messages.append("✨ **피터핏 팬티의 특징**")
                messages.append("• 브라와 동일한 고급 소재로 제작된 퍼펙트 세트 라인")
                messages.append("• 하복부와 힙 라인을 우아하게 정리하는 스마트 핏")
                messages.append("• 일반 제품 대비 뛰어난 내구성과 착용감")
                messages.append("")
                messages.append("💡 **사이즈 선택 기준**")
                if measurement_data.get("hip"):
                    messages.append(f"• 힙 실측 {measurement_data['hip']:.1f}cm 기준으로 추천")
                else:
                    messages.append(f"• 평소 팬티 사이즈 기준으로 추천")
                messages.append("• 피터핏만의 정밀한 사이즈 시스템으로 완벽한 핏 보장")
            else:
                messages.append("❌ 팬티 추천을 위해 추가 정보가 필요합니다.")
                messages.append("• 힙 실측값 또는 평소 팬티 사이즈를 입력해주세요!")
        
        else:
            messages.append("❌ 지원하지 않는 제품 카테고리입니다.")
            messages.append("브라, 나이트케어, 팬티 중에서 선택해주세요.")
        
        messages.append("")
        messages.append("💬 궁금한 점이 있으시면 언제든 문의해주세요!")
        messages.append("고객님의 완벽한 핏을 위해 피터핏 스마트 피팅이 함께 합니다. ✨")
        
        return "\n".join(messages)
    
    # 메인 로직
    recommended_size = ""
    measurement_data = {
        "underbust": measurement1 if category in ["BRA", "SLEEP_BRA"] else None,
        "topbust": measurement2,
        "hip": measurement1 if category == "PANTY" else None,
        "current_bra": existing_bra,
        "body_type": body_type,
        "panty_size": panty_size
    }
    
    lineup_info = get_lineup_info(lineup) if lineup else {}
    
    if category == "BRA":
        recommended_size = recommend_bra_size(measurement1, measurement2, existing_bra, body_type)
    elif category == "SLEEP_BRA":
        recommended_size = recommend_sleep_bra_size(measurement1, existing_bra)
    elif category == "PANTY":
        recommended_size = recommend_panty_size(measurement1, panty_size)
    
    result_message = generate_fitting_master_message(category, recommended_size, measurement_data, lineup_info)
    result_data = recommended_size
    
    return result_message, result_data


# Streamlit 앱 시작
def main():
    # 헤더
    st.markdown('<div class="main-header">✨ 피터핏 스마트 피팅</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI 기술과 빅데이터로 고객님만의 완벽한 사이즈를 찾아드립니다</div>', unsafe_allow_html=True)
    
    # 메인 레이아웃
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🔍 스마트 피팅 정보 입력")
        
        # 제품 카테고리 선택
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        category = st.selectbox(
            "제품 카테고리",
            ["브라", "나이트케어(세레나)", "팬티"],
            help="추천받고 싶은 제품 종류를 선택하세요"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 카테고리별 입력 필드
        if category == "브라":
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("**📏 실측 정보**")
            underbust = st.number_input("밑가슴 둘레 (cm)", min_value=60, max_value=110, value=75, step=1)
            topbust = st.number_input("윗가슴 둘레 (cm)", min_value=70, max_value=130, value=90, step=1)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("**👗 현재 착용 정보**")
            current_bra = st.text_input("평소 브라 사이즈", value="75B", placeholder="예: 75B, 80C")
            body_type = st.selectbox("체형 특성", ["군살없음", "군살보통", "군살많음"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("**✨ 제품 라인**")
            lineup = st.selectbox("희망 라인", ["루나", "스텔라", "아우라", "베라"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 파라미터 매핑
            param1, param2, param3, param4, param5, param6 = "BRA", str(underbust), str(topbust), current_bra, body_type, lineup
        
        elif category == "나이트케어(세레나)":
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("**📏 실측 정보**")
            underbust = st.number_input("밑가슴 둘레 (cm)", min_value=60, max_value=110, value=75, step=1, help="모르시면 0으로 입력하세요")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("**👗 현재 착용 정보**")
            current_bra = st.text_input("평소 브라 사이즈", value="75B", placeholder="예: 75B, 80C")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 파라미터 매핑
            param1, param2, param3, param4, param5, param6 = "SLEEP_BRA", str(underbust), "", current_bra, "", "세레나"
        
        else:  # 팬티
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("**📏 실측 정보**")
            hip = st.number_input("힙 둘레 (cm)", min_value=70, max_value=120, value=90, step=1)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("**👗 현재 착용 정보**")
            panty_size = st.selectbox("평소 팬티 호수", ["85", "90", "95", "100"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 파라미터 매핑
            param1, param2, param3, param4, param5, param6 = "PANTY", str(hip), panty_size, "", "", ""
        
        # 분석 버튼
        analyze_button = st.button("✨ 스마트 피팅 분석 시작", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 📊 피팅 분석 결과")
        
        if analyze_button:
            with st.spinner("피터핏 AI가 분석 중입니다..."):
                # 사이즈 추천 실행
                result_message, recommended_size = process_data(param1, param2, param3, param4, param5, param6)
                
                # 결과 표시
                if recommended_size:
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(f'<div class="size-highlight">추천 사이즈: {recommended_size}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="fitting-message">', unsafe_allow_html=True)
                st.markdown(result_message)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 추가 정보
                st.markdown("---")
                st.info("💡 **비즈니스 데모 시스템**\n\n이 시스템은 피터핏의 혁신적인 AI 피팅 기술을 시연하기 위한 데모용 애플리케이션입니다. 실제 서비스 런칭 시 더욱 정교한 개인화 추천과 고급 기능이 추가될 예정입니다.")
        
        else:
            st.info("👈 왼쪽에서 피팅 정보를 입력하고 '스마트 피팅 분석 시작' 버튼을 클릭하세요!")
            
            # 샘플 결과 미리보기
            st.markdown("### 🎬 결과 미리보기")
            st.markdown("""
            **입력 예시**: 브라, 밑가슴 74cm, 윗가슴 89cm, 평소 75B, 군살보통, 루나
            
            **예상 결과**:
            """)
            
            sample_message = """
안녕하세요, 고객님! 피터핏 스마트 피팅 마스터입니다.

📊 고객님의 체형 데이터 분석이 완료되었습니다.
• 밑가슴 실측: 74.0cm | 윗가슴 실측: 89.0cm | 평소 착용: 75B | 체형 특징: 군살보통

🎯 **최종 추천 사이즈: 75C**

✨ 추천 제품: **루나 브라**
💎 핵심 기능: 초경량 소재와 무봉제 설계로 하루 종일 편안한 착용감을 제공하며 자연스러운 볼륨 연출

📋 **추천 근거**
• 피터핏은 일반 브라보다 우수한 서포트 기능을 제공하므로
• 평소 컵에서 1단계 크게 선택하시는 것이 최적입니다
• 고급 소재와 정밀 설계로 완벽한 핏을 제공합니다

💬 궁금한 점이 있으시면 언제든 문의해주세요!
고객님의 완벽한 핏을 위해 피터핏 스마트 피팅이 함께 합니다. ✨
            """
            
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown('<div class="size-highlight">추천 사이즈: 75C</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="fitting-message">', unsafe_allow_html=True)
            st.markdown(sample_message)
            st.markdown('</div>', unsafe_allow_html=True)

    # 사이드바 정보
    with st.sidebar:
        st.markdown("### 📞 고객지원")
        st.markdown("""
        **피터핏 고객센터**
        - 전화: 1588-1234
        - 운영시간: 평일 9:00-18:00
        - 이메일: support@peterfit.co.kr
        """)
        
        st.markdown("### 📏 정확한 측정 가이드")
        st.markdown("""
        **측정 방법**
        1. 밑가슴: 가슴 바로 아래 수평으로 측정
        2. 윗가슴: 가슴의 가장 높은 부분 측정
        3. 힙: 엉덩이의 가장 넓은 부분 측정
        
        **측정 팁**
        - 속옷 미착용 상태에서 측정
        - 줄자를 너무 조이지 않고 자연스럽게
        - 정면을 보고 편안히 선 자세에서 측정
        """)
        
        st.markdown("### ✨ 피터핏 브랜드 소개")
        st.markdown("""
        **피터핏의 혁신**
        - AI 기반 스마트 피팅 기술
        - 프리미엄 소재와 정밀 설계
        - 개인 맞춤형 사이즈 추천
        - 지속가능한 뷰티 케어
        """)

if __name__ == "__main__":
    main()
