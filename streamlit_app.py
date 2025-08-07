import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

# إعداد الصفحة
st.set_page_config(layout="wide")
st.markdown("<style>body {background-color: #f5f5f5;}</style>", unsafe_allow_html=True)

# شعارات في الجانب الأيسر
col1, col2 = st.columns([1, 5])
with col1:
    siemens_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Siemens-logo.svg/2560px-Siemens-logo.svg.png"
    st.image(siemens_logo, width=150)
    st.image("logo_placeholder.png", caption="CAD Project", width=150)  # شعار الكاد

with col2:
    st.markdown("## ")
    st.markdown("## ")
    st.markdown("## ")

    # تصميم الدوائر
    st.markdown(
        '''
        <style>
        .circle-container {
            display: flex;
            justify-content: space-around;
            margin-top: 50px;
        }
        .circle {
            width: 150px;
            height: 150px;
            background-color: orange;
            color: white;
            font-weight: bold;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            text-align: center;
            cursor: pointer;
        }
        .circle:hover {
            transform: scale(1.3);
        }
        </style>
        <div class="circle-container">
            <div class="circle" onclick="window.location.href='/?selected=requests'">📩<br>Requests</div>
            <div class="circle" onclick="window.location.href='/?selected=schedule'">📅<br>Schedule</div>
            <div class="circle" onclick="window.location.href='/?selected=documents'">📄<br>Documents</div>
            <div class="circle" onclick="window.location.href='/?selected=3d'">🧊<br>3D</div>
            <div class="circle" onclick="window.location.href='/?selected=maintenance'">🔧<br>Maintenance</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# التعامل مع التنقل بين الصفحات
query_params = st.experimental_get_query_params()
selected = query_params.get("selected", [None])[0]

if selected == "requests":
    st.header("📩 Requests Page")
    st.write("هنا تقدر ترسل طلبات معينة.")

elif selected == "schedule":
    st.header("📅 Schedule Page")
    st.write("هنا الجدول الكامل للأجهزة.")

elif selected == "documents":
    st.header("📄 Documents Page")
    st.write("هنا ملفات PDF و Word للمشروع.")

elif selected == "3d":
    st.header("🧊 3D Viewer")
    st.write("هنا نموذج ثلاثي الأبعاد للأجهزة.")

elif selected == "maintenance":
    st.header("🔧 Maintenance Page")
    st.write("هنا تفاصيل أعطال الأجهزة السابقة.")
