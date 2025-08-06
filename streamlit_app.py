import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="C-Arm Dashboard", layout="centered")

# CSS للدوائر مع تأثير التكبير عند المرور
st.markdown("""
    <style>
        .circle-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 80px;
            margin-top: 100px;
        }
        .circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background-color: #3498db;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 20px;
            font-weight: bold;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .circle:hover {
            transform: scale(1.2);
            background-color: #2980b9;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# عناوين الدوائر وروابطها (ممكن لاحقًا تحط صفحات متعددة)
st.markdown("""
    <div class="circle-container">
        <a href="?page=Schedule" class="circle">Schedule</a>
        <a href="?page=Maintenance" class="circle">Maintenance</a>
        <a href="?page=Quiz" class="circle">Quiz</a>
    </div>
""", unsafe_allow_html=True)

# محتوى الصفحات البسيط كاختبار
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Home"])[0]

if page == "Schedule":
    st.title("📅 Schedule Page")
    st.write("هنا ممكن تضيف جدول الحجوزات.")
elif page == "Maintenance":
    st.title("🛠 Maintenance Page")
    st.write("هنا تقدر تعرض الأعطال والصيانة.")
elif page == "Quiz":
    st.title("❓ Quiz Page")
    st.write("هنا تقدر تضيف اختبار أو تقييم سريع.")
else:
    st.title("🏠 Welcome to C-Arm Dashboard")
    st.write("اختر أي دائرة للمتابعة 👆")
