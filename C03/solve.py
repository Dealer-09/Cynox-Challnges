custom_decode = {
    '-': 'A',    '..-': 'B',   '...-': 'C',  '.--': 'D',
    '-..-': 'E', '-.--': 'F',  '--..': 'G',  '.-': 'H',
    '-...': 'I', '-.-.': 'J',  '-..': 'K',   '.': 'L',
    '..-.'  : 'M','--.'  : 'N', '....': 'O',  '..': 'P',
    '.---': 'Q', '-.-': 'R',   '.-..': 'S',  '--': 'T',
    '-.': 'U',   '---': 'V',   '.--.' : 'W',  '--.-': 'X',
    '.-.': 'Y',  '...': 'Z',
    '...--': '0','....-': '1', '.....': '2',  '-....': '3',
    '--...': '4','---..' : '5','----.': '6',  '-----': '7',
    '.----': '8','..---': '9',
    '..--..': '_'
}

encoded = open("asgard_transmission.txt").read().strip()
tokens = [t.strip() for t in encoded.split('|')]
decoded = ''.join(custom_decode[t] for t in tokens).lower()
print(f"cyn0x{{{decoded}}}")
# Output: cyn0x{4sg4rd_sp34ks_1n_c0d3}
