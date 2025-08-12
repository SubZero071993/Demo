import streamlit as st
import base64

st.title(" Clinical Assets Dashboard (CAD)")

st.set_page_config(page_title="CAD Portal", layout="wide")


# CSS for hover effect
st.markdown("""
    <style>
    .circle-container {
        display: flex;
        justify-content: center;
        gap: 50px;
        margin-top: 50px;
        flex-wrap: wrap;
    }
    .circle-button {
        background-color: #FF6F00;
        color: white;
        border: none;
        border-radius: 50%;
        width: 150px;
        height: 150px;
        font-size: 18px;
        text-align: center;
        line-height: 1.5;
        cursor: pointer;
        transition: transform 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .circle-button:hover {
        transform: scale(1.2);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([10, 1, 10, 1, 1, 1, 1, 1, 1, 1])  # تقسيم الصفحة إلى 10 أعمدة بنسبة مختلفة

# الشعار اليسار (سيمنس)
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300)

# الشعار في الوسط (الكاد)
with col3:
    st.image("https://iili.io/FiS0iNa.png", width=300)


selected_page = st.session_state.get("selected_page")

# Circle buttons
if not selected_page:
    st.markdown("""
        <div class="circle-container">
            <form action="" method="post">
                <button name="page" value="requests" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=64nKv4tDb3Qt&format=png&color=000000" width="60"><br>Requests
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="schedule" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=117507&format=png&color=000000" width="60"><br>Schedule
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="documents" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=42415&format=png&color=000000" width="60"><br>Documents
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="3d" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=5WoqJ6SAzPMX&format=png&color=000000" width="60"><br>3D
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="maintenance" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=102356&format=png&color=000000" width="60"><br>Maintenance
                </button>
            </form>
        </div>
    """, unsafe_allow_html=True)

# Detect click
if "page" in st.query_params:
    selected_page = st.query_params["page"]
    st.session_state["selected_page"] = selected_page

# Example page logic
selected_page = st.session_state.get("selected_page")

if selected_page == "schedule":
    st.markdown("<h2>📅 جدول الأجهزة المجربة</h2>", unsafe_allow_html=True)
   
    # كود الجدول اللي تبي
    import pandas as pd
    data = {
        "Model": ["Cios Alpha", "Cios Select"],
        "Delivery Date": ["2025-07-01", "2025-07-15"],
        "Location": ["Riyadh", "Jeddah"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

elif selected_page == "requests":
    st.write("📨 هنا تقدر تتابع الطلبات")
elif selected_page == "documents":
    st.write("📄 مستندات الجهاز")
elif selected_page == "3d":
    st.write("🧊 ملفات 3D الخاصة بالجهاز")
elif selected_page == "maintenance":
    st.write("🔧 سجل الصيانة")
st.title("تطبيقك الجميل")

# محتوى التطبيق هنا

# نص الفوتر تحت الصفحة
st.markdown(
    """
    <div style='text-align: center; margin-top: 50px; color: gray; font-size: 14px;'>
        Developed by <b>Hossam Al-Zahrani</b><br>
        AT Product Manager
    </div>
    """,
    unsafe_allow_html=True
)
