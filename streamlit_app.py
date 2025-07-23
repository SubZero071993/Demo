import streamlit as st
import pandas as pd
from datetime import datetime
from email.message import EmailMessage

st.set_page_config(page_title="C-arm Demo Tracker", layout="wide")
st.title("📦 C-arm Demo Tracker")

# ========================
# 1. Demo Data
# ========================

data = {
    'Demo C-arm Model': [
        'Cios Select FD VA20', 'Cios Connect', 'Cios Fusion',
        'Cios Alpha VA20', 'Cios Alpha VA30', 'Cios Spin VA30'
    ],
    'Delivery Date': [
        '22-07-25', '25-05-25', '25-06-25',
        '29-05-25', '03-07-25', '10-07-25'
    ],
    'Serial #': [20087, 21521, 31181, 13020, 43815, 50097],
    'Current Location': [
        'warehouse',
        'Al-Rawdah Hospital (until we submit Cios Select)',
        'Al-Salam Health Hospital',
        'Al-Hayyat Hospital (until they receive their C-arm)',
        'Aster Sanad Hospital',
        'Johns Hopkins Aramco Hospital'
    ],
    'Account Manager': [
        'Ayman Tamimi', 'Ayman Tamimi', 'Mohammad Gharibeh',
        'Ammar', 'Ammar', 'Ayman Tamimi'
    ],
    'Application Specialist': ['', '', 'Ali', '', '', 'Ali']
}

df = pd.DataFrame(data)

# Date formatting and calculations
df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], format='%d-%m-%y')
today = datetime.today()
df['Days Since Delivery'] = (today - df['Delivery Date']).dt.days
df['Needs Attention'] = (df['Days Since Delivery'] >= 14) & (df['Current Location'].str.lower() != 'warehouse')

# ========================
# 2. Full Table Display
# ========================

st.subheader("📋 All Demo Units")
st.dataframe(df, use_container_width=True)

# ========================
# 3. Filtered Table: Units Needing Attention
# ========================

attention_df = df[df['Needs Attention']]
st.subheader("🚨 Units Exceeding 14 Days (Not in Warehouse)")
if attention_df.empty:
    st.success("No units require attention ✅")
else:
    st.dataframe(attention_df, use_container_width=True)

# ========================
# 4. Email Body Generation
# ========================

def generate_email_body(df_attention):
    if df_attention.empty:
        return "✅ No demo units require attention this week."
    message = "🚨 The following demo units have exceeded 14 days:\n\n"
    for _, row in df_attention.iterrows():
        message += (
            f"- {row['Demo C-arm Model']} (Serial: {row['Serial #']})\n"
            f"  Location: {row['Current Location']}\n"
            f"  Delivered: {row['Delivery Date'].strftime('%d-%m-%Y')} "
            f"({row['Days Since Delivery']} days ago)\n\n"
        )
    message += "Please follow up with the relevant accounts as soon as possible.\n"
    return message

email_body = generate_email_body(attention_df)

st.subheader("📧 Email Body Preview")
st.code(email_body, language="markdown")

# ========================
# 5. Download Button
# ========================

st.download_button("📩 Download Email Text", data=email_body, file_name="demo_alert.txt")