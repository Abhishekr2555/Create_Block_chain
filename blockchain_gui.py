import hashlib
import datetime as date
import streamlit as st

class Block:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha_algo = hashlib.sha256()
        sha_algo.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.prev_hash).encode('utf-8')
        )
        return sha_algo.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_first_block()]  # first block = genesis block

    def create_first_block(self):
        first_block = Block(0, date.datetime.now(), '', '0')
        return first_block

    def new_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.prev_hash = self.new_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.prev_hash != previous_block.hash:
                return False

        return True

# Initialize Streamlit session state for blockchain and validation status
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

if 'validation_status' not in st.session_state:
    st.session_state.validation_status = None

# Streamlit interface
st.set_page_config(page_title="Blockchain Demo", page_icon="🔗", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        font-size: 16px;
        cursor: pointer;
        margin: 2px;
        transition-duration: 0.4s;
    }
    .stButton>button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    .block {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: white;
        color: black; /* Text color */
    }
    .stMarkdown p {
        color: black; 
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: black; 
    }
    .custom-title {
        color: blue; 
    }
    .custom-subheader {
        color: green; 
    }
    .custom-validation {
        color: black; 
    }
    .custom-error {
        color: red; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="custom-title">🔗 Simple Blockchain Demo</h1>', unsafe_allow_html=True)

st.sidebar.header("Configuration")
num_blocks = st.sidebar.number_input('Enter the number of blocks you want to create:', min_value=1, step=1)

# Variable to store input data
block_data = []

for i in range(num_blocks):
    data = st.sidebar.text_input(f'Enter data for Transaction {i + 1}:', key=f'data_{i}')
    block_data.append(data)

if st.sidebar.button('Add Blocks'):
    for i in range(num_blocks):
        previous_hash = st.session_state.blockchain.chain[-1].hash if st.session_state.blockchain.chain else '0'
        block = Block(len(st.session_state.blockchain.chain), date.datetime.now(), block_data[i], previous_hash)
        st.session_state.blockchain.add_block(block)
    st.sidebar.success(f'{num_blocks} blocks added successfully!')

st.markdown('<h2 class="custom-subheader">Blockchain Contents</h2>', unsafe_allow_html=True)
for block in st.session_state.blockchain.chain:
    with st.expander(f'Block {block.index}', expanded=True):
        st.markdown(
            f"""
            <div class="block">
                <b>Index:</b> {block.index}<br>
                <b>Timestamp:</b> {block.timestamp}<br>
                <b>Data:</b> {block.data}<br>
                <b>Previous Hash:</b> {block.prev_hash}<br>
                <b>New Hash:</b> {block.hash}
            </div>
            """,
            unsafe_allow_html=True
        )

if st.button('Validate Blockchain'):
    if len(st.session_state.blockchain.chain) <= 1:
        st.session_state.validation_status = "no_data"
    else:
        if st.session_state.blockchain.is_valid():
            st.session_state.validation_status = "valid"
        else:
            st.session_state.validation_status = "invalid"


if st.session_state.validation_status:
    if st.session_state.validation_status == "valid":
        st.markdown('<p class="custom-validation">Blockchain is valid.</p>', unsafe_allow_html=True)
    elif st.session_state.validation_status == "invalid":
        st.markdown('<p class="custom-validation">Blockchain is not valid.</p>', unsafe_allow_html=True)
    elif st.session_state.validation_status == "no_data":
        st.markdown('<p class="custom-error">Please enter data and add blocks before validating.</p>', unsafe_allow_html=True)
