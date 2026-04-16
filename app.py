import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config

# --- PAGE CONFIGURATION ---
# This MUST stay in app.py, never config.py
st.set_page_config(page_title=config.APP_NAME, layout="wide")

# --- HEADER SECTION ---
st.title(f"🏢 {config.APP_NAME}")
st.caption(f"**{config.TAGLINE}**")
st.divider()

# --- BLOCKCHAIN CONNECTION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=w3.to_checksum_address(config.CONTRACT_ADDRESS), abi=config.CONTRACT_ABI)

# --- SIDEBAR NAVIGATION ---
pages = ["Overview", "Full About SMANO", "Donation Portal", "Logistics & Tracking", "Subscribe (R60)"]
selection = st.sidebar.radio("Go to", pages)

if selection == "Overview":
    st.subheader("Platform Dashboard")
    col1, col2 = st.columns(2)
    try:
        col1.metric("Batches Tracked", contract.functions.batchCount().call())
        col2.metric("Service Fee", "10%")
    except:
        st.error("Blockchain Connection Error")

elif selection == "Full About SMANO":
    st.write("### Mission")
    st.write(config.ABOUT_MISSION)
    st.write("### Solution")
    st.info(config.ABOUT_SOLUTION)

elif selection == "Donation Portal":
    st.subheader("Support a School")
    amount = st.number_input("Amount (ETH)", min_value=0.01)
    if st.button("Donate"):
        st.write(f"Processing {amount} ETH (includes 10% fee)")

elif selection == "Logistics & Tracking":
    st.subheader("Real-Time Tracking")
    st.write("Enter a batch ID to see the status from Supplier to School.")

elif selection == "Subscribe (R60)":
    st.subheader("Monthly Subscription")
    st.write(f"Contribute R{config.SUBSCRIPTION_FEE_ZAR} to support the project.")
    if st.button("Subscribe"):
        st.success("Thank you!")
