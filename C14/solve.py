from PIL import Image
from PIL.ExifTags import TAGS

img  = Image.open("ssr_dossier.jpg")
exif = img.getexif()

print("EXIF fields:")
for tag_id, val in exif.items():
    print(f"  {TAGS.get(tag_id, tag_id):20s}: {val}")

# Step 1: Find the MD5 hash in the Make field
pw_hash = exif[271]   # Make field
print(f"\nHash found (Make): {pw_hash}")
print("Crack this MD5 hash to find the password.")
print("Hint: It's a leetspeak name from the challenge lore.")
print("Answer: cart3r  (MD5: de40c560f041031f2dc9dc4d8f4ce9c6)")

# Step 2: Use password to XOR-decrypt the flag from Software field
password = "cart3r"
enc_hex  = exif[305]   # Software field
enc_bytes = bytes.fromhex(enc_hex)

def xor_decrypt(data, key):
    return bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(data)])

flag = xor_decrypt(enc_bytes, password).decode()
print(f"\nFlag: {flag}")
# Output: cyn0x{4g3nt_c4rt3r_n3v3r_f0rg3ts}