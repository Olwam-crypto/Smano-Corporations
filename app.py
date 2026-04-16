# pip install streamlit web3 streamlit-js-eval
import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title=config.APP_NAME, layout="wide")

# --- HEADER SECTION (LOGO REMOVED) ---
st.title(f"🏢 {config.APP_NAME}")
st.caption(f"**{config.TAGLINE}**")
st.markdown(config.DESCRIPTION)
st.divider()

# --- BLOCKCHAIN CONNECTION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(
    address=w3.to_checksum_address(config.CONTRACT_ADDRESS), 
    abi=config.CONTRACT_ABI
)

# --- SIDEBAR NAVIGATION ---
pages = [
    "Overview", 
    "Full About SMANO", 
    "Donation Portal", 
    "Supplier Management", 
    "Logistics & Tracking", 
    "Admin", 
    "Subscribe (R60)"
]
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
    except Exception:
        st.warning("Please connect MetaMask to see live blockchain metrics.")

# ==========================================
# PAGE: FULL ABOUT SMANO
# ==========================================
elif selection == "Full About SMANO":
    st.subheader("Mission & Transparency")
    st.write(config.ABOUT_MISSION)
    
    st.info(f"**The SMANO Solution:** {config.ABOUT_SOLUTION}")
    
    st.markdown("### Ecosystem Roles")
    for role, desc in config.ABOUT_ROLES.items():
        st.write(f"**{role}:** {desc}")

# ==========================================
# PAGE: DONATION PORTAL
# ==========================================
elif selection == "Donation Portal":
    st.subheader("Secure Donation Portal")
    st.write("Donors must be registered with CSR to contribute.")
    
    with st.expander("Terms and Conditions", expanded=False):
        st.write("Agreeing to terms after downloading the app is compulsory.")
        agreed = st.checkbox("I agree to the SMANO Terms and Conditions")

    amount = st.number_input("Amount to Donate (ETH)", min_value=0.01, step=0.01)
    
    if amount > 0:
        fee = amount * config.SERVICE_FEE_RATE
        net_amount = amount - fee
        st.write(f"Gross Donation: {amount} ETH")
        st.write(f"10% Service Fee: {fee:.4f} ETH")
        st.success(f"Net funds allocated to schools: {net_amount:.4f} ETH")

    if st.button("Donate Now"):
        if not agreed:
            st.error("You must agree to the Terms and Conditions first.")
        else:
            st.info("Checking CSR Registration Status... Please check MetaMask.")

# ==========================================
# PAGE: LOGISTICS & TRACKING
# ==========================================
elif selection == "Logistics & Tracking":
    st.subheader("Real-Time Supply Chain Tracking")
    st.write("Ensuring products move from verified suppliers to schools in need.")
    
    batch_id = st.number_input("Enter Batch ID to Track", min_value=0, step=1)
    
    if st.button("Track Progress"):
        # This reflects the lifecycle states from your document
        st.markdown("### Current Status Flow")
        st.info("Status: Processing Order...")
        # Note: In production, this pulls directly from contract.functions.batches(batch_id)

# ==========================================
# PAGE: SUBSCRIBE (R60)
# ==========================================
elif selection == "Subscribe (R60)":
    st.subheader("Support SMANO")
    st.markdown(f"## R{config.SUBSCRIPTION_FEE_ZAR} per month")
    st.write("Maintaining a decentralized ledger for school transparency.")
    
    if st.button("Subscribe"):
        st.balloons()
        st.success("Redirecting to payment gateway. Thank you for your support!")
