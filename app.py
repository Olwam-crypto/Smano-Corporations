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
# 1. First, define the variable by running the JavaScript evaluator
user_address_js = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")

# 2. Then, you can use it in your sidebar or pages
# (The rest of your code follows below...)
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

# ==========================================
# PAGE: DONATION PORTAL
# ==========================================
elif selection == "Donation Portal":
    st.subheader("Secure Donation Portal")
    st.write("In accordance with SMANO rules, donors must be registered with CSR before contributing.")

    if not user_address_js:
        st.warning("Please connect your MetaMask wallet to verify your registration status.")
    else:
        # Check if the connected address is registered in the smart contract
        is_registered = contract.functions.registeredDonors(user_address_js).call()

        if not is_registered:
            st.error("🚨 You are not registered as a donor yet.")
            st.info("Registration is compulsory to ensure CSR compliance and transparency.")
            if st.button("Register Now"):
                # This calls the registerDonor function from your ABI
                st.info("Please confirm the registration transaction in MetaMask...")
                # Note: In a full app, you'd send the transaction here via web3.js/eval
        else:
            st.success("✅ Donor Identity Verified (Registered with CSR)")
            
            with st.expander("Terms and Conditions", expanded=False):
                st.write("Agreeing to terms after downloading the app is compulsory for accountability.")
                agreed = st.checkbox("I agree to the SMANO Terms and Conditions")

            amount = st.number_input("Amount to Donate (ETH)", min_value=0.01, step=0.01)
            
            if amount > 0:
                fee = amount * config.SERVICE_FEE_RATE
                net_amount = amount - fee
                st.write(f"**Gross Donation:** {amount} ETH")
                st.write(f"**10% Service Fee:** {fee:.4f} ETH")
                st.success(f"**Net funds allocated to schools:** {net_amount:.4f} ETH")

            if st.button("Complete Donation"):
                if not agreed:
                    st.error("You must agree to the Terms and Conditions to proceed.")
                else:
                    st.info("Opening MetaMask for secure donation...")
elif selection == "Logistics & Tracking":
    st.subheader("Real-Time Tracking")
    st.write("Enter a batch ID to see the status from Supplier to School.")

elif selection == "Subscribe (R60)":
    st.subheader("Monthly Subscription")
    st.write(f"Contribute R{config.SUBSCRIPTION_FEE_ZAR} to support the project.")
    if st.button("Subscribe"):
        st.success("Thank you!")
