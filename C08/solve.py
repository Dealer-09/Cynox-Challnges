def decode(text, rot=19):
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord('a') if ch.islower() else ord('A')
            out.append(chr((ord(ch) - base + (26 - rot)) % 26 + base))
        elif ch.isdigit():
            out.append(str(9 - int(ch)))   # reverse: 9-d
        else:
            out.append(ch)
    return ''.join(out)

encoded = open("hydra_communique.txt").read().strip()
print(decode(encoded))
# Output: cyn0x{r0m4n_c1ph3r_1snt_s4f3}
