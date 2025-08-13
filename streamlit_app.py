import streamlit as st

# Page configuration

st.set_page_config(
page_title=“Demo Device Request”,
page_icon=“🏥”,
layout=“centered”
)

# Custom CSS for styling

st.markdown(”””

<style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        padding: 20px 0;
        border-bottom: 3px solid #4a90e2;
        margin-bottom: 30px;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    .required-field {
        color: red;
        font-weight: bold;
    }
    .section-divider {
        margin: 30px 0;
        border-top: 1px solid #e0e0e0;
        padding-top: 20px;
    }
</style>

“””, unsafe_allow_html=True)

# Initialize session state

if ‘form_submitted’ not in st.session_state:
st.session_state.form_submitted = False

if ‘form_data’ not in st.session_state:
st.session_state.form_data = {}

def reset_form():
st.session_state.form_submitted = False
st.session_state.form_data = {}
# Clear all form inputs
for key in st.session_state:
if key.startswith(‘device_’) or key.startswith(‘request_’) or key.startswith(‘urgent_’):
del st.session_state[key]
st.rerun()

# Main header

st.markdown(’<h1 class="main-header">🏥 Demo Device Request Form</h1>’, unsafe_allow_html=True)

if not st.session_state.form_submitted:
st.markdown(“Please fill out all required fields to submit your demo device request.”)

```
# Device Type Selection
st.markdown("### Device Type <span class='required-field'>*</span>", unsafe_allow_html=True)
device_type = st.selectbox(
    "Select device type:",
    options=["", "Ultrasound", "X-Ray", "C-Arm"],
    key="device_type",
    help="Choose the type of medical device you need for demo"
)

# Device Model Selection (conditional)
device_model = ""
if device_type:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Device Model <span class='required-field'>*</span>", unsafe_allow_html=True)
   
    if device_type == "Ultrasound":
        device_model = st.selectbox(
            "Select ultrasound model:",
            options=["", "Ultrasound Device"],
            key="device_model"
        )
    elif device_type == "X-Ray":
        device_model = st.selectbox(
            "Select X-Ray model:",
            options=["", "X-Ray Device"],
            key="device_model"
        )
    elif device_type == "C-Arm":
        device_model = st.selectbox(
            "Select C-Arm model:",
            options=["", "Cios Connect", "Cios Fusion", "Cios Alpha VA30", "Cios Spin"],
            key="device_model"
        )

# Request Reason
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("### Request Reason <span class='required-field'>*</span>", unsafe_allow_html=True)
request_reason = st.selectbox(
    "Why are you requesting this demo?",
    options=["", "Possible PO", "Demo", "Support"],
    key="request_reason",
    help="Select the primary reason for your demo request"
)

# Urgent Request
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("### Urgent Request <span class='required-field'>*</span>", unsafe_allow_html=True)
is_urgent = st.radio(
    "Is this request urgent?",
    options=["No", "Yes"],
    key="is_urgent",
    help="Select Yes if you need this demo urgently"
)

# Urgent Justification (conditional)
urgent_justification = ""
if is_urgent == "Yes":
    st.markdown("### Urgent Justification <span class='required-field'>*</span>", unsafe_allow_html=True)
    urgent_justification = st.text_area(
        "Please explain why this request is urgent:",
        key="urgent_justification",
        help="Provide detailed justification for the urgent request",
        placeholder="Enter the reason for urgency..."
    )

# Submit button
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Submit Request", use_container_width=True, type="primary"):
        # Validation
        errors = []
       
        if not device_type:
            errors.append("Device type is required")
        if not device_model:
            errors.append("Device model is required")
        if not request_reason:
            errors.append("Request reason is required")
        if not is_urgent:
            errors.append("Please specify if the request is urgent")
        if is_urgent == "Yes" and not urgent_justification.strip():
            errors.append("Urgent justification is required when request is urgent")
       
        if errors:
            st.error("Please fix the following errors:")
            for error in errors:
                st.error(f"• {error}")
        else:
            # Save form data and mark as submitted
            st.session_state.form_data = {
                'device_type': device_type,
                'device_model': device_model,
                'request_reason': request_reason,
                'is_urgent': is_urgent,
                'urgent_justification': urgent_justification if is_urgent == "Yes" else ""
            }
            st.session_state.form_submitted = True
            st.rerun()
```

else:
# Success page
st.markdown(”””
<div class="success-message">
<h2>✅ Request Submitted Successfully!</h2>
<p>Your demo device request has been received and will be processed shortly.</p>
</div>
“””, unsafe_allow_html=True)

```
# Display submitted data
st.markdown("### 📋 Request Details:")

col1, col2 = st.columns(2)

with col1:
    st.info(f"**Device Type:** {st.session_state.form_data['device_type']}")
    st.info(f"**Device Model:** {st.session_state.form_data['device_model']}")

with col2:
    st.info(f"**Request Reason:** {st.session_state.form_data['request_reason']}")
    st.info(f"**Urgent Request:** {st.session_state.form_data['is_urgent']}")

if st.session_state.form_data['urgent_justification']:
    st.warning(f"**Urgent Justification:** {st.session_state.form_data['urgent_justification']}")

# New request button
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📝 Submit New Request", use_container_width=True, type="secondary"):
        reset_form()
```

# Footer

st.markdown(”—”)
st.markdown(
“<div style='text-align: center; color: #666; padding: 20px;'>”
“Demo Device Request System | Medical Equipment Management”
“</div>”,
unsafe_allow_html=True
)
