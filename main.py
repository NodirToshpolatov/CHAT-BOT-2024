import streamlit as st
import os

USER_DATA_FILE = "user_data.txt"

def save_user_data(nickname, password, api_key, experience):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{nickname},{password},{api_key},{experience}\n")

def update_user_data(nickname, password, api_key, experience):
    if os.path.exists(USER_DATA_FILE):
        updated_lines = []
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                saved_nickname, saved_password, _, _ = line.strip().split(",")
                if saved_nickname == nickname and saved_password == password:
                    updated_lines.append(f"{nickname},{password},{api_key},{experience}\n")
                else:
                    updated_lines.append(line)
        with open(USER_DATA_FILE, "w") as file:
            file.writelines(updated_lines)
    else:
        save_user_data(nickname, password, api_key, experience)

def check_user_exists(nickname):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                saved_nickname, saved_password, _, _ = line.strip().split(",")
                if saved_nickname == nickname and saved_password == password:
                    return True
    return False

def get_user_data(nickname, password):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                saved_nickname, saved_password, saved_api_key, _ = line.strip().split(",")
                if saved_nickname == nickname and saved_password == password:
                    return saved_api_key
    return None

def add_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_background_image("https://fotoblik.ru/wp-content/uploads/2023/09/fon-dlia-rabochego-stola-programmista-27.webp")

st.title("Foydalanuvchi tizimi")

if "action" not in st.session_state:
    st.session_state.action = "Ro'yxatdan o'tish"

def update_action(selected_action):
    st.session_state.action = selected_action
    st.session_state.nickname = ""
    st.session_state.password = ""
    st.session_state.api_key = ""
    st.session_state.experience = "Endi boshlayapman"

action = st.radio("Iltimos, amalni tanlang:", ("Ro'yxatdan o'tish", "Kirish"), index=0, on_change=update_action, args=(st.session_state.action,))

if action == "Ro'yxatdan o'tish":
    st.subheader("Yangi foydalanuvchi yaratish")
    nickname = st.text_input("Nicknameingizni kiriting:", key="nickname")
    password = st.text_input("Parolingizni kiriting:", type="password", key="password")
    api_key = st.text_input("API kalitingizni kiriting:", key="api_key")
    st.subheader("Dasturlash tajribangizni tanlang:")
    experience = st.radio("Siz dasturlashga qanchalik qiziqasiz yoki qanchalik tajribalisiz?", options=["Endi boshlayapman", "O'rtacha tajribam bor", "Professional dasturchiman"], key="experience")
    if st.button("Ro'yxatdan o'tish"):
        if nickname and password and api_key:
            if check_user_exists(nickname):
                st.warning("Foydalanuvchi mavjud! Ma'lumotlaringizni yangilashni xohlaysizmi?")
                if st.button("Ma'lumotlarni yangilash"):
                    update_user_data(nickname, password, api_key, experience)
                    st.success("Ma'lumotlaringiz yangilandi!")
            else:
                save_user_data(nickname, password, api_key, experience)
                st.success("Ro'yxatdan muvaffaqiyatli o'tdingiz!")
        else:
            st.error("Barcha maydonlarni to‘ldiring!")

elif action == "Kirish":
    st.subheader("Kirish")
    nickname = st.text_input("Nicknamenizni kiriting:", key="nickname")
    password = st.text_input("Parolingizni kiriting:", type="password", key="password")
    if st.button("Kirish"):
        if nickname and password:
            api_key = get_user_data(nickname, password)
            if api_key:
                st.success("Muvaffaqiyatli kirdingiz!")
                st.write(f"🔑 API kalitingiz: {api_key}")
            else:
                st.error("Nickname yoki parol noto‘g‘ri!")
        else:
            st.error("Barcha maydonlarni to‘ldiring!")
