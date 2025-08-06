import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="Clinical Assets Dashboard", layout="wide")

# تقسيم الصفحة إلى عمودين (يسار للشعارات، يمين للمحتوى)
col1, col2 = st.columns([1, 2])

with col1:
    # شعار سيمنس
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=150)  # غير المسار إذا لازم

    # شعار CAD
    st.image("https://i.postimg.cc/Nj9t3KVL/image0.png", width=150)  # حط أي شعار مؤقت للمشروع

    st.markdown("<br><br>", unsafe_allow_html=True)  # مسافة فاصلة

    # نص ترحيبي
    st.markdown(
        "<h3 style='color:grey;'>C-Arm Dashboard</h3>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### ")

    # ثلاثة أعمدة للدوائر
    col_a, col_b, col_c = st.columns(3)

    circle_style = """
        width:150px; height:150px; border-radius:50%;
        background-color:#FF9800; display:flex;
        justify-content:center; align-items:center;
        color:white; font-weight:bold; font-size:18px;
        transition: all 0.3s ease; margin:auto;
    """

    with col_a:
        st.markdown(
            f"""
            <a href="?page=Schedule" style="text-decoration:none;">
                <div style="{circle_style}">Schedule</div>
            </a>
            """,
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown(
            f"""
            <a href="?page=Maintenance" style="text-decoration:none;">
                <div style="{circle_style}">Maintenance</div>
            </a>
            """,
            unsafe_allow_html=True
        )

    with col_c:
        st.markdown(
            f"""
            <a href="?page=Quiz" style="text-decoration:none;">
                <div style="{circle_style}">Quiz</div>
            </a>
            """,
            unsafe_allow_html=True
        )
