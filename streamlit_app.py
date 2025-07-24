import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# إعداد الصفحة
st.set_page_config(layout="wide")
st.image("https://upload.wikimedia.org/wikipedia/commons/4/44/Siemens_Healthineers_logo.svg", width=200)
st.title("C-arm Demo Unit Tracker")

# قائمة مدراء الحساب والإيميلات
account_managers = {
    "Ayman Tamimi": "ayman.tamimi@example.com",
    "Wesam": "wesam@example.com",
    "Ammar": "ammar@example.com",
    "Saleh": "saleh@example.com",
    "Mohammad Al-Hamed": "mohammad.alhamed@example.com",
    "Moath": "moath@example.com"
}

# البيانات
data = [
    {"Model": "Cios Alpha", "Delivery Date": "2025-07-01", "Location": "Riyadh", "App Specialist": "Ali", "Account Manager": "Ayman Tamimi"},
    {"Model": "Cios Spin", "Delivery Date": "2025-07-03", "Location": "Jeddah", "App Specialist": "Sara", "Account Manager": "Ayman Tamimi"},
    {"Model": "Cios Select", "Delivery Date": "2025-07-10", "Location": "Warehouse", "App Specialist": "Ahmed", "Account Manager": "Wesam"},
    {"Model": "Cios Fit", "Delivery Date": "2025-07-15", "Location": "Dammam", "App Specialist": "Lama", "Account Manager": "Ammar"},
    {"Model": "Cios Fusion", "Delivery Date": "2025-07-18", "Location": "Makkah", "App Specialist": "Omar", "Account Manager": "Saleh"},
    {"Model": "Cios Flow", "Delivery Date": "2025-07-21", "Location": "Warehouse", "App Specialist": "Yasmin", "Account Manager": "Mohammad Al-Hamed"},
]

df = pd.DataFrame(data)
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"])
today = pd.to_datetime(datetime.today().date())

# حساب الأيام باستثناء "Warehouse"
df["Days in Location"] = df.apply(
    lambda row: (today - row["Delivery Date"]).days if row["Location"].lower() != "warehouse" else 0,
    axis=1
)

# إعداد خيارات الجدول
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("Account Manager", editable=True, cellEditor='agSelectCellEditor',
                    cellEditorParams={'values': list(account_managers.keys())})
gb.configure_column("Days in Location", editable=False)
gb.configure_grid_options(domLayout='normal')
grid_options = gb.build()

# عرض الجدول
st.subheader("📋 Device Table (Editable)")
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=True,
    height=600
)
updated_df = pd.DataFrame(grid_response["data"])

# روابط البروشور والكونفيقريشن
st.subheader("📎 Brochure & Configuration Links")
for model in updated_df["Model"]:
    model_clean = model.replace(" ", "").lower()
    brochure_url = f"https://example.com/brochures/{model_clean}.pdf"
    config_url = f"https://example.com/configs/{model_clean}.pdf"
    st.markdown(f"**{model}** – [📄 Brochure]({brochure_url}) | [🛠️ Config]({config_url})", unsafe_allow_html=True)

# دالة إرسال إيميل بدون باسورد (SMTP بدون توثيق)
def send_email_no_auth(receiver_email, subject, body):
    sender_email = "demo-tracker@yourcompany.com"  # حطه وهمي أو إيميل عام للشركة

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("hossam.al-zahrani@siemens-healthineers.com", 25) as server:  # عدّل حسب السيرفر الداخلي
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
        return False

# أزرار التنبيه
st.subheader("🔔 Notify Account Managers")

for idx, row in updated_df.iterrows():
    model = row["Model"]
    manager = row["Account Manager"]
    email = account_managers.get(manager)
    days = row["Days in Location"]
    location = row["Location"]

    if st.button(f"🔔 Notify: {model}"):
        if not email:
            st.warning(f"No email found for {manager}")
        else:
            subject = f"🔔 Reminder: {model} has been in {location} for {days} days"
            body = f"""Dear {manager},

This is an automated notification regarding the demo unit:

Model: {model}
Location: {location}
Days in Location: {days}

Please take appropriate action if needed.

Best regards,
Hossam
"""
            success = send_email_no_auth(email, subject, body)
            if success:
                st.success(f"✅ Email sent to {manager} at {email}")

