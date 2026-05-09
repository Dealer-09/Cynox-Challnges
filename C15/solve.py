"""
C15 Solver — Helicarrier Traffic

Steps:
1. Open helicarrier_traffic.pcap in Wireshark
2. Filter HTTP traffic → see normal S.H.I.E.L.D. web requests (decoy)
3. Filter DNS traffic: udp.port == 53
4. Notice suspicious DNS queries to *.exfil.shield-c2.net
5. Extract the hex subdomains in order and decode

AI trap: AI focuses on HTTP stream (user/password login packet is a red herring),
         never filters DNS traffic where the actual exfiltration happens.
"""

# Manual extraction (no scapy needed):
# DNS subdomains from the PCAP in order:
chunks = [
    "63796e30787b6434",
    "74345f337866316c",
    "5f316e5f646e355f",
    "7034636b3374737d"
]

flag = bytes.fromhex(''.join(chunks)).decode()
print(f"Flag: {flag}")
# Output: cyn0x{d4t4_3xf1l_1n_dn5_p4ck3ts}