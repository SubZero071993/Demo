import streamlit as st
import pandas as pd
from datetime import datetime

#Logo
st.image( "https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300 )

# بيانات الأجهزة
data = [
    ["Cios Select FD VA20", "22-07-25", 20087, "warehouse", "", ""],
    ["Cios Connect", "25-05-25", 21521, "Al-Rawdhah Hospital (until we submit Cios Select)", "Ayman Tamimi", ""],
    ["Cios Fusion", "13-08-25", 31181, "Prince Sultan Military Hospital", "Tuqa", ""],
    ["Cios Alpha VA20", "05-08-25", 13020, "warehouse", "", ""],
    ["Cios Alpha VA30", "03-07-25", 43815, "Aster Sanad Hospital", "Ammar", ""],
    ["Cios Spin VA30", "12-08-25", 50097, "warehouse", "", ""]
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
df["Days in Site"] = df.apply(
    lambda row: (pd.to_datetime(today) - pd.to_datetime(row["Delivery Date"])).days 
    if row["Current Location"].strip().lower() != "warehouse" else "",
    axis=1
)

# إضافة عمود "هل الجهاز خربان؟" (قابل للتعديل)
df["Malfunctioned?"] = False

# عنوان الصفحة
st.set_page_config(layout="wide")
st.title("📋C-Arm Demo (CAD)")

# عرض الجدول قابل للتعديل
edited_df = st.data_editor(
    df,
    column_config={
        "Account Manager": st.column_config.SelectboxColumn(
            "Account Manager",
            options=[
                "Moath", "Ayman Tamimi", "Wesam", "Ammar", "Ayman Ghandurah", 
                "Saleh", "Najla", "Tuqa", "Mohammad Al-Hamed", "Mohammad Al-Mutairi", 
                "Ahmad", "Iqbal", "Anas", "Mohammad Gharibeh"
            ]
        )
    },
    use_container_width=True,
    num_rows="dynamic"
)

# ====== 🎨 تنسيق الألوان ======
def highlight_row(row):
    try:
        days = float(row["Days in Site"])
    except:
        days = 0
    if row["Malfunctioned?"]:
        return ["background-color: lightgray"] * len(row)
    elif days > 30:
        return ["background-color: #FF6F61"] * len(row)
    elif days > 14:
        return ["background-color: lightyellow"] * len(row)
    elif str(row["Current Location"]).strip().lower() == "warehouse":
        return ["background-color: lightgreen"] * len(row)
    else:
        return [""] * len(row)

st.markdown("### 🎨 Final Results:")
styled_df = edited_df.style.apply(highlight_row, axis=1)
st.dataframe(styled_df, use_container_width=True)
