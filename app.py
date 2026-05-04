import streamlit as st
import random
import time
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="Anatomy Quiz Pro", page_icon="💀", layout="centered")

# 2. 뼈 데이터 (이미지 대비 위치 %로 설정: top, left 순서)
# 이 숫자를 조금씩 고치면 점의 위치가 이동합니다!
bone_data = {
    "Skull (Cranium)": {"pos": (8, 50), "options": ["Skull", "Mandible", "Cervical", "Clavicle"]},
    "Mandible": {"pos": (13, 50), "options": ["Mandible", "Maxilla", "Hyoid", "Skull"]},
    "Clavicle": {"pos": (18, 40), "options": ["Clavicle", "Scapula", "Sternum", "Humerus"]},
    "Sternum": {"pos": (28, 50), "options": ["Sternum", "Ribs", "Clavicle", "Xiphoid"]},
    "Humerus": {"pos": (35, 30), "options": ["Humerus", "Radius", "Ulna", "Femur"]},
    "Pelvis": {"pos": (50, 50), "options": ["Pelvis", "Femur", "Sacrum", "Ilium"]},
    "Femur": {"pos": (65, 42), "options": ["Femur", "Tibia", "Fibula", "Patella"]},
    "Patella": {"pos": (75, 42), "options": ["Patella", "Femur", "Tibia", "Fibula"]},
    "Tibia": {"pos": (85, 40), "options": ["Tibia", "Fibula", "Tarsals", "Femur"]}
}

if 'score' not in st.session_state: st.session_state.score = 0
if 'quiz_count' not in st.session_state: st.session_state.quiz_count = 0
if 'current_bone' not in st.session_state: st.session_state.current_bone = random.choice(list(bone_data.keys()))

st.title("💀 AI Anatomy Quiz")

# 3. 시각화 영역 (이미지 크기 조절 및 점 위치 고정)
try:
    # 깃허브 아이디를 입력하지 않아도 되는 가장 안정적인 방식
    st.markdown(f"""
        <div style="position: relative; width: 100%; max-width: 400px; margin: auto; border: 2px solid #4a90e2; border-radius: 10px; overflow: hidden;">
            <!-- 이미지 높이를 500px로 제한하여 객관식 버튼이 보이게 함 -->
            <img src="https://raw.githubusercontent.com/{st.session_state.get('user_id', '본인아이디')}/bone-quiz/main/skeleton.jpg" 
                 style="width: 100%; height: 500px; object-fit: contain; background-color: white;">
            <!-- 빨간 점 (위치 % 방식) -->
            <div style="
                position: absolute; 
                top: {bone_data[st.session_state.current_bone]['pos'][0]}%; 
                left: {bone_data[st.session_state.current_bone]['pos'][1]}%; 
                width: 18px; 
                height: 18px; 
                background-color: #ff4757; 
                border: 2px solid white; 
                border-radius: 50%; 
                box-shadow: 0 0 10px red; 
                transform: translate(-50%, -50%); 
                z-index: 10;">
            </div>
        </div>
    """, unsafe_allow_html=True)
except:
    st.error("Check your skeleton.jpg and GitHub ID.")

st.markdown("---")

# 4. 퀴즈 섹션
options = bone_data[st.session_state.current_bone]["options"]
random.shuffle(options)

st.subheader("❓ What is this bone?")
cols = st.columns(2)
for i, option in enumerate(options):
    with cols[i % 2]:
        if st.button(option, use_container_width=True):
            if option == st.session_state.current_bone:
                st.success("🎯 CORRECT!")
                st.session_state.score += 10
                st.session_state.quiz_count += 1
                st.session_state.current_bone = random.choice(list(bone_data.keys()))
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ INCORRECT")

# 5. 대시보드
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.metric("Solved", st.session_state.quiz_count)
