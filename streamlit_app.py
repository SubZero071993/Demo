import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

st.set_page_config(layout="wide")

# شعار
st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300)
st.title("C-arm Demo Unit Tracker")

# بيانات
data = [
    {"Model": "Cios Alpha", "Delivery Date": "2025-07-01", "Location": "Riyadh", "App Specialist": "Ali", "Account Manager": "Moath"},
    {"Model": "Cios Spin", "Delivery Date": "2025-07-03", "Location": "Jeddah", "App Specialist": "Sara", "Account Manager": "Ayman Tamimi"},
    {"Model": "Cios Select", "Delivery Date": "2025-07-10", "Location": "Warehouse", "App Specialist": "Ahmed", "Account Manager": "Wesam"},
    {"Model": "Cios Fit", "Delivery Date": "2025-07-15", "Location": "Dammam", "App Specialist": "Lama", "Account Manager": "Ammar"},
    {"Model": "Cios Fusion", "Delivery Date": "2025-07-18", "Location": "Makkah", "App Specialist": "Omar", "Account Manager": "Saleh"},
    {"Model": "Cios Flow", "Delivery Date": "2025-07-21", "Location": "Warehouse", "App Specialist": "Yasmin", "Account Manager": "Mohammad Al-Hamed"},
]

# الإيميلات المرتبطة بمدراء الحسابات
emails = {
    "Moath": "moath@example.com",
    "Ayman Tamimi": "ayman@example.com",
    "Wesam": "wesam@example.com",
    "Ammar": "ammar@example.com",
    "Saleh": "saleh@example.com",
    "Mohammad Al-Hamed": "mohammad@example.com"
}

# حساب عدد الأيام (باستثناء Warehouse)
today = datetime.today()
for row in data:
    delivery_date = datetime.strptime(row["Delivery Date"], "%Y-%m-%d")
    days = (today - delivery_date).days
    row["Days in Location"] = days if row["Location"].lower() != "warehouse" else 0

# تحويل لقائمة قابلة للتعديل
df = pd.DataFrame(data)
managers = list(emails.keys())

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)
gb.configure_column("Account Manager", editable=True, cellEditor='agSelectCellEditor', cellEditorParams={'values': managers})
grid = AgGrid(df, gridOptions=gb.build(), update_mode="MODEL_CHANGED", height=400)

# إشعار بالإيميل
st.subheader("Send Email Notification")

for i, row in grid["data"].iterrows():
    with st.expander(f"Notify: {row['Model']}"):
        if st.button(f"Send Alert to {row['Account Manager']}", key=f"btn_{i}"):
            manager = row['Account Manager']
            email = emails.get(manager)
            if email:
                msg = MIMEText(f"""Dear {manager},

This is an automatic notification regarding the demo unit: {row['Model']} currently located in {row['Location']} since {row['Delivery Date']}.

Please take necessary actions if needed.

Regards,
C-arm Tracking System
""")
                msg['Subject'] = f"Demo Unit Alert: {row['Model']}"
                msg['From'] = "demo-tracker@yourdomain.com"
                msg['To'] = email

                try:
                    # هنا ممكن تغير الإعدادات لو عندك SMTP فعّال
                    smtp = smtplib.SMTP("your.smtp.server", 587)
                    smtp.starttls()
                    smtp.login("your_username", "your_password")
                    smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
                    smtp.quit()
                    st.success(f"Email sent to {manager}")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")
            else:
                st.warning("No email found for this account manager.")

# روابط البروشور والكونفيق
st.subheader("📎 Clickable Links")
for model in df["Model"]:
    st.markdown(f"- **{model}** – [Brochure](https://example.com/{model.replace(' ', '_')}_brochure.pdf) | [Configuration](https://example.com/{model.replace(' ', '_')}_config.pdf)")

