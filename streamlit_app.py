import streamlit as st
import pandas as pd
from datetime import datetime

#Logo
st.image( "https://upload.wikimedia.org/wikipedia/commons/7/79/Siemens_Healthineers_logo.svg", width=300 )


# Data
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

df = pd.DataFrame(data, columns=columns)
df["Delivery Date"] = pd.to_datetime(df["Delivery Date"], format="%d-%m-%y").dt.date

today = datetime(2025, 7, 27).date()
df["Days in Site"] = df.apply(
    lambda row: (today - row["Delivery Date"]).days 
    if row["Current Location"].strip().lower() != "warehouse" else "",
    axis=1
)
df["Is Broken?"] = False

st.set_page_config(layout="wide")
st.title("📋C-Arm Demo (CAD)")

# Editable schedule
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Is Broken?": st.column_config.CheckboxColumn("Is Broken?"),
    }
)

# Generate background color for each row
def get_row_bg(row):
    if row["Is Broken?"]:
        return "background-color: #dddddd;"  # light-grey
    elif row["Days in Site"] != "" and row["Days in Site"] > 14 and row["Current Location"].strip().lower() != "warehouse":
        return "background-color: #fff9c4;"  # yellow
    else:
        return ""

# Display table with color cues (as emoji or color boxes for visibility)
def display_colored_schedule(df):
    st.markdown("### Schedule")
    for idx, row in df.iterrows():
        style = get_row_bg(row)
        # You can display a colored box or emoji for visual cue
        color_box = ""
        if style:
            if "#dddddd" in style:
                color_box = "⬜️"
            elif "#fff9c4" in style:
                color_box = "🟨"
        st.markdown(
            f"{color_box} **{row['Demo C-arm Model']}** | Delivery: {row['Delivery Date']} | Serial: {row['Serial #']} | Location: {row['Current Location']} | Days in Site: {row['Days in Site']} | Broken: {row['Is Broken?']}"
        )

# Show colored schedule summary below editable table
display_colored_schedule(edited_df)

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
                
