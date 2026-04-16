# ==========================================
# SMANO CONFIGURATION FILE
# ==========================================
# This file stores all the settings for the app.
# It contains no active logic, only variables and data dictionaries.
# Beginners: Update these values if your contract address changes or 
# if you want to change how the text looks on the website.

# --- Application Display Text ---
APP_NAME = "SMANO"
TAGLINE = "Transparent, verifiable, and permanent supply chains for education."
DESCRIPTION = "A decentralized platform connecting donors, verified suppliers, and logistics to ensure every contribution reaches disadvantaged schools."
LOGO_PATH = "assets/logo.png" # The app will look for an image here. If it fails, it uses the APP_NAME text.

# --- Blockchain Network Settings ---
# We hardcode the Sepolia public remote procedure call (RPC) URL so the app can read from the blockchain.
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CONTRACT_ADDRESS = "0xD1eE418868CeA61E6fE6079f9E3b3990A1C116D1"

# --- Human-Readable Dictionaries ---
# The blockchain stores statuses as numbers (0, 1, 2...). 
# These dictionaries translate those numbers into plain English for the users.
SUPPLIER_STATUS_MAP = {
    0: "Unregistered",
    1: "Application Pending",
    2: "Verified & Active",
    3: "Suspended",
    4: "Application Rejected"
}

ITEM_STATUS_MAP = {
    0: "Order Received",
    1: "Being Prepared at Supplier",
    2: "In Transit",
    3: "Delivered to School",
    4: "Passed Quality Inspection",
    5: "Failed Quality Inspection"
}

# --- Contract Application Binary Interface (ABI) ---
# The ABI is the "instruction manual" that tells Python how to talk to the Solidity smart contract.
CONTRACT_ABI = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "uint256", "name": "batchId", "type": "uint256"}, {"indexed": False, "internalType": "enum SMANO.ItemStatus", "name": "status", "type": "uint8"}], "name": "BatchStatusUpdated", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "donor", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "grossAmount", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "fee", "type": "uint256"}], "name": "DonationReceived", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "supplier", "type": "address"}, {"indexed": False, "internalType": "string", "name": "name", "type": "string"}], "name": "SupplierApplied", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "supplier", "type": "address"}, {"indexed": False, "internalType": "enum SMANO.SupplierStatus", "name": "newStatus", "type": "uint8"}, {"indexed": False, "internalType": "string", "name": "reason", "type": "string"}], "name": "SupplierStatusChanged", "type": "event"},
    {"inputs": [], "name": "SERVICE_FEE_PERCENT", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "string", "name": "_type", "type": "string"}, {"internalType": "bytes32", "name": "_hash", "type": "bytes32"}, {"internalType": "uint256", "name": "_issueDate", "type": "uint256"}, {"internalType": "uint256", "name": "_expiryDate", "type": "uint256"}], "name": "addCertification", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "admin", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "string", "name": "_country", "type": "string"}, {"internalType": "string", "name": "_region", "type": "string"}, {"internalType": "string", "name": "_company", "type": "string"}], "name": "applyAsSupplier", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "batchCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "batches", "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "enum SMANO.ItemStatus", "name": "status", "type": "uint8"}, {"internalType": "address", "name": "supplier", "type": "address"}, {"internalType": "address", "name": "transporter", "type": "address"}, {"internalType": "address", "name": "destinationSchool", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "donate", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "_supplier", "type": "address"}], "name": "hasValidCertification", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "registerDonor", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "registeredDonors", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "suppliers", "outputs": [{"internalType": "string", "name": "name", "type": "string"}, {"internalType": "string", "name": "country", "type": "string"}, {"internalType": "string", "name": "region", "type": "string"}, {"internalType": "string", "name": "companyName", "type": "string"}, {"internalType": "enum SMANO.SupplierStatus", "name": "status", "type": "uint8"}, {"internalType": "string", "name": "reason", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_batchId", "type": "uint256"}, {"internalType": "enum SMANO.ItemStatus", "name": "_newStatus", "type": "uint8"}], "name": "updateBatchStatus", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "_supplier", "type": "address"}, {"internalType": "uint256", "name": "_index", "type": "uint256"}], "name": "verifyCertification", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "_supplier", "type": "address"}, {"internalType": "bool", "name": "_approve", "type": "bool"}, {"internalType": "string", "name": "_reason", "type": "string"}], "name": "verifySupplier", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"stateMutability": "payable", "type": "receive"}
]
