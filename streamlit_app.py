import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# شعار سيمنس
st.image("https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300)

st.title("C-arm Demo Unit Tracker")

# بيانات الأجهزة
data = {
    "Model": ["Cios Alpha", "Cios Spin", "Cios Select", "Cios Fit", "Cios Fusion", "Cios Flow"],
    "Delivery Date": ["2025-07-01", "2025-07-03", "2025-07-10", "2025-07-15", "2025-07-18", "2025-07-21"],
    "Location": ["Riyadh", "Jeddah", "Warehouse", "Dammam", "Makkah", "Warehouse"],
    "Application Specialist": ["Ali", "Sara", "Ahmed", "Lama", "Omar", "Yasmin"],
    "Account Manager": ["Moath", "Ayman Tamimi", "Wesam", "Ammar", "Saleh", "Mohammad Al-Hamed"]
}

df = pd.DataFrame(data)

# عرض الجدول وتفعيله للتعديل
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)
grid_options = gb.build()

st.subheader("Editable Table")
grid_response = AgGrid(df, gridOptions=grid_options, editable=True, theme='streamlit')

# روابط الملفات
st.subheader("📎 Clickable Links")

for model in data["Model"]:
    name_key = model.lower().replace(" ", "_")
    brochure_url = f"https://example.com/brochure_{name_key}.pdf"
    config_url = f"https://example.com/config_{name_key}.pdf"
    st.markdown(f"**{model}** – [Brochure]({brochure_url}) | [Configuration]({config_url})")

# (لاحقًا) تنبيه مدير الحساب بزر
st.subheader("🔔 Alert System")
selected_model = st.selectbox("Select model to notify account manager:", data["Model"])
if st.button("Send Alert"):
    st.success(f"Alert sent to account manager of {selected_model} (mocked)")
