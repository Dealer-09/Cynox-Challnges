import zipfile, io

# Step 1: Find and extract the ZIP hidden inside the PNG
with open("quantum_realm.png", "rb") as f:
    data = f.read()

zip_start = data.find(b'PK\x03\x04')
with zipfile.ZipFile(io.BytesIO(data[zip_start:])) as zf:
    encrypted_flag = zf.read("flag.txt").decode()
    note           = zf.read("note.txt").decode()

print("Encrypted flag:", encrypted_flag)
print("Note:", note)

# Step 2: Vigenère decrypt — key is the filename stem: "quantum_realm"
def vigenere_decrypt(text, key):
    key = key.lower()
    result, ki = [], 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord('a')
            base  = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        elif ch.isdigit():
            shift = ord(key[ki % len(key)]) - ord('a')
            result.append(str((int(ch) - shift) % 10))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)

key  = "quantum_realm"   # the filename without extension — the note hints at this
flag = vigenere_decrypt(encrypted_flag, key)
print("Flag:", flag)
# Output: cyn0x{4lw4ys_ch3ck_th3_f1l3n4m3}
