import streamlit as st
import base64

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

# Layout: Siemens + CAD logo
st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300)

# Page logic
selected_page = st.session_state.get("selected_page", "")

# Circle buttons
if not selected_page:
    st.markdown("""
        <div class="circle-container">
            <form action="" method="post">
                <button name="page" value="requests" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=64nKv4tDb3Qt&format=png&color=000000" width="80"><br>Requests
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="schedule" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=117507&format=png&color=000000" width="80"><br>Schedule
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="documents" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=42415&format=png&color=000000" width="80"><br>Documents
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="3d" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=5WoqJ6SAzPMX&format=png&color=000000" width="80"><br>3D
                </button>
            </form>
            <form action="" method="post">
                <button name="page" value="maintenance" class="circle-button">
                    <img src="https://img.icons8.com/?size=100&id=102356&format=png&color=000000" width="80"><br>Maintenance
                </button>
            </form>
        </div>
    """, unsafe_allow_html=True)

# Detect click
if "page" in st.query_params:
    selected_page = st.query_params["page"]
    st.session_state["selected_page"] = selected_page

# Page content
if selected_page == "requests":
    st.header("📧 طلبات")
    st.write("صفحة الطلبات هنا...")
elif selected_page == "schedule":
    st.header("🗓️ الجدول")
    st.write("صفحة الجدول هنا...")
elif selected_page == "documents":
    st.header("📄 مستندات")
    st.write("صفحة المستندات هنا...")
elif selected_page == "3d":
    st.header("🧊 عرض ثلاثي الأبعاد")
    st.write("صفحة الـ 3D هنا...")
elif selected_page == "maintenance":
    st.header("🔧 صيانة")
    st.write("صفحة الأعطال هنا...")
