import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title=config.APP_NAME, layout="wide")

# --- 2. SETUP BLOCKCHAIN ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=w3.to_checksum_address(config.CONTRACT_ADDRESS), abi=config.CONTRACT_ABI)

# --- 3. GET WALLET ADDRESS ---
# We define this early to avoid NameErrors in the pages
user_address_js = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")

# --- 4. HEADER ---
st.title(f"🏢 {config.APP_NAME}")
st.caption(f"**{config.TAGLINE}**")
st.divider()

# --- 5. SIDEBAR WALLET STATUS & NAVIGATION ---
st.sidebar.header("🔐 Wallet Status")
is_registered = False

if user_address_js:
    st.sidebar.success(f"Connected: {user_address_js[:6]}...{user_address_js[-4:]}")
    try:
        is_registered = contract.functions.registeredDonors(user_address_js).call()
        if is_registered:
            st.sidebar.info("✅ Registered Donor")
        else:
            st.sidebar.warning("⚠️ Not Registered")
    except:
        st.sidebar.error("Blockchain unreachable")
else:
    st.sidebar.error("MetaMask Not Connected")
    if st.sidebar.button("Connect Wallet"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })", key="connect_btn")

st.sidebar.divider()
pages = ["Overview", "Full About SMANO", "Donation Portal", "Logistics & Tracking", "Subscribe (R60)"]
selection = st.sidebar.radio("Go to", pages)

# --- PAGE: OVERVIEW ---
if selection == "Overview":
    st.subheader("Platform Dashboard")
    col1, col2 = st.columns(2)
    try:
        col1.metric("Batches Tracked", contract.functions.batchCount().call())
        col2.metric("Service Fee", "10%")
    except:
        st.warning("Connect to MetaMask to see metrics.")

# --- PAGE: FULL ABOUT SMANO ---
elif selection == "Full About SMANO":
    st.write("### Mission")
    st.write(config.ABOUT_MISSION)
    st.write("### The Solution")
    st.info(config.ABOUT_SOLUTION)
    st.markdown("### Ecosystem Roles")
    for role, desc in config.ABOUT_ROLES.items():
        st.write(f"**{role}:** {desc}")

# --- PAGE: DONATION PORTAL ---
elif selection == "Donation Portal":
    st.subheader("Secure Donation Portal")
    
    if not user_address_js:
        st.warning("Please connect your MetaMask wallet to proceed.")
    elif not is_registered:
        st.error("🚨 Registration Required")
        st.write("In accordance with CSR rules, you must be a registered donor to contribute.")
        if st.button("Register as Donor"):
            st.info("Please confirm the 'registerDonor' transaction in MetaMask.")
    else:
        st.success("✅ Verified Donor")
        agreed = st.checkbox("I agree to the SMANO Terms and Conditions (Compulsory)")
        
        amount = st.number_input("Amount to Donate (ETH)", min_value=0.01, step=0.01)
        if amount > 0:
            fee = amount * config.SERVICE_FEE_RATE
            net_amount = amount - fee
            st.write(f"Gross: {amount} ETH | Fee: {fee:.4f} ETH | **School Allocation: {net_amount:.4f} ETH**")
        
        if st.button("Complete Donation"):
            if not agreed:
                st.error("You must agree to the Terms and Conditions first.")
            else:
                st.info("Initiating secure donation... please check MetaMask.")

# --- PAGE: LOGISTICS & TRACKING ---
elif selection == "Logistics & Tracking":
    st.subheader("Supply Chain Tracking")
    batch_id = st.number_input("Enter Batch ID", min_value=0, step=1)
    if st.button("Track Progress"):
        st.info(f"Checking status for Batch #{batch_id} on-chain...")

# --- PAGE: SUBSCRIBE (R60) ---
elif selection == "Subscribe (R60)":
    st.subheader("Platform Support")
    st.markdown(f"## R{config.SUBSCRIPTION_FEE_ZAR} per month")
    st.write("Your subscription helps cover operating costs for the transparent supply chain.")
    if st.button("Subscribe Now"):
        st.success("Redirecting to secure payment. Thank you!")

        
          
