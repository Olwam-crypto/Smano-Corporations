# ==========================================
# SMANO CONFIGURATION FILE
# ==========================================

APP_NAME = "SMANO"
TAGLINE = "Transparent, verifiable, and permanent supply chains for education."
DESCRIPTION = "A decentralized platform connecting donors, verified suppliers, and logistics to ensure every donation is accounted for."

# --- Blockchain Network Settings ---
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CONTRACT_ADDRESS = "0xD1eE418868CeA61E6fE6079f9E3b3990A1C116D1"

# --- Financial Rules ---
SERVICE_FEE_RATE = 0.10  # 10% as specified in documentation
SUBSCRIPTION_FEE_ZAR = 60.00

# --- Human-Readable Maps ---
SUPPLIER_STATUS_MAP = {0: "Unregistered", 1: "Applied", 2: "Verified", 3: "Suspended", 4: "Rejected"}
ITEM_STATUS_MAP = {0: "Order Received", 1: "At Supplier", 2: "In Transit", 3: "Delivered", 4: "Passed Quality", 5: "Failed Quality"}

# --- Content from SMANO Documentation ---
ABOUT_MISSION = (
    "Our research has highlighted critical issues regarding the lack of infrastructure and basic necessities "
    "for children in disadvantaged schools. Many donations do not reach their destination due to misuse or poor management."
)

ABOUT_SOLUTION = (
    "SMANO addresses these problems by creating a transparent, trackable donation supply chain system. "
    "Every donation creates an indelible mark on the blockchain, creating a paper trail "
    "that allows donors to see exactly how their money is being used."
)

ABOUT_ROLES = {
    "Admin": "Deploys contract and performs necessary verification of suppliers and transporters.",
    "Suppliers": "Certified providers of food and necessities.",
    "Transporter": "Logistics companies shipping goods while recording details in real-time.",
    "Schools": "Confirm delivery and perform quality inspections on received materials.",
    "Donors": "Provide funds for learning materials and food vouchers (Must be CSR registered)."
}

# --- Contract ABI ---
CONTRACT_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"batchId","type":"uint256"},{"indexed":False,"internalType":"enum SMANO.ItemStatus","name":"status","type":"uint8"}],"name":"BatchStatusUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"donor","type":"address"},{"indexed":False,"internalType":"uint256","name":"grossAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"DonationReceived","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"supplier","type":"address"},{"indexed":False,"internalType":"string","name":"name","type":"string"}],"name":"SupplierApplied","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"supplier","type":"address"},{"indexed":False,"internalType":"enum SMANO.SupplierStatus","name":"newStatus","type":"uint8"},{"indexed":False,"internalType":"string","name":"reason","type":"string"}],"name":"SupplierStatusChanged","type":"event"},{"inputs":[],"name":"SERVICE_FEE_PERCENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_type","type":"string"},{"internalType":"bytes32","name":"_hash","type":"bytes32"},{"internalType":"uint256","name":"_issueDate","type":"uint256"},{"internalType":"uint256","name":"_expiryDate","type":"uint256"}],"name":"addCertification","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_country","type":"string"},{"internalType":"string","name":"_region","type":"string"},{"internalType":"string","name":"_company","type":"string"}],"name":"applyAsSupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"batchCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"batches","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"description","type":"string"},{"internalType":"enum SMANO.ItemStatus","name":"status","type":"uint8"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"transporter","type":"address"},{"internalType":"address","name":"destinationSchool","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"donate","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_supplier","type":"address"}],"name":"hasValidCertification","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"registerDonor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"registeredDonors","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"suppliers","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"country","type":"string"},{"internalType":"string","name":"region","type":"string"},{"internalType":"string","name":"companyName","type":"string"},{"internalType":"enum SMANO.SupplierStatus","name":"status","type":"uint8"},{"internalType":"string","name":"reason","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_batchId","type":"uint256"},{"internalType":"enum SMANO.ItemStatus","name":"_newStatus","type":"uint8"}],"name":"updateBatchStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_supplier","type":"address"},{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"verifyCertification","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_supplier","type":"address"},{"internalType":"bool","name":"_approve","type":"bool"},{"internalType":"string","name":"_reason","type":"string"}],"name":"verifySupplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
