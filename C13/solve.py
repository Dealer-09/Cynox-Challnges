import base64, codecs

data = open("vision_fragment.txt").read().strip()

# Decode chain (reverse of encoding):
# Step 1: Reverse the string
# Step 2: ROT13
# Step 3: Base32 decode
# Step 4: Hex decode

s1 = data[::-1]
s2 = codecs.encode(s1, 'rot_13')
s3 = base64.b32decode(s2).decode()
s4 = bytes.fromhex(s3).decode()
print(s4)
# Output: cyn0x{m1nd_st0n3_3nc0d1ng_ch41n}