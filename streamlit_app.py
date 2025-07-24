import streamlit as st
import pandas as pd
from datetime import datetime, date
import smtplib
from email.mime.text import MIMEText
import base64

st.set_page_config(layout="wide")

# شعار سيمنس
st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=200)

st.title("C-arm Demo Tracker - Siemens Healthineers")

# البيانات الأساسية
data = {
    "Demo C-arm Model": [
        "Cios Select FD VA20", "Cios Connect", "Cios Fusion",
        "Cios Alpha VA20", "Cios Alpha VA30", "Cios Spin VA30"
    ],
    "Delivery Date": [
        "22-07-25", "25-06-25", "25-05-25",
        "30-05-25", "19-06-25", "10-07-25"
    ],
    "Serial #": [
        20087, 21181, 21581,
        13002, 13095, 50097
    ],
    "Current Location": [
        "warehouse", "Al-Rawdah Hospital (until we submit Cios Select)", "Al-Salam Health Hospital",
        "Al-Hayat Hospital (until they receive their c-arm)", "Aster Sanad Hospital", "Johns Hopkins Aramco Hospital"
    ],
    "Account Manager": [
        "Ayman Tamimi", "Mohammad Ghariebh", "Mohammad Ghariebh",
        "Ammar", "Ammar", "Ayman Tamimi"
    ],
    "Application Specialist": [
        "", "", "Ali",
        "", "", "Ali"
    ],
    "Device Faulty (🔧)": [
        False, False, False,
        False, False, False
    ]
}

# تحويل التاريخ وحساب عدد الأيام
df = pd.DataFrame(data)
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], format="%d-%m-%y")
today = pd.to_datetime(date.today())

def calculate_days(row):
    if row["Current Location"].strip().lower() == "warehouse":
        return 0
    return (today - row["Delivery Date"]).days

df["Days in Location"] = df.apply(calculate_days, axis=1)

# روابط البروشور والكونفيقريشن
brochure_links = {
    "Cios Select FD VA20": ("https://example.com/select_brochure", "https://example.com/select_config"),
    "Cios Connect": ("https://example.com/connect_brochure", "https://example.com/connect_config"),
    "Cios Fusion": ("https://example.com/fusion_brochure", "https://example.com/fusion_config"),
    "Cios Alpha VA20": ("https://example.com/alpha20_brochure", "https://example.com/alpha20_config"),
    "Cios Alpha VA30": ("https://example.com/alpha30_brochure", "https://example.com/alpha30_config"),
    "Cios Spin VA30": ("https://example.com/spin_brochure", "https://example.com/spin_config")
}

# حفظ التعديلات في سيشن
if "df" not in st.session_state:
    st.session_state.df = df

edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    use_container_width=True,
    key="editable_table"
)

# تظليل الصف إذا فيه عطل
def style_row(row):
    if row["Device Faulty (🔧)"]:
        return ["background-color: #ffe6e6"] * len(row)
    else:
        return [""] * len(row)

st.markdown("### 🔧 Brochure & Configuration Links")
for model in df["Demo C-arm Model"]:
    brochure, config = brochure_links.get(model, ("#", "#"))
    st.markdown(f"- **{model}** — [📄 Brochure]({brochure}) | [🛠 Config]({config})")

# زر إرسال إيميل تنبيه
st.markdown("---")
st.markdown("### 📬 Send Email Notification to Account Managers")

for i, row in edited_df.iterrows():
    if row["Days in Location"] > 14 and row["Current Location"].strip().lower() != "warehouse":
        if st.button(f"Send Reminder to {row['Account Manager']}", key=f"email_{i}"):
            # إعداد الإيميل (إيميل وهمي للتجربة، غيّره لاحقًا)
            sender_email = "demo@example.com"
            recipient_email = f"{row['Account Manager'].replace(' ', '').lower()}@example.com"
            subject = f"Reminder: {row['Demo C-arm Model']} device has exceeded 14 days"
            body = f"""Dear {row['Account Manager']},

The demo unit **{row['Demo C-arm Model']}** (Serial: {row['Serial #']}) has been in location "**{row['Current Location']}**" for **{row['Days in Location']}** days.

Please take the necessary action as per the demo policy.

Best regards, 
C-arm Demo Tracker – Siemens Healthineers
"""
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = recipient_email

            try:
                with smtplib.SMTP("smtp.office365.com", 587) as server:
                    server.starttls()
                    server.login("demo@example.com", "your_password_here")  # احذف لاحقًا
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                st.success(f"Email sent to {recipient_email}")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
