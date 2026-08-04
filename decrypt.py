from Crypto.Cipher import AES

# =========================
# LOAD AES KEY
# =========================

with open("secret.key", "rb") as f:
    key = f.read()

# =========================
# ENCRYPTED FILE
# =========================
filename = "evidence_20260713_111212.avi.enc"

# Change this filename

# =========================
# READ ENCRYPTED DATA
# =========================

with open(filename, 'rb') as f:

    nonce = f.read(16)
    tag = f.read(16)
    ciphertext = f.read()

# =========================
# DECRYPT
# =========================

cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

data = cipher.decrypt_and_verify(ciphertext, tag)

# =========================
# SAVE DECRYPTED FILE
# =========================

output_file = "decrypted_video.avi"

with open(output_file, 'wb') as f:
    f.write(data)

print("Decryption successful")
print("Saved as:", output_file)