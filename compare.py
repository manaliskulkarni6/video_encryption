# ==========================================================
# Secure Cryptography Benchmark Dashboard
# Author : Mansi
# Part 1
# ==========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import hashlib
import base64
import time
import psutil
import os

from algorithms import *

from benchmark import *

from charts import *

from utils import *



from Crypto.Cipher import AES, DES, DES3, PKCS1_OAEP, ChaCha20
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Secure Cryptography Benchmark Dashboard",
    page_icon="🔐",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

body{
background-color:#0E1117;
}

.main{
background:#0E1117;
}

.title{
font-size:42px;
font-weight:bold;
color:#00F5D4;
text-align:center;
}

.subtitle{
font-size:20px;
color:white;
text-align:center;
}

.card{

background:#262730;
padding:15px;
border-radius:15px;

}

.metric-container{

background:#1F2937;
padding:20px;
border-radius:10px;

}

.stButton>button{

width:100%;
background:#00C49A;
color:white;
font-size:18px;
border-radius:10px;

}

</style>

""",unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
"<p class='title'>🔐 Secure Cryptography Benchmark Dashboard</p>",
unsafe_allow_html=True
)

st.markdown(
"<p class='subtitle'>AES | DES | 3DES | RSA | ChaCha20 Performance Analyzer</p>",
unsafe_allow_html=True
)

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Navigation")

menu=st.sidebar.radio(

"Select Module",

[
"Encryption",
"Benchmark",
"Charts",
"System Monitor",
"About"
]

)

# ==========================================================
# INPUT MESSAGE
# ==========================================================

message=st.text_area(

"Enter Message",

"Hello Secure Digital Evidence Management System"

)

# ==========================================================
# ALGORITHM
# ==========================================================

algorithm=st.selectbox(

"Select Algorithm",

[
"AES",
"DES",
"3DES",
"RSA",
"ChaCha20"
]

)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def bytes_to_binary(data):

    return ''.join(format(x,'08b') for x in data)

def bytes_to_hex(data):

    return data.hex()

def bytes_to_base64(data):

    return base64.b64encode(data).decode()

def sha256_hash(data):

    return hashlib.sha256(data).hexdigest()

# ==========================================================
# AES
# ==========================================================

def aes_encrypt(message):

    key=get_random_bytes(16)

    cipher=AES.new(key,AES.MODE_EAX)

    start=time.perf_counter()

    ciphertext,tag=cipher.encrypt_and_digest(message.encode())

    enc_time=(time.perf_counter()-start)*1000

    cipher2=AES.new(

        key,

        AES.MODE_EAX,

        nonce=cipher.nonce

    )

    start=time.perf_counter()

    plaintext=cipher2.decrypt(ciphertext)

    dec_time=(time.perf_counter()-start)*1000

    return{

        "Algorithm":"AES",

        "Cipher":ciphertext,

        "Plain":plaintext.decode(),

        "Key":key,

        "KeySize":128,

        "EncTime":enc_time,

        "DecTime":dec_time

    }

# ==========================================================
# DES
# ==========================================================

def des_encrypt(message):

    key=get_random_bytes(8)

    cipher=DES.new(

        key,

        DES.MODE_ECB

    )

    data=pad(message.encode(),8)

    start=time.perf_counter()

    ciphertext=cipher.encrypt(data)

    enc_time=(time.perf_counter()-start)*1000

    start=time.perf_counter()

    plaintext=unpad(

        cipher.decrypt(ciphertext),

        8

    )

    dec_time=(time.perf_counter()-start)*1000

    return{

        "Algorithm":"DES",

        "Cipher":ciphertext,

        "Plain":plaintext.decode(),

        "Key":key,

        "KeySize":56,

        "EncTime":enc_time,

        "DecTime":dec_time

    }

# ==========================================================
# 3DES
# ==========================================================

def triple_des_encrypt(message):

    key=DES3.adjust_key_parity(

        get_random_bytes(24)

    )

    cipher=DES3.new(

        key,

        DES3.MODE_ECB

    )

    data=pad(message.encode(),8)

    start=time.perf_counter()

    ciphertext=cipher.encrypt(data)

    enc_time=(time.perf_counter()-start)*1000

    start=time.perf_counter()

    plaintext=unpad(

        cipher.decrypt(ciphertext),

        8

    )

    dec_time=(time.perf_counter()-start)*1000

    return{

        "Algorithm":"3DES",

        "Cipher":ciphertext,

        "Plain":plaintext.decode(),

        "Key":key,

        "KeySize":168,

        "EncTime":enc_time,

        "DecTime":dec_time

    }

# ==========================================================
# PART 1 ENDS HERE
# ==========================================================
# ==========================================================
# RSA
# ==========================================================

def rsa_encrypt(message):

    key = RSA.generate(2048)

    public_key = key.publickey()

    cipher = PKCS1_OAEP.new(public_key)

    start = time.perf_counter()

    ciphertext = cipher.encrypt(message.encode())

    enc_time = (time.perf_counter() - start) * 1000

    cipher2 = PKCS1_OAEP.new(key)

    start = time.perf_counter()

    plaintext = cipher2.decrypt(ciphertext)

    dec_time = (time.perf_counter() - start) * 1000

    return{

        "Algorithm":"RSA",

        "Cipher":ciphertext,

        "Plain":plaintext.decode(),

        "Key":"RSA-2048",

        "KeySize":2048,

        "EncTime":enc_time,

        "DecTime":dec_time

    }

# ==========================================================
# CHACHA20
# ==========================================================

def chacha_encrypt(message):

    key = get_random_bytes(32)

    cipher = ChaCha20.new(key=key)

    start = time.perf_counter()

    ciphertext = cipher.encrypt(message.encode())

    enc_time = (time.perf_counter()-start)*1000

    cipher2 = ChaCha20.new(

        key=key,

        nonce=cipher.nonce

    )

    start = time.perf_counter()

    plaintext = cipher2.decrypt(ciphertext)

    dec_time = (time.perf_counter()-start)*1000

    return{

        "Algorithm":"ChaCha20",

        "Cipher":ciphertext,

        "Plain":plaintext.decode(),

        "Key":key,

        "KeySize":256,

        "EncTime":enc_time,

        "DecTime":dec_time

    }

# ==========================================================
# ENCRYPT BUTTON
# ==========================================================

st.divider()

encrypt_btn = st.button("🔐 Encrypt Message")

if encrypt_btn:

    if algorithm=="AES":

        result = aes_encrypt(message)

    elif algorithm=="DES":

        result = des_encrypt(message)

    elif algorithm=="3DES":

        result = triple_des_encrypt(message)

    elif algorithm=="RSA":

        result = rsa_encrypt(message)

    else:

        result = chacha_encrypt(message)

    cipher = result["Cipher"]

    plain = result["Plain"]

    enc_time = result["EncTime"]

    dec_time = result["DecTime"]

    key_size = result["KeySize"]

    algorithm_name = result["Algorithm"]

    hex_output = bytes_to_hex(cipher)

    binary_output = bytes_to_binary(cipher)

    base64_output = bytes_to_base64(cipher)

    hash_output = sha256_hash(cipher)

    st.success("Encryption Successful")

    # =============================================

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(

        "Algorithm",

        algorithm_name

    )

    col2.metric(

        "Encryption",

        f"{enc_time:.4f} ms"

    )

    col3.metric(

        "Decryption",

        f"{dec_time:.4f} ms"

    )

    col4.metric(

        "Key Size",

        f"{key_size} bits"

    )

    st.divider()

    # =============================================

    st.subheader("Original Message")

    st.code(message)

    st.subheader("Encrypted Message (HEX)")

    st.code(hex_output)

    st.subheader("Encrypted Message (Binary)")

    st.text_area(

        "",

        binary_output,

        height=180

    )

    st.subheader("Encrypted Message (Base64)")

    st.code(base64_output)

    st.subheader("SHA-256 Hash")

    st.code(hash_output)

    st.subheader("Decrypted Message")

    st.success(plain)

    st.download_button(

        "Download Encrypted HEX",

        hex_output,

        file_name="cipher_hex.txt"

    )

    st.download_button(

        "Download Binary",

        binary_output,

        file_name="cipher_binary.txt"

    )

    st.download_button(

        "Download Base64",

        base64_output,

        file_name="cipher_base64.txt"

    )

    st.download_button(

        "Download SHA256",

        hash_output,

        file_name="sha256.txt"

    )

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.divider()

st.header("System Information")

cpu = psutil.cpu_percent()

memory = psutil.virtual_memory()

disk = psutil.disk_usage('/')

c1,c2,c3 = st.columns(3)

c1.metric(

    "CPU Usage",

    f"{cpu}%"

)

c2.metric(

    "Memory Used",

    f"{memory.percent}%"

)

c3.metric(

    "Disk Used",

    f"{disk.percent}%"

)

# ==========================================================
# PART 2 COMPLETED
# ==========================================================
# ==========================================================
# PART 3
# BENCHMARK ALL ALGORITHMS
# ==========================================================

st.divider()

st.header("📊 Benchmark All Algorithms")

benchmark_btn = st.button("Run Benchmark")

if benchmark_btn:

    results=[]

    # ----------------------------
    # AES
    # ----------------------------

    aes=aes_encrypt(message)

    results.append({

        "Algorithm":"AES",

        "Encryption(ms)":aes["EncTime"],

        "Decryption(ms)":aes["DecTime"],

        "Key(bits)":128,

        "Cipher(Bytes)":len(aes["Cipher"])

    })

    # ----------------------------
    # DES
    # ----------------------------

    des=des_encrypt(message)

    results.append({

        "Algorithm":"DES",

        "Encryption(ms)":des["EncTime"],

        "Decryption(ms)":des["DecTime"],

        "Key(bits)":56,

        "Cipher(Bytes)":len(des["Cipher"])

    })

    # ----------------------------
    # 3DES
    # ----------------------------

    td=triple_des_encrypt(message)

    results.append({

        "Algorithm":"3DES",

        "Encryption(ms)":td["EncTime"],

        "Decryption(ms)":td["DecTime"],

        "Key(bits)":168,

        "Cipher(Bytes)":len(td["Cipher"])

    })

    # ----------------------------
    # RSA
    # ----------------------------

    rsa=rsa_encrypt(message)

    results.append({

        "Algorithm":"RSA",

        "Encryption(ms)":rsa["EncTime"],

        "Decryption(ms)":rsa["DecTime"],

        "Key(bits)":2048,

        "Cipher(Bytes)":len(rsa["Cipher"])

    })

    # ----------------------------
    # ChaCha20
    # ----------------------------

    cha=chacha_encrypt(message)

    results.append({

        "Algorithm":"ChaCha20",

        "Encryption(ms)":cha["EncTime"],

        "Decryption(ms)":cha["DecTime"],

        "Key(bits)":256,

        "Cipher(Bytes)":len(cha["Cipher"])

    })

    # ----------------------------

    df=pd.DataFrame(results)

    st.success("Benchmark Completed")

    st.dataframe(df,use_container_width=True)

    # ==========================================
    # FASTEST ALGORITHM
    # ==========================================

    fastest=df.loc[df["Encryption(ms)"].idxmin()]

    slowest=df.loc[df["Encryption(ms)"].idxmax()]

    c1,c2=st.columns(2)

    c1.success(

    f"""
    🏆 Fastest

    {fastest['Algorithm']}

    {fastest['Encryption(ms)']:.4f} ms
    """

    )

    c2.error(

    f"""
    🐢 Slowest

    {slowest['Algorithm']}

    {slowest['Encryption(ms)']:.4f} ms
    """

    )

    # ==========================================
    # BAR CHART
    # ==========================================

    st.subheader("Encryption Time Comparison")

    fig,ax=plt.subplots(figsize=(8,5))

    ax.bar(

        df["Algorithm"],

        df["Encryption(ms)"],

        color=["green","red","orange","purple","blue"]

    )

    ax.set_ylabel("Milliseconds")

    st.pyplot(fig)

    # ==========================================

    st.subheader("Decryption Time Comparison")

    fig,ax=plt.subplots(figsize=(8,5))

    ax.bar(

        df["Algorithm"],

        df["Decryption(ms)"],

        color=["green","red","orange","purple","blue"]

    )

    ax.set_ylabel("Milliseconds")

    st.pyplot(fig)

    # ==========================================
    # PIE CHART
    # ==========================================

    st.subheader("Encryption Time Distribution")

    fig=px.pie(

        df,

        values="Encryption(ms)",

        names="Algorithm",

        title="Encryption Time"

    )

    st.plotly_chart(fig,use_container_width=True)

    # ==========================================
    # MEMORY ESTIMATION
    # ==========================================

    memory=[]

    for algo in df["Algorithm"]:

        if algo=="AES":

            memory.append(18)

        elif algo=="DES":

            memory.append(14)

        elif algo=="3DES":

            memory.append(32)

        elif algo=="ChaCha20":

            memory.append(22)

        else:

            memory.append(110)

    df["Memory(KB)"]=memory

    st.subheader("Estimated Memory Usage")

    fig,ax=plt.subplots(figsize=(8,5))

    ax.bar(

        df["Algorithm"],

        df["Memory(KB)"]

    )

    ax.set_ylabel("KB")

    st.pyplot(fig)

    # ==========================================
    # ENERGY ESTIMATION
    # ==========================================

    energy=[]

    for t in df["Encryption(ms)"]:

        power=3.3*0.08

        energy.append(round(power*(t/1000)*1000,4))

    df["Energy(mJ)"]=energy

    st.subheader("Estimated Energy")

    fig,ax=plt.subplots(figsize=(8,5))

    ax.bar(

        df["Algorithm"],

        df["Energy(mJ)"]

    )

    ax.set_ylabel("mJ")

    st.pyplot(fig)

    # ==========================================
    # SECURITY LEVEL
    # ==========================================

    security=[]

    for algo in df["Algorithm"]:

        if algo=="DES":

            security.append("Low")

        elif algo=="3DES":

            security.append("Medium")

        elif algo=="AES":

            security.append("High")

        elif algo=="ChaCha20":

            security.append("High")

        else:

            security.append("Very High")

    df["Security"]=security

    st.subheader("Security Comparison")

    st.table(df[["Algorithm","Security"]])

    # ==========================================
    # CSV EXPORT
    # ==========================================

    csv=df.to_csv(index=False).encode()

    st.download_button(

        "📥 Download Benchmark CSV",

        csv,

        "benchmark.csv",

        "text/csv"

    )

    # ==========================================
    # SUMMARY
    # ==========================================

    st.divider()

    st.header("📑 Benchmark Summary")

    st.write(

    f"""
    ✔ Message Length : {len(message)} Characters

    ✔ Algorithms Compared : {len(df)}

    ✔ Fastest Algorithm : {fastest['Algorithm']}

    ✔ Slowest Algorithm : {slowest['Algorithm']}

    ✔ Lowest Memory Usage : {df.loc[df['Memory(KB)'].idxmin(),'Algorithm']}

    ✔ Lowest Estimated Energy : {df.loc[df['Energy(mJ)'].idxmin(),'Algorithm']}
    """

    )

    st.success("Benchmark Completed Successfully")

# ==========================================================
# END OF PART 3
# ==========================================================