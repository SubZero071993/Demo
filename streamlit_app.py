import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Demo Tracker", layout="wide")
st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300)
st.title("C-arm Demo Unit Tracker")

# البيانات الأساسية
data = {
    "Model": ["Cios Alpha", "Cios Spin", "Cios Select", "Cios Fit", "Cios Fusion", "Cios Flow"],
    "Delivery Date": ["2025-07-01", "2025-07-03", "2025-07-10", "2025-07-15", "2025-07-18", "2025-07-21"],
    "Location": ["Riyadh", "Jeddah", "Warehouse", "Dammam", "Makkah", "Warehouse"],
    "Application Specialist": ["Ali", "Sara", "Ahmed", "Lama", "Omar", "Yasmin"],
    "Account Manager": ["Moath", "Ayman Tamimi", "Wesam", "Ammar", "Saleh", "Mohammad Al-Hamed"],
    "Brochure": [
        "https://example.com/brochure_alpha.pdf",
        "https://example.com/brochure_spin.pdf",
        "https://example.com/brochure_select.pdf",
        "https://example.com/brochure_fit.pdf",
        "https://example.com/brochure_fusion.pdf",
        "https://example.com/brochure_flow.pdf",
    ],
    "Configuration": [
        "https://example.com/config_alpha.pdf",
        "https://example.com/config_spin.pdf",
        "https://example.com/config_select.pdf",
        "https://example.com/config_fit.pdf",
        "https://example.com/config_fusion.pdf",
        "https://example.com/config_flow.pdf",
    ],
}

# تحويل إلى DataFrame
df = pd.DataFrame(data)
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"])

# تعديل مباشر داخل الجدول
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# عرض روابط للتحميل
st.markdown("### 📎 Clickable Links")
for i in range(len(edited_df)):
    st.markdown(f"**{edited_df.loc[i, 'Model']}** - [Brochure]({edited_df.loc[i, 'Brochure']}) | [Configuration]({edited_df.loc[i, 'Configuration']})")

# تنبيه للأجهزة اللي برا المستودع وتعدّت ١٤ يوم
st.markdown("### 🔔 Alert System")
today = datetime.today()
for i in range(len(edited_df)):
    days_out = (today - edited_df.loc[i, "Delivery Date"]).days
    if edited_df.loc[i, "Location"].lower() != "warehouse" and days_out > 14:
        st.error(f"{edited_df.loc[i, 'Model']} has been out for {days_out} days!")
