import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

st.set_page_config(layout="wide")
st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300)

st.title("C-arm Demo Tracking System")
st.markdown("### قائمة الأجهزة التجريبية في المملكة")

# جعل الجدول قابل للتعديل
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Account Manager": st.column_config.SelectboxColumn("Account Manager", options=account_managers),
        "Device Status (Broken?)": st.column_config.CheckboxColumn("Broken?"),
    }
)

# بيانات الأجهزة
data = [
    ["Cios Select FD VA20", "22-07-25", 20087, "warehouse", "", "", "", ""],
    ["Cios Connect", "25-05-25", 21521, "Al-Rawdhah Hospital (until we submit Cios Select)", "Ayman Tamimi", "", "", ""],
    ["Cios Fusion", "27-07-25", 31181, "warehouse", "", "", "", ""],
    ["Cios Alpha VA20", "29-05-25", 13020, "Al-Hayyat Hospital (until they receive their C-arm)", "Ammar", "", "", ""],
    ["Cios Alpha VA30", "03-07-25", 43815, "Aster Sanad Hospital", "Ammar", "", "", ""],
    ["Cios Spin VA30", "10-07-25", 50097, "Johns Hopkins Aramco Hospital", "Ayman Tamimi", "Ali", "", ""]
]

account_managers = [
    "Ayman Ghandurah", "Ayman Tamimi", "Moath", "Wesam", "Najla", "Mohammad Al-Hamed",
    "Mohammad Gharabieh", "Tuqa", "Ammar", "Saleh", "Mohammad Al-Mutairi", "Iqbal"
]

df = pd.DataFrame(data, columns=[
    "Demo C-arm Model", "Delivery Date", "Serial #", "Current Location",
    "Account Manager", "Application Specialist", "Device Status (Broken?)", "Brochure Link"
])


# تحويل التاريخ إلى datetime
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], format="%d-%m-%y")
today = datetime(2025, 7, 27)
df["Days in Site"] = (today - df["Delivery Date"]).dt.days

def row_style(row):
    if row["Current Location"].lower() == "warehouse":
        return "background-color: lightgreen"
    elif row["Device Status (Broken?)"]:
        return "background-color: lightgray"
    elif row["Days in Site"] > 14:
        return "background-color: yellow"
    return ""

# تطبيق التنسيقات الشرطية
styled_df = edited_df.style.apply(lambda row: [row_style(row)]*len(row), axis=1)
st.dataframe(styled_df, use_container_width=True)

st.markdown("### 🔗 روابط البروشور والكونفيقريشن لكل جهاز")
for i, row in edited_df.iterrows():
    st.markdown(f"**{row['Demo C-arm Model']} ({row['Serial #']})**")
    brochure = row["Brochure Link"] if row["Brochure Link"] else "No link provided."
    st.markdown(f"- [📄 Brochure]({brochure})")
    st.markdown("---")

st.markdown("### ✉️ إرسال تنبيه لمدير الحساب")

selected_device = st.selectbox("اختر الجهاز", edited_df["Demo C-arm Model"] + " | Serial: " + edited_df["Serial #"].astype(str))
if st.button("إرسال تنبيه"):
    # نص الإشعار
    msg = MIMEText(f"تم تجاوز 14 يومًا للجهاز: {selected_device}. نرجو المتابعة.")
    msg["Subject"] = "تنبيه بخصوص جهاز تجريبي"
    msg["From"] = "your_email@domain.com"
    msg["To"] = "manager_email@domain.com"  # حط الإيميل الصحيح هنا

    # إرسال (هذا الجزء لا يعمل إلا في بيئة حقيقية مع SMTP)
    try:
        with smtplib.SMTP("smtp.domain.com", 587) as server:
            server.starttls()
            server.login("your_email@domain.com", "your_password")
            server.send_message(msg)
        st.success("تم إرسال الإشعار بنجاح.")
    except Exception as e:
        st.error(f"فشل إرسال الإيميل: {e}")
