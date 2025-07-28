import streamlit as st
import pandas as pd
from datetime import datetime

#Logo
st.image( "https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300 )

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
df["Days in Site"] = df.apply(
    lambda row: (pd.to_datetime(today) - pd.to_datetime(row["Delivery Date"])).days 
    if row["Current Location"].strip().lower() != "warehouse" else "",
    axis=1
)

# إضافة عمود "هل الجهاز خربان؟" (قابل للتعديل)
df["Is Broken?"] = False

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
    if row["Is Broken?"]:
        return ["background-color: lightgray"] * len(row)
    elif str(row["Current Location"]).strip().lower() == "warehouse":
        return ["background-color: lightgreen"] * len(row)
    elif isinstance(row["Days in Site"], (int, float)) and row["Days in Site"] > 14:
        return ["background-color: lightyellow"] * len(row)
    else:
        return [""] * len(row)

st.markdown("### 🎨 Final Results:")
styled_df = edited_df.style.apply(highlight_row, axis=1)
st.dataframe(styled_df, use_container_width=True)

st.set_page_config(layout="wide")
st.title("📎Brochures and Configurations ") 
devices = [
    {
        "Device": "Cios Connect",
        "Brochure": "https://smallpdf.com/file#s=a25c199b-1739-4745-a81a-e1725caba96c",
        "Configuration": "https://smallpdf.com/file#s=57bb6fa2-cba3-4971-bbce-0049462e9165"
    },
    {
        "Device": "Cios Fusion",
        "Brochure": "https://smallpdf.com/file#s=cec6d7a8-4b7a-47c5-bfa2-a098da63f422",
        "Configuration": "https://smallpdf.com/file#s=dfd03daa-a6f0-4ad7-84a9-235b585cbf38"
    },
    {
        "Device": "Cios Alpha VA30",
        "Brochure": "https://smallpdf.com/file#s=0371cf4c-e55e-48bb-82bb-ffd6aa2cf9d2",
        "Configuration": "https://smallpdf.com/file#s=b07cc63b-0327-4b5a-b2f6-59fc2ec66e2b"
    },
    {
        "Device": "Cios Spin",
        "Brochure": "https://smallpdf.com/file#s=3b4c2ced-54cb-48d4-8124-9e9f8beb5f15",
        "Configuration": "https://smallpdf.com/file#s=9a377c59-e004-4804-8d3c-6c8f2e53309d"
    }
]

import streamlit as st

icon_brochure = "📄"
icon_config = "🛠️"

for device in devices:
    st.markdown(f"### {device['Device']}")
    st.markdown(
        f"{icon_brochure} Brochure: [Click here]({device['Brochure']})  \n"
        f"{icon_config} Configuration: [Click here]({device['Configuration']})"
    )



st.markdown("Developed by **Hossam Al-Zahrani**  \nAT Product Manager")
