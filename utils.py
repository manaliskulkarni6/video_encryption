"""
=========================================================
utils.py
Utility Functions
=========================================================
"""

import hashlib
import base64
import pandas as pd
from datetime import datetime
import os

# ==========================================================
# SHA-256 HASH
# ==========================================================

def generate_sha256(data):

    if isinstance(data, str):
        data = data.encode()

    return hashlib.sha256(data).hexdigest()


# ==========================================================
# MD5 HASH (Optional)
# ==========================================================

def generate_md5(data):

    if isinstance(data, str):
        data = data.encode()

    return hashlib.md5(data).hexdigest()


# ==========================================================
# HEX CONVERSION
# ==========================================================

def bytes_to_hex(data):

    return data.hex()


# ==========================================================
# BINARY CONVERSION
# ==========================================================

def bytes_to_binary(data):

    return ''.join(format(byte, '08b') for byte in data)


# ==========================================================
# BASE64 CONVERSION
# ==========================================================

def bytes_to_base64(data):

    return base64.b64encode(data).decode()


# ==========================================================
# CURRENT TIMESTAMP
# ==========================================================

def get_timestamp():

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==========================================================
# FILE NAME WITH TIMESTAMP
# ==========================================================

def generate_filename(prefix="report", extension=".csv"):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{prefix}_{timestamp}{extension}"


# ==========================================================
# SAVE BENCHMARK CSV
# ==========================================================

def save_csv(df, filename=None):

    if filename is None:
        filename = generate_filename("benchmark", ".csv")

    df.to_csv(filename, index=False)

    return filename


# ==========================================================
# SAVE TEXT FILE
# ==========================================================

def save_text(content, filename):

    with open(filename, "w", encoding="utf-8") as file:

        file.write(content)

    return filename


# ==========================================================
# SAVE HEX FILE
# ==========================================================

def save_hex(cipher_bytes, filename="cipher_hex.txt"):

    with open(filename, "w") as file:

        file.write(bytes_to_hex(cipher_bytes))

    return filename


# ==========================================================
# SAVE BINARY FILE
# ==========================================================

def save_binary(cipher_bytes, filename="cipher_binary.txt"):

    with open(filename, "w") as file:

        file.write(bytes_to_binary(cipher_bytes))

    return filename


# ==========================================================
# SAVE BASE64 FILE
# ==========================================================

def save_base64(cipher_bytes, filename="cipher_base64.txt"):

    with open(filename, "w") as file:

        file.write(bytes_to_base64(cipher_bytes))

    return filename


# ==========================================================
# FILE SIZE
# ==========================================================

def get_file_size(data):

    return len(data)


# ==========================================================
# ESTIMATED ENERGY
# Formula:
# Energy = Voltage × Current × Time
# ==========================================================

def estimate_energy(time_ms,
                    voltage=3.3,
                    current=0.08):

    time_sec = time_ms / 1000

    energy = voltage * current * time_sec

    return round(energy * 1000, 4)


# ==========================================================
# ESTIMATED MEMORY
# ==========================================================

def estimate_memory(algorithm):

    memory = {

        "AES":18,
        "DES":14,
        "3DES":32,
        "RSA":120,
        "ChaCha20":22

    }

    return memory.get(algorithm,0)


# ==========================================================
# SECURITY LEVEL
# ==========================================================

def security_level(algorithm):

    levels = {

        "AES":"High",

        "DES":"Low",

        "3DES":"Medium",

        "RSA":"Very High",

        "ChaCha20":"High"

    }

    return levels.get(algorithm,"Unknown")


# ==========================================================
# PERFORMANCE SCORE
# ==========================================================

def performance_score(enc_time):

    score = 100 / (enc_time + 0.01)

    return round(score,2)


# ==========================================================
# CREATE RESULTS DIRECTORY
# ==========================================================

def create_report_folder():

    folder = "reports"

    if not os.path.exists(folder):

        os.makedirs(folder)

    return folder


# ==========================================================
# BENCHMARK SUMMARY
# ==========================================================

def benchmark_summary(df):

    fastest = df.loc[df["Encryption Time"].idxmin()]

    slowest = df.loc[df["Encryption Time"].idxmax()]

    summary = {

        "Fastest":fastest["Algorithm"],

        "Slowest":slowest["Algorithm"],

        "Average Encryption":

        round(df["Encryption Time"].mean(),4),

        "Average Decryption":

        round(df["Decryption Time"].mean(),4)

    }

    return summary


# ==========================================================
# END
# ==========================================================