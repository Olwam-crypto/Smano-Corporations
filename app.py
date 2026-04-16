# pip install streamlit web3 streamlit-js-eval
import streamlit as st
import os
import time
from web3 import Web3
from web3.exceptions import Web3Exception
from streamlit_js_eval import streamlit_js_eval
import config

# ==========================================
# PAGE SETUP & STYLING
# ==========================================
st.set_page_config(page_title=config.APP_NAME, layout="centered")

# Header Logic: Try loading the logo exclusively, fallback to text title.
try:
    if os.path.exists(config.LOGO_PATH):
        st.image(config.LOGO_PATH, width=200)
    else:
        st.title(config.APP_NAME)
except Exception:
    st.title(config.APP_NAME)

st.caption(f"**{config.TAGLINE}**")
st.markdown(config.DESCRIPTION)
st.divider()

# ==========================================
# BLOCKCHAIN CONNECTION SETUP
# ==========================================
# Initialize Web3 using the RPC URL provided in config
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))

# Ensure we have a valid checksum address for the contract
contract_address = w3.to_checksum_address(config.CONTRACT_ADDRESS)
contract = w3.eth.contract(address=contract_address, abi=config.CONTRACT_ABI)

# ==========================================
# METAMASK INTEGRATION (BROWSER)
# ==========================================
# We use JavaScript evaluation to passively check if the user has connected MetaMask
user_address_js = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")

user_address = None
if user_address_js:
    # Format the browser address to a safe Python format
    user_address = w3.to_checksum_address(user_address_js)

def trigger_metamask_tx(tx_data, value_in_wei=0):
    """
    Builds a transaction command and sends it to the user's browser to be signed by MetaMask.
    The private key never touches Python.
    """
    hex_value = hex(value_in_wei)
    js_code = f"""
    if (typeof window.ethereum !== 'undefined') {{
        window.ethereum.request({{
            method: 'eth_sendTransaction',
            params: [{{
                from: '{user_address}',
                to: '{contract_address}',
                data: '{tx_data}',
                value: '{hex_value}'
            }}]
        }}).then((txHash) => {{
            alert('Transaction submitted to MetaMask! Hash: ' + txHash);
        }}).catch((error) => {{
            alert('Transaction failed or cancelled: ' + error.message);
        }});
    }}
    """
    # Execute the JS snippet in the browser
    streamlit_js_eval(js_expressions=js_code, key=f"tx_{time.time()}")
    st.info("Please check your MetaMask popup to confirm the transaction.")

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.header("Navigation")
pages = ["Overview / Dashboard", "Donation Portal", "Supplier Management", "Logistics & Tracking", "Admin Settings"]
selection = st.sidebar.radio("Go to", pages)

st.sidebar.divider()
st.sidebar.subheader("Wallet Status")
if user_address:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")
else:
    st.sidebar.warning("MetaMask not connected. Please connect to interact with the platform.")
    # JavaScript to trigger the MetaMask connection popup
    if st.sidebar.button("Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })", key="connect_wallet")

# ==========================================
# PAGE 1: OVERVIEW / DASHBOARD
# ==========================================
if selection == "Overview / Dashboard":
    st.subheader("Platform Dashboard")
    
    with st.spinner("Fetching live network data..."):
        try:
            # Call read functions from the blockchain
            admin_address = contract.functions.admin().call()
            total_batches = contract.functions.batchCount().call()
            fee_percent = contract.functions.SERVICE_FEE_PERCENT().call()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Deliveries Tracked", total_batches)
            col2.metric("Platform Fee", f"{fee_percent}%")
            col3.metric("Network", "Sepolia Testnet")
            
            st.info(f"**Platform Administrator:** `{admin_address}`")
            
            # If a user is connected, look up their specific profile data
            if user_address:
                st.subheader("Your Profile Status")
                is_donor = contract.functions.registeredDonors(user_address).call()
                if is_donor:
                    st.success("You are a Registered Donor.")
                else:
                    st.warning("You are not currently registered as a Donor.")

                my_supplier_data = contract.functions.suppliers(user_address).call()
                # my_supplier_data returns a tuple: (name, country, region, companyName, status_enum, reason)
                my_status = config.SUPPLIER_STATUS_MAP.get(my_supplier_data[4], "Unknown")
                
                if my_status != "Unregistered":
                    st.info(f"**Supplier Status:** {my_status} (Company: {my_supplier_data[3]})")
                    
        except Web3Exception as e:
            st.error(f"Could not connect to the network. Error: {e}")

# ==========================================
# PAGE 2: DONATION PORTAL
# ==========================================
elif selection == "Donation Portal":
    st.subheader("Support Disadvantaged Schools")
    
    # READ: Check registration
    is_registered = False
    if user_address:
        try:
            is_registered = contract.functions.registeredDonors(user_address).call()
        except Exception:
            pass
            
    if not is_registered:
        st.warning("You must register as a donor before contributing.")
        if st.button("Register as Donor"):
            if user_address:
                # Build the transaction payload for MetaMask
                tx_data = contract.encodeABI(fn_name="registerDonor", args=[])
                trigger_metamask_tx(tx_data)
            else:
                st.error("Please connect your wallet from the sidebar first.")
    else:
        st.success("Your donor profile is active and ready.")
        
        with st.form("donation_form"):
            st.write("Make a Contribution")
            amount_eth = st.number_input("Amount (in ETH)", min_value=0.001, step=0.01)
            st.caption("A 10% service fee is automatically deducted to support platform maintenance.")
            
            submitted = st.form_submit_button("Donate Securely")
            if submitted:
                if user_address:
                    amount_wei = w3.to_wei(amount_eth, "ether")
                    tx_data = contract.encodeABI(fn_name="donate", args=[])
                    trigger_metamask_tx(tx_data, value_in_wei=amount_wei)
                else:
                    st.error("Please connect your wallet first.")

