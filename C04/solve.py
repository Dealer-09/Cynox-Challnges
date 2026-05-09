from PIL import Image

img  = Image.open("surveillance_log.png")
pix  = list(img.getdata())
bits = [(p[0] & 1) for p in pix]

out = []
for i in range(0, len(bits) - 7, 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | bits[i + j]  # MSB-first — NOT the default
    if byte == 0:
        break
    out.append(chr(byte))

print(''.join(out))
# Output: cyn0x{n4t4sh4_s33s_4ll}
