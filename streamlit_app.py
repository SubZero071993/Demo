from datetime import datetime
import pandas as pd
import streamlit as st
import base64

# إعداد الصفحة
st.set_page_config(page_title="C-Arm Tracker", layout="wide")

# تحميل الشعار وعرضه
with open("siemens_logo.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()
st.markdown(
    f'<div style="text-align: center;"><img src="data:image/png;base64,{encoded_image}" width="200"></div>',
    unsafe_allow_html=True
)

# عنوان الصفحة
st.markdown("<h1 style='text-align: center;'>C-Arm Dashboard (CAD)</h1>", unsafe_allow_html=True)
st.markdown("---")

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_excel("c_arm_data.xlsx")

df = load_data()

# حساب عدد الأيام في كل موقع
def calculate_days(date_str):
    try:
        date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
        delta = datetime.now() - date_obj
        return delta.days
    except:
        return None

df["Days in Location"] = df["Delivery Date"].apply(calculate_days)

# استثناء الأجهزة الموجودة في المستودع من التنبيه
df["Notify"] = df["Current Location"].apply(lambda x: False if "مستودع" in str(x) else True)

# عرض الجدول بدون تعديل
st.dataframe(df, use_container_width=True)
