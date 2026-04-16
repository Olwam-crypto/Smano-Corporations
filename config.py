# pip install streamlit web3 streamlit-js-eval
import streamlit as st
import base64
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config

# --- LOGO DATA ---
# Paste your logo's Base64 string here
LOGO_B64 = "YOUR_LOGO_BASE64_STRING_HERE"

st.set_page_config(page_title=config.APP_NAME, layout="wide")

# Header Logic
if LOGO_B64 != "YOUR_LOGO_BASE64_STRING_HERE":
    st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{LOGO_B64}" width="200"></div>', unsafe_allow_html=True)
else:
    st.title(config.APP_NAME)
st.caption(f"**{config.TAGLINE}**")
st.divider()

# Blockchain Connection
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=w3.to_checksum_address(config.CONTRACT_ADDRESS), abi=config.CONTRACT_ABI)
user_address_js = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")

# Sidebar Navigation
pages = ["Overview", "Full About SMANO", "Donation Portal", "Supplier Management", "Logistics & Tracking", "Admin", "Subscribe (R60)"]
selection = st.sidebar.radio("Go to", pages)

# ==========================================
# PAGE: OVERVIEW
# ==========================================
if selection == "Overview":
    st.subheader("Platform Status")
    col1, col2, col3 = st.columns(3)
    
    try:
        batch_count = contract.functions.batchCount().call()
        col1.metric("Total Batches", batch_count)
        col2.metric("Service Fee", f"{int(config.SERVICE_FEE_RATE * 100)}%")
        col3.metric("Network", "Sepolia Testnet")
    except:
        st.warning("Connect to MetaMask to view live metrics.")

# ==========================================
# PAGE: FULL ABOUT SMANO
# ==========================================
elif selection == "Full About SMANO":
    st.subheader("Mission & Transparency") [cite: 7, 8]
    st.write(config.ABOUT_MISSION) [cite: 3, 4]
    
    st.info(f"**The SMANO Solution:** {config.ABOUT_SOLUTION}") [cite: 7, 10]
    
    st.markdown("### Ecosystem Roles") [cite: 13]
    for role, desc in config.ABOUT_ROLES.items():
        st.write(f"**{role}:** {desc}") [cite: 14, 15, 17, 18, 20]

# ==========================================
# PAGE: DONATION PORTAL
# ==========================================
elif selection == "Donation Portal":
    st.subheader("Secure Donation Portal")
    st.write("Donors must be registered with CSR to contribute.") [cite: 34]
    
    with st.expander("Terms and Conditions", expanded=False):
        st.write("Agreeing to terms after downloading the app is compulsory.") [cite: 35]
        agreed = st.checkbox("I agree to the SMANO Terms and Conditions")

    amount = st.number_input("Amount to Donate (ETH)", min_value=0.01, step=0.01)
    
    if amount > 0:
        fee = amount * config.SERVICE_FEE_RATE
        net_amount = amount - fee
        st.write(f"Gross Donation: {amount} ETH")
        st.write(f"10% Service Fee: {fee:.4f} ETH") [cite: 34, 39]
        st.success(f"Net funds allocated to schools: {net_amount:.4f} ETH") [cite: 9]

    if st.button("Donate Now"):
        if not agreed:
            st.error("You must agree to the Terms and Conditions first.")
        else:
            st.info("Initiating transaction... Please check MetaMask.")

# ==========================================
# PAGE: LOGISTICS & TRACKING
# ==========================================
elif selection == "Logistics & Tracking":
    st.subheader("Real-Time Supply Chain Tracking") [cite: 40]
    st.write("Follow the lifecycle of learning materials and food.") [cite: 23]
    
    batch_id = st.number_input("Enter Batch ID to Track", min_value=0, step=1)
    
    if st.button("Track Progress"):
        # This simulates the Lifecycle states from the document
        st.markdown("### Current Status")
        st.steps([
            "Order Received",
            "At Supplier",
            "In Transit",
            "Delivered",
            "Quality Inspection"
        ]) [cite: 23, 25]

# ==========================================
# PAGE: SUBSCRIBE (R60)
# ==========================================
elif selection == "Subscribe (R60)":
    st.subheader("Support SMANO")
    st.markdown(f"## R{config.SUBSCRIPTION_FEE_ZAR} per month")
    st.write("Help us expand our reach to more schools in need.") [cite: 37]
    
    if st.button("Subscribe"):
        st.balloons()
        st.success("Thank you for supporting educational transparency!")