# ==========================================
# PAGE 3: SUPPLIER MANAGEMENT
# ==========================================
elif selection == "Supplier Management":
    st.subheader("Supplier Registration & Certifications")
    st.write("Join our network to provide essential learning materials and food.")
    
    with st.expander("Apply to be a Supplier", expanded=True):
        with st.form("supplier_form"):
            contact_name = st.text_input("Full Contact Name")
            company_name = st.text_input("Company Name")
            country = st.text_input("Operating Country")
            region = st.text_input("Operating Region / State")
            st.caption("All applications are reviewed by the platform administrator before approval.")
            
            if st.form_submit_button("Submit Application"):
                if user_address:
                    tx_data = contract.encodeABI(fn_name="applyAsSupplier", args=[contact_name, country, region, company_name])
                    trigger_metamask_tx(tx_data)
                else:
                    st.error("Please connect your wallet first.")

    with st.expander("Upload a New Certification"):
        with st.form("cert_form"):
            cert_type = st.text_input("Certification Type (e.g., 'Health & Safety')")
            doc_hash = st.text_input("Document Verification Hash (Bytes32)", placeholder="0x...")
            st.caption("Enter the cryptographic hash of your certification document.")
            issue_date = st.number_input("Issue Date (Unix Timestamp)", min_value=0, step=1)
            expiry_date = st.number_input("Expiry Date (Unix Timestamp)", min_value=0, step=1)
            
            if st.form_submit_button("Add Certification"):
                if user_address:
                    try:
                        # Ensure hash is properly formatted to bytes32
                        formatted_hash = Web3.to_bytes(hexstr=doc_hash) 
                        tx_data = contract.encodeABI(fn_name="addCertification", args=[cert_type, formatted_hash, int(issue_date), int(expiry_date)])
                        trigger_metamask_tx(tx_data)
                    except Exception as e:
                        st.error(f"Invalid input data: {e}")
                else:
                    st.error("Please connect your wallet first.")

# ==========================================
# PAGE 4: LOGISTICS & TRACKING
# ==========================================
elif selection == "Logistics & Tracking":
    st.subheader("Track Supply Batches")
    
    batch_id_to_check = st.number_input("Enter Delivery Batch ID to Track", min_value=0, step=1)
    if st.button("Look up Delivery"):
        with st.spinner("Querying blockchain records..."):
            try:
                batch_data = contract.functions.batches(batch_id_to_check).call()
                # batch_data tuple: (id, description, status_enum, supplier, transporter, school)
                current_status = config.ITEM_STATUS_MAP.get(batch_data[2], "Unknown")
                
                if batch_data[3] == "0x0000000000000000000000000000000000000000":
                    st.warning("No batch found with that ID.")
                else:
                    st.success(f"**Current Status:** {current_status}")
                    st.write(f"**Description:** {batch_data[1]}")
                    st.write(f"**Supplier:** `{batch_data[3]}`")
                    st.write(f"**Destination School:** `{batch_data[5]}`")
            except Exception as e:
                st.error(f"Error fetching batch: {e}")
                
    st.divider()
    st.write("Update Delivery Status (Logistics Partners Only)")
    with st.form("update_status"):
        batch_id = st.number_input("Batch ID", min_value=0, step=1)
        # We allow users to select the human-readable text, but we capture the numerical ID for the contract
        new_status_label = st.selectbox("New Status", options=list(config.ITEM_STATUS_MAP.values()))
        new_status_int = list(config.ITEM_STATUS_MAP.keys())[list(config.ITEM_STATUS_MAP.values()).index(new_status_label)]
        
        if st.form_submit_button("Update Status on Blockchain"):
            if user_address:
                tx_data = contract.encodeABI(fn_name="updateBatchStatus", args=[int(batch_id), new_status_int])
                trigger_metamask_tx(tx_data)
            else:
                st.error("Wallet not connected.")

# ==========================================
# PAGE 5: ADMIN SETTINGS
# ==========================================
elif selection == "Admin Settings":
    st.subheader("Administrator Controls")
    
    # Extra security check on UI layer
    try:
        admin_address = contract.functions.admin().call()
        if user_address and user_address != admin_address:
            st.warning("You are not the connected Administrator. Transactions submitted here will be rejected by the contract.")
    except Exception:
        pass

    with st.expander("Verify or Reject a Supplier", expanded=True):
        with st.form("verify_supplier_form"):
            target_supplier = st.text_input("Supplier Wallet Address", placeholder="0x...")
            action = st.radio("Decision", ["Approve", "Reject / Suspend"])
            reason = st.text_input("Reason (Mandatory if Rejecting)")
            
            if st.form_submit_button("Submit Decision"):
                if user_address:
                    try:
                        clean_address = w3.to_checksum_address(target_supplier)
                        approve_bool = True if action == "Approve" else False
                        tx_data = contract.encodeABI(fn_name="verifySupplier", args=[clean_address, approve_bool, reason])
                        trigger_metamask_tx(tx_data)
                    except Exception as e:
                        st.error(f"Invalid input: {e}")
                else:
                    st.error("Wallet not connected.")
