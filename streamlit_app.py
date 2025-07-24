import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Demo Tracker", layout="wide")

# Siemens logo
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Siemens-Healthineers-Logo.svg/2560px-Siemens-Healthineers-Logo.svg.png", width=300)

st.title("C-arm Demo Unit Tracker")

# Sample data
data = {
    "Model": ["Cios Alpha", "Cios Spin", "Cios Select", "Cios Fit", "Cios Fusion", "Cios Flow"],
    "Delivery Date": ["2025-07-01", "2025-07-03", "2025-07-10", "2025-07-15", "2025-07-18", "2025-07-21"],
    "Location": ["Riyadh", "Jeddah", "Warehouse", "Dammam", "Makkah", "Warehouse"],
    "Application Specialist": ["Ali", "Sara", "Ahmed", "Lama", "Omar", "Yasmin"],
    "Account Manager": ["Moath", "Ayman Tamimi", "Wesam", "Ammar", "Saleh", "Mohammad Al-Hamed"],
    "Brochure": [
        "[Click Here](https://example.com/brochure_alpha.pdf)",
        "[Click Here](https://example.com/brochure_spin.pdf)",
        "[Click Here](https://example.com/brochure_select.pdf)",
        "[Click Here](https://example.com/brochure_fit.pdf)",
        "[Click Here](https://example.com/brochure_fusion.pdf)",
        "[Click Here](https://example.com/brochure_flow.pdf)",
    ],
    "Configuration": [
        "[Click Here](https://example.com/config_alpha.pdf)",
        "[Click Here](https://example.com/config_spin.pdf)",
        "[Click Here](https://example.com/config_select.pdf)",
        "[Click Here](https://example.com/config_fit.pdf)",
        "[Click Here](https://example.com/config_fusion.pdf)",
        "[Click Here](https://example.com/config_flow.pdf)",
    ],
}

df = pd.DataFrame(data)

# Convert date column
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"])

# Editable fields
for i in range(len(df)):
    with st.expander(f"{df.loc[i, 'Model']} - Edit Info"):
        df.loc[i, "Delivery Date"] = st.date_input(f"Delivery Date - {df.loc[i, 'Model']}", value=df.loc[i, "Delivery Date"], key=f"date_{i}")
        df.loc[i, "Location"] = st.text_input(f"Location - {df.loc[i, 'Model']}", value=df.loc[i, "Location"], key=f"loc_{i}")
        df.loc[i, "Application Specialist"] = st.text_input(f"App Specialist - {df.loc[i, 'Model']}", value=df.loc[i, "Application Specialist"], key=f"app_{i}")
        df.loc[i, "Account Manager"] = st.selectbox(f"Account Manager - {df.loc[i, 'Model']}",
            ["Moath", "Ayman Tamimi", "Wesam", "Ammar", "Ayman Ghandurah", "Saleh", "Mohammad Al-Hamed", "Mohammad Al-Mutairi", "Ahmad", "Iqbal", "Mohammad Gharabieh"],
            index=["Moath", "Ayman Tamimi", "Wesam", "Ammar", "Ayman Ghandurah", "Saleh", "Mohammad Al-Hamed", "Mohammad Al-Mutairi", "Ahmad", "Iqbal", "Mohammad Gharabieh"].index(df.loc[i, "Account Manager"]),
            key=f"am_{i}"
        )

# Display updated table
st.markdown("### Updated Table")
st.dataframe(df, use_container_width=True)

# Alert if any demo unit > 14 days outside warehouse
st.markdown("### Alert System")

today = datetime.today()
for i in range(len(df)):
    days_out = (today - df.loc[i, "Delivery Date"]).days
    if df.loc[i, "Location"].lower() != "warehouse" and days_out > 14:
        st.error(f"{df.loc[i, 'Model']} has been out for {days_out} days!")
