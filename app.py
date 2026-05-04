import streamlit as st
import random
import time
from PIL import Image
import os

# 1. Page Config
st.set_page_config(page_title="Professional Anatomy Quiz", page_icon="💀", layout="centered")

# 2. Bone Data
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

if 'score' not in st.session_state: st.session_state.score = 0
if 'quiz_count' not in st.session_state: st.session_state.quiz_count = 0
if 'current_bone' not in st.session_state: st.session_state.current_bone = random.choice(list(bone_data.keys()))

st.title("💀 AI Anatomy Diagnostic System")
st.write("Identify the bone highlighted by the red marker.")

# 3. 이미지 표시 (주소 방식이 아닌 직접 파일 로드 방식)
image_path = "skeleton.jpg"

if os.path.exists(image_path):
    y, x = bone_data[st.session_state.current_bone]["pos"]
    
    # 이미지를 열어서 화면에 표시
    st.image(image_path, use_container_width=True)
    
    # 이미지 위에 빨간 점을 표시하기 위한 레이아웃 (HTML/CSS)
    # st.image 바로 아래에 점을 띄우는 것이 어려울 수 있어, 
    # 다시 한번 안정적인 HTML 렌더링 방식을 시도합니다. 
    # 단, 이번에는 로컬 이미지 데이터를 직접 활용합니다.
    import base64
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    
    st.markdown(f"""
        <div style="position: relative; width: 100%; max-width: 500px; margin: auto; margin-top: -550px;">
            <div style="height: 500px;"></div> <!-- 이미지 높이만큼 공간 확보 -->
            <div style="position: absolute; top: {y}px; left: {x}px; width: 22px; height: 22px; background-color: #ff4757; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 15px red; transform: translate(-50%, -50%); z-index: 99;"></div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error(f"'{image_path}' 파일을 찾을 수 없습니다. GitHub에 사진을 올렸는지 확인해주세요.")

st.markdown("---")

# 4. 퀴즈 섹션
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
