import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import os

# ----------- Page Config -----------
st.set_page_config(layout="wide")

# ----------- Logo -----------
st.image("sh_logo_rgb.png", width=200)

st.markdown("<h1 style='color:#ff6600;'>C-arm Demo Unit Tracker</h1>", unsafe_allow_html=True)

# ----------- File Setup -----------
CSV_FILE = "demo_units.csv"
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Model", "Delivery Date", "Location", "App Specialist", "Account Manager", "Days in Location", "Issue"])
    df.to_csv(CSV_FILE, index=False)
else:
    df = pd.read_csv(CSV_FILE)

# ----------- Data Preprocessing -----------
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"])
today = pd.to_datetime(datetime.today().date())
df["Days in Location"] = (today - df["Delivery Date"]).dt.days
df["Issue"] = df["Issue"].fillna(False)

# ----------- Editable Table -----------
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Issue": st.column_config.CheckboxColumn("🔧 Device Issue", help="Check if the device has an issue"),
    }
)

# ----------- Save Changes -----------
edited_df.to_csv(CSV_FILE, index=False)

# ----------- Highlight Broken Devices -----------
def highlight_issues(row):
    if row["Issue"]:
        return ["background-color: #ffe6e6"] * len(row)
    else:
        return [""] * len(row)

styled_df = edited_df.style.apply(highlight_issues, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# ----------- Email Notification Section -----------
st.markdown("## 🔔 Send Email Notification")

for i, row in edited_df.iterrows():
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.write(f"Notify: {row['Model']}")
    with col2:
        if st.button("🔔", key=row["Model"]):
            st.success(f"📧 Email would be sent to {row['Account Manager']} (placeholder)")
            # Add actual email logic here if needed

# ----------- Brochure & Config Links -----------
st.markdown("---")
st.markdown("## 📎 Brochure & Configuration Links")

links = {
    "Cios Alpha": {
        "brochure": "https://example.com/alpha_brochure.pdf",
        "config": "https://example.com/alpha_config.pdf"
    },
    "Cios Spin": {
        "brochure": "https://example.com/spin_brochure.pdf",
        "config": "https://example.com/spin_config.pdf"
    },
    "Cios Select": {
        "brochure": "https://example.com/select_brochure.pdf",
        "config": "https://example.com/select_config.pdf"
    },
    "Cios Fit": {
        "brochure": "https://example.com/fit_brochure.pdf",
        "config": "https://pdf.ac/3u7Xrl"
    },
    "Cios Fusion": {
        "brochure": "https://example.com/fusion_brochure.pdf",
        "config": "https://example.com/fusion_config.pdf"
    },
    "Cios Flow": {
        "brochure": "https://example.com/flow_brochure.pdf",
        "config": "https://example.com/flow_config.pdf"
    },
}

for model, files in links.items():
    st.markdown(f"**{model}** – 📄 [Brochure]({files['brochure']}) | 🛠 [Config]({files['config']})")

# Optional: Hide streamlit style
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
