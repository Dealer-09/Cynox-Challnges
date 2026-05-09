# The key is "loki" — hidden in the filename: loki_encrypted_log.txt

def vigenere_decode(text, key):
    out, ki = [], 0
    for ch in text:
        if ch.isalpha():
            base  = ord('a') if ch.islower() else ord('A')
            shift = ord(key[ki % len(key)].lower()) - ord('a')
            out.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)

encoded = open("loki_encrypted_log.txt").read().strip()
key     = "loki"   # first word of the filename
print(vigenere_decode(encoded, key))
# Output: cyn0x{v1g3n3r3_k3y_1n_pl41n_s1ght}
