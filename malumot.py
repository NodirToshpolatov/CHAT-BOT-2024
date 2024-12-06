import streamlit as st
import openai

# OpenAI API kalitini sozlash
openai.api_key = "API_KEY"

# txt fayldan foydalanuvchi ma'lumotlarini o'qish va ajratish
def read_user_data(file_path):
    user_data = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 4:
                        nickname, password, api_key, experience = parts
                        user_data.append({
                            "nickname": nickname.strip(),
                            "password": password.strip(),
                            "api_key": api_key.strip(),
                            "experience": experience.strip()
                        })
                    else:
                        st.error(f"Xato format: {line} (Format: nickname,password,apikey,experience)")
        return user_data
    except FileNotFoundError:
        st.error(f"Fayl topilmadi: {file_path}")
        return []
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
        return []

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


# Foydalanuvchi ma'lumotlarini o'qish
file_path = "user_data.txt"
users = read_user_data(file_path)

if users:
    current_user = users[0]
else:
    st.error("Foydalanuvchi ma'lumotlari topilmadi.")
    current_user = None

# Javob olish funksiyasi
def get_response(messages, user_question):
    programming_keywords = [
    # Dasturlash tillari
    "python", "java", "javascript", "c++", "c#", "go", "ruby", "php", "swift", "kotlin", "r", "typescript", "scala",
    "perl", "shell", "bash", "html", "css", "sql", "matlab", "dart", "rust",

    # Dasturlashga oid atamalar
    "code", "programming", "algorithm", "function", "variable", "array", "object", "class", "loop", "conditional",
    "recursion", "method", "debug", "compile", "execute", "pointer", "stack", "queue", "data structure",
    "linked list", "hashmap", "dictionary", "module", "package", "framework", "library", "api", "json", "xml",
    "regex", "inheritance", "polymorphism", "abstraction", "encapsulation", "multithreading", "concurrency", "pipeline",

    # Matematik atamalar
    "matrix", "vector", "derivative", "integral", "limit", "equation", "function", "logarithm", "exponent",
    "probability", "statistics", "mean", "median", "mode", "standard deviation", "variance", "distribution",
    "set", "union", "intersection", "factorial", "permutation", "combination", "fourier", "laplace",
    "eigenvalue", "eigenvector", "linear algebra", "differential equation", "optimization", "gradient descent",
    "loss function", "cost function", "normalization", "standardization", "correlation", "covariance", "hypothesis"
]

    if not any(keyword in user_question.lower() for keyword in programming_keywords):
        return "Kechirasiz men bunday mavzudagi savollarga javob bera olmayman."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Xatolik yuz berdi: {e}"

# Streamlit interfeysi
st.title("Dasturlash tillari yordamchisi (Chat)")

# Dasturlash tilini tanlash
languages = ["Python", "JavaScript", "Java", "C++", "Go"]
selected_language = st.selectbox("Dasturlash tilini tanlang:", languages)

# Chat sessiyasini boshlash
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"Siz {selected_language} bo'yicha yordamchisiz."}
    ]

# Chat xabarlarini ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Yangi xabar uchun input
if user_input := st.chat_input("Savolingizni kiriting:"):
    # Foydalanuvchi xabarini qo'shish
    st.session_state.messages.append({"role": "user", "content": f"Sen {selected_language} bo'yicha O'rtacha darajada javob beradigan yordamchisan va hoziz {user_input} savoli dasturlash yoki dasturlash algoritmi va yana dasturlash matematikasiga oid bolmasa unga 'Kechirasiz, men faqat dasturlash sohasiga oid savollarga javob bera olaman.' deb javob ber"} )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Javobni olish
    with st.chat_message("assistant"):
        with st.spinner("Javob olinmoqda..."):
            response = get_response(st.session_state.messages, user_input)
            st.markdown(response)
        # Yordamchi xabarini qo'shish
        st.session_state.messages.append({"role": "assistant", "content": response})
