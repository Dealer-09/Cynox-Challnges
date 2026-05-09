# The flag is hidden as whitespace binary between the visible memo lines
# space = 0, tab = 1, each character = 8 bits = one line

with open("stark_memo.txt", 'r') as f:
    lines = f.read().split('\n')

# Extract lines made entirely of spaces and tabs (exactly 8 chars = 1 byte)
ws_lines = [l for l in lines if l and all(c in ' \t' for c in l) and len(l) == 8]

flag = ''
for line in ws_lines:
    bits = ''.join('1' if c == '\t' else '0' for c in line)
    flag += chr(int(bits, 2))

print(flag)
# Output: cyn0x{wh1t3sp4c3_1s_n0t_3mpty}