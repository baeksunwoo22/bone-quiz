import streamlit as st
import random
import time
import base64
import os

# 1. 페이지 설정
st.set_page_config(page_title="Anatomy Quiz Final", page_icon="💀", layout="centered")

# 2. 뼈 데이터 (이미지 대비 위치 %: top, left)
# 점 위치가 이상하면 이 숫자들을 (위아래, 좌우) 순서로 조금씩 고치세요!
bone_data = {
    "Skull (Cranium)": {"pos": (12, 50), "options": ["Skull", "Mandible", "Cervical", "Clavicle"]},
    "Mandible": {"pos": (16, 50), "options": ["Mandible", "Maxilla", "Hyoid", "Skull"]},
    "Clavicle": {"pos": (22, 40), "options": ["Clavicle", "Scapula", "Sternum", "Humerus"]},
    "Sternum": {"pos": (32, 50), "options": ["Sternum", "Ribs", "Clavicle", "Xiphoid"]},
    "Humerus": {"pos": (38, 32), "options": ["Humerus", "Radius", "Ulna", "Femur"]},
    "Pelvis": {"pos": (55, 50), "options": ["Pelvis", "Femur", "Sacrum", "Ilium"]},
    "Femur": {"pos": (70, 42), "options": ["Femur", "Tibia", "Fibula", "Patella"]},
    "Patella": {"pos": (78, 42), "options": ["Patella", "Femur", "Tibia", "Fibula"]},
    "Tibia": {"pos": (88, 40), "options": ["Tibia", "Fibula", "Tarsals", "Femur"]}
}

if 'score' not in st.session_state: st.session_state.score = 0
if 'quiz_count' not in st.session_state: st.session_state.quiz_count = 0
if 'current_bone' not in st.session_state: 
    st.session_state.current_bone = random.choice(list(bone_data.keys()))

st.title("💀 AI Anatomy Quiz")

# 3. 이미지 로드 로직 (Base64 방식 - 가장 확실함)
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_file = "skeleton.jpg"

if os.path.exists(image_file):
    img_base64 = get_base64_image(image_file)
    y, x = bone_data[st.session_state.current_bone]["pos"]
    
    st.markdown(f"""
        <div style="position: relative; width: 100%; max-width: 400px; margin: auto;">
            <!-- 이미지를 Base64로 직접 삽입 (주소 에러 방지) -->
            <img src="data:image/jpeg;base64,{img_base64}" style="width: 100%; height: auto; border-radius: 10px; border: 2px solid #4a90e2;">
            <!-- 빨간 점 -->
            <div style="
                position: absolute; 
                top: {y}%; 
                left: {x}%; 
                width: 20px; 
                height: 20px; 
                background-color: #ff4757; 
                border: 2px solid white; 
                border-radius: 50%; 
                box-shadow: 0 0 15px red; 
                transform: translate(-50%, -50%); 
                z-index: 10;">
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("GitHub 저장소에 'skeleton.jpg' 파일이 있는지 확인해 주세요!")

st.markdown("---")

# 4. 퀴즈 섹션
options = bone_data[st.session_state.current_bone]["options"]
random.shuffle(options)

st.subheader("❓ What is this bone?")
cols = st.columns(2)
for i, option in enumerate(options):
    with cols[i % 2]:
        if st.button(option, key=f"btn_{i}_{st.session_state.quiz_count}", use_container_width=True):
            if option == st.session_state.current_bone:
                st.success("🎯 CORRECT!")
                st.session_state.score += 10
                st.session_state.quiz_count += 1
                st.session_state.current_bone = random.choice(list(bone_data.keys()))
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ INCORRECT")

# 5. 사이드바
st.sidebar.metric("Total Score", st.session_state.score)
st.sidebar.metric("Solved", st.session_state.quiz_count)
