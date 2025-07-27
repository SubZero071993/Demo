import streamlit as st
import pandas as pd
from datetime import datetime

# البيانات
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

# تحويل إلى DataFrame
df = pd.DataFrame(data, columns=columns)

# تحويل التاريخ
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], format="%d-%m-%y")
today = datetime(2025, 7, 27)
df["Days in Site"] = (today - df["Delivery Date"]).dt.days

# عمود "هل الجهاز خربان؟" – افتراضيًا كل الأجهزة سليمة
df["Is Broken?"] = False

# عرض الجدول
st.title("C-arm Device Table")
st.dataframe(df, use_container_width=True)
