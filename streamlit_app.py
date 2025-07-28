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
        "Brochure": "https://example.com/cios_connect_brochure.pdf",
        "Configuration": "https://example.com/cios_connect_config.pdf"
    },
    {
        "Device": "Cios Fusion",
        "Brochure": "https://example.com/cios_fusion_brochure.pdf",
        "Configuration": "https://example.com/cios_fusion_config.pdf"
    },
    {
        "Device": "Cios Alpha VA30",
        "Brochure": "https://example.com/cios_alpha_va30_brochure.pdf",
        "Configuration": "https://example.com/cios_alpha_va30_config.pdf"
    },
    {
        "Device": "Cios Spin",
        "Brochure": "https://example.com/cios_spin_brochure.pdf",
        "Configuration": "https://example.com/cios_spin_config.pdf"
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
                
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# إعداد معلومات SMTP من Brevo
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = "934e56001@smtp-brevo.com"
SMTP_PASSWORD = "Lf9sCKyvh7ImpJcO"  # هذا هو Master Password

# بيانات الإيميل
sender_email = SMTP_USERNAME
receiver_email = "hossam.al-zahrani@siemens-healthineers.com"
subject = "🔔 C-arm Device Notification"
body = "Hello Hossam,\n\nThis is a test email from your Streamlit app.\n\nRegards,\nStreamlit Bot"

# واجهة المستخدم
st.set_page_config(layout="centered")
st.title("📧 Send Test Notification")

if st.button("Send Email"):
    try:
        # تجهيز الإيميل
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # الاتصال بالسيرفر وإرسال الإيميل
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        st.success("✅ Email sent successfully!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
