import streamlit as st
import pandas as pd
from datetime import datetime

# بيانات الأجهزة
data = [
    ["Cios Select FD VA20", "22-07-25", 20087, "warehouse", "", ""],
    ["Cios Connect", "25-05-25", 21521, "Al-Rawdhah Hospital (until we submit Cios Select)", "Ayman Tamimi", ""],
    ["Cios Fusion", "27-07-25", 31181, "warehouse", "", ""],
    ["Cios Alpha VA20", "29-05-25", 13020, "Al-Hayyat Hospital (until they receive their C-arm)", "Ammar", ""],
    ["Cios Alpha VA30", "03-07-25", 43815, "Aster Sanad Hospital", "Ammar", ""],
    ["Cios Spin VA30", "10-07-25", 50097, "Johns Hopkins Aramco Hospital", "Ayman Tamimi", "Ali"]
]

columns = [
    "Demo C-arm Model", 
    "Delivery Date", 
    "Serial #", 
    "Current Location", 
    "Account Manager", 
    "Application Specialist"
]

# تحويل البيانات إلى DataFrame
df = pd.DataFrame(data, columns=columns)

# تحويل التاريخ وإزالة الوقت
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], format="%d-%m-%y").dt.date

# حساب عدد الأيام في الموقع
today = datetime(2025, 7, 27).date()
df["Days in Site"] = (pd.to_datetime(today) - pd.to_datetime(df["Delivery Date"])).dt.days

# إضافة عمود "هل الجهاز خربان؟" (قابل للتعديل)
df["Is Broken?"] = False

# عنوان الصفحة
st.set_page_config(layout="wide")
st.title("📋 جدول أجهزة C-arm التجريبية")

# عرض الجدول قابل للتعديل
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic"
)

