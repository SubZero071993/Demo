import streamlit as st

st.image("https://i.postimg.cc/vB9fTQSz/85-EEED00-2-AC8-4201-BDB1-9978-B32000-D9-removebg-preview.png", width=200)

st.set_page_config(layout="wide")
st.title("📎Documents ") 
devices = [
    {
        "Device": "Cios Connect",
        "Brochure": "https://smallpdf.com/file#s=a25c199b-1739-4745-a81a-e1725caba96c",
        "Configuration": "https://smallpdf.com/file#s=57bb6fa2-cba3-4971-bbce-0049462e9165",
        "Data Sheet": "https://smallpdf.com/file#s=57bb6fa2-cba3-4971-bbce-0049462e9165" 
    },
    {
        "Device": "Cios Fusion",
        "Brochure": "https://smallpdf.com/file#s=cec6d7a8-4b7a-47c5-bfa2-a098da63f422",
        "Configuration": "https://smallpdf.com/file#s=dfd03daa-a6f0-4ad7-84a9-235b585cbf38",
        "Data Sheet": "https://smallpdf.com/file#s=57bb6fa2-cba3-4971-bbce-0049462e9165" 
    },
    {
        "Device": "Cios Alpha VA30",
        "Brochure": "https://smallpdf.com/file#s=0371cf4c-e55e-48bb-82bb-ffd6aa2cf9d2",
        "Configuration": "https://smallpdf.com/file#s=b07cc63b-0327-4b5a-b2f6-59fc2ec66e2b",
        "Data Sheet": "https://smallpdf.com/file#s=57bb6fa2-cba3-4971-bbce-0049462e9165" 
    },
    {
        "Device": "Cios Spin",
        "Brochure": "https://smallpdf.com/file#s=3b4c2ced-54cb-48d4-8124-9e9f8beb5f15",
        "Configuration": "https://smallpdf.com/file#s=9a377c59-e004-4804-8d3c-6c8f2e53309d",
        "Data Sheet": "https://smallpdf.com/file#s=57bb6fa2-cba3-4971-bbce-0049462e9165" 
    }
]

import streamlit as st

icon_data = "📄"
icon_config = "🛠️"
icon_brochure = "📣"

for device in devices:
    st.markdown(f"### {device['Device']}")
    st.markdown(
        f"{icon_brochure} Brochure: [Click here]({device['Brochure']})  \n"
        f"{icon_config} Configuration: [Click here]({device['Configuration']}) <br> {icon_data} Data Sheet: [Click here]({device['Data Sheet']})",
        unsafe_allow_html=True  
    )
