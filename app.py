import streamlit as st
import random
import time
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="Professional Anatomy Quiz", page_icon="💀", layout="centered")

# 2. 뼈 데이터 (이미지 크기에 맞춰 좌표 조절 필요)
# (y좌표, x좌표) 순서입니다.
bone_data = {
    "Skull (Cranium)": {"pos": (80, 250), "options": ["Skull", "Mandible", "Cervical", "Clavicle"]},
    "Mandible": {"pos": (130, 250), "options": ["Mandible", "Maxilla", "Hyoid", "Skull"]},
    "Clavicle": {"pos": (180, 200), "options": ["Clavicle", "Scapula", "Sternum", "Humerus"]},
    "Sternum": {"pos": (250, 250), "options": ["Sternum", "Ribs", "Clavicle", "Xiphoid"]},
    "Humerus": {"pos": (300, 160), "options": ["Humerus", "Radius", "Ulna", "Femur"]},
    "Pelvis": {"pos": (450, 250), "options": ["Pelvis", "Femur", "Sacrum", "Ilium"]},
    "Femur": {"pos": (600, 200), "options": ["Femur", "Tibia", "Fibula", "Patella"]},
    "Patella": {"pos": (720, 200), "options": ["Patella", "Femur", "Tibia", "Fibula"]},
    "Tibia": {"pos": (850, 210), "options": ["Tibia", "Fibula", "Tarsals", "Femur"]},
    "Fibula": {"pos": (850, 240), "options": ["Fibula", "Tibia", "Talus", "Tarsals"]}
}

# 세션 상태 초기화
if 'score' not in st.session_state: st.session_state.score = 0
if 'quiz_count' not in st.session_state: st.session_state.quiz_count = 0
if 'current_bone' not in st.session_state: st.session_state.current_bone = random.choice(list(bone_data.keys()))

st.title("💀 AI Anatomy Diagnostic System")
st.write("Professional Medical Quiz: Identify the highlighted bone.")

# 3. 이미지와 마커 표시
try:
    image = Image.open("skeleton.jpg")
    y, x = bone_data[st.session_state.current_bone]["pos"]
    
    st.markdown(f"""
        <div style="position: relative; width: 100%; max-width: 500px; margin: auto;">
            <img src="https://raw.githubusercontent.com/{st.session_state.get('user_id', '본인아이디')}/bone-quiz/main/skeleton.jpg" style="width: 100%; border-radius: 10px; border: 2px solid #4a90e2;">
            <div style="position: absolute; top: {y}px; left: {x}px; width: 22px; height: 22px; background-color: #ff4757; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 15px red; transform: translate(-50%, -50%); z-index: 10;"></div>
        </div>
    """, unsafe_allow_html=True)
except:
    st.error("Please ensure 'skeleton.jpg' is uploaded to your GitHub repository.")

st.markdown("---")

# 4. 퀴즈 섹션 (영문 객관식)
options = bone_data[st.session_state.current_bone]["options"]
random.shuffle(options)

st.subheader("❓ Question: What is this bone?")
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
st.sidebar.metric("Total Score", st.session_state.score)
st.sidebar.metric("Solved Cases", st.session_state.quiz_count)
