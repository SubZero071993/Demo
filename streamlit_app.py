import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO

# --- تحميل البيانات الأساسية ---
data = {
    "Demo C-arm Model": [
        "Cios Select FD VA20", "Cios Connect", "Cios Fusion",
        "Cios Alpha VA20", "Cios Alpha VA30", "Cios Spin VA30"
    ],
    "Delivery Date": [
        "22-07-25", "25-05-25", "26-05-25",
        "13-06-25", "20-07-25", "10-07-25"
    ],
    "Serial #": [
        300087, 21581, 21584, 13002, 13222, 50097
    ],
    "Current Location": [
        "warehouse", "Al-Rawdah Hospital (until we submit Cios Select)",
        "Al-Salam Health Hospital", "Al-Hayyat Hospital (until they receive their C-arm)",
        "Aster Sanad Hospital", "Johns Hopkins Aramco Hospital"
    ],
    "Account Manager": [
        "Ayman Tamimi", "Mohammad Ghariebh", "Mohammad Ghariebh",
        "Ammar", "Ammar", "Ayman Tamimi"
    ],
    "Application Specialist": [
        "", "", "Ali", "", "", "Ali"
    ],
    "Device Fault": [
        False, False, False, False, False, False
    ]
}

df = pd.DataFrame(data)
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], format="%d-%m-%y")

# --- حساب الأيام في الموقع (مع استثناء المستودع) ---
today = pd.to_datetime(datetime.today().date())
df["Days in Location"] = df.apply(
    lambda row: (today - row["Delivery Date"]).days if "warehouse" not in row["Current Location"].lower() else 0,
    axis=1
)

# --- إعداد الصفحة ---
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- شعار سيمنس ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Siemens_Healthineers_logo.svg/2560px-Siemens_Healthineers_logo.svg.png", width=300)

st.title("C-arm Device Tracker")

# --- عرض وتعديل الجدول ---
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Account Manager": st.column_config.SelectboxColumn(
            "Account Manager",
            help="Choose the AM",
            options=df["Account Manager"].unique().tolist()
        ),
        "Device Fault": st.column_config.CheckboxColumn("🔧 Fault")
    },
    hide_index=True,
    key="carm_editor"
)

# --- تظليل الصف إذا فيه عطل ---
def highlight_fault(row):
    if row["Device Fault"]:
        return ["background-color: #ffe6e6"] * len(row)
    return [""] * len(row)

st.dataframe(
    edited_df.style.apply(highlight_fault, axis=1),
    use_container_width=True
)

# --- روابط البروشور والكونفقريشن ---
st.subheader("📎 Brochure & Configuration Links")
links = {
    "Cios Alpha": ["https://example.com/brochure_alpha.pdf", "https://example.com/config_alpha.pdf"],
    "Cios Spin": ["https://example.com/brochure_spin.pdf", "https://example.com/config_spin.pdf"],
    "Cios Select": ["https://example.com/brochure_select.pdf", "https://example.com/config_select.pdf"],
    "Cios Fit": ["https://example.com/brochure_fit.pdf", "https://example.com/config_fit.pdf"],
    "Cios Fusion": ["https://example.com/brochure_fusion.pdf", "https://example.com/config_fusion.pdf"],
    "Cios Connect": ["https://example.com/brochure_connect.pdf", "https://example.com/config_connect.pdf"],
}

for model, (brochure, config) in links.items():
    st.markdown(f"**{model}** – [📄 Brochure]({brochure}) | [🛠️ Config]({config})")

# --- إرسال إشعار عبر البريد إذا تجاوز الجهاز أسبوعين ---
import smtplib
from email.mime.text import MIMEText

st.subheader("📬 Send Notification for Devices > 14 Days (excluding warehouse)")

for index, row in edited_df.iterrows():
    if row["Days in Location"] > 14 and "warehouse" not in row["Current Location"].lower():
        if st.button(f"Notify {row['Account Manager']} about {row['Demo C-arm Model']}", key=index):
            recipient = "fake.email@siemens-healthineers.com"  # ← غيّرها لإيميل مدير الحساب
            subject = f"Device {row['Demo C-arm Model']} has been at {row['Current Location']} for over 14 days"
            body = f"""Dear {row['Account Manager']},

This is an automated reminder that the C-arm device **{row['Demo C-arm Model']}** (Serial: {row['Serial #']}) has been at **{row['Current Location']}** for **{row['Days in Location']} days**.

Please take the necessary action.

Best regards,
Demo Tracking System"""

            try:
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = "demo-tracker@yourdomain.com"
                msg["To"] = recipient

                smtp_server = "smtp.yourdomain.com"  # ← غيّر هذا بناءً على نظام شركتك
                smtp_port = 587
                smtp_user = "demo-tracker@yourdomain.com"
                smtp_password = "yourpassword"  # مو مطلوب حالياً

                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)

                st.success(f"Notification sent to {recipient}")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
