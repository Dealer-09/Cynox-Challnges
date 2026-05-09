import base64

data = "ZDc5N2M2YzY0MzMzMjdmNTQ3MDNlNmY1NDMyNzQ2OTc4NmY1YzY5NjQzODZiNzg3MDNlNjk3MzY="

# Step 1: base64 decode
step1 = base64.b64decode(data).decode()

# Step 2: reverse the string
step2 = step1[::-1]

# Step 3: hex decode
flag = bytes.fromhex(step2).decode()
print(flag)
# Output: cyn0x{h4il_hydr4_n0t_r34lly}
