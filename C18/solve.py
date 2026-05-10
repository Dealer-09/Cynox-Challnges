"""
C18 Solver — Triskelion Logs

Parse the XML event log and find the flag.

AI trap: AI searches for event IDs 4624 (logon), 4648 (explicit creds),
         4625 (failed logon) — all present as decoys.
         The flag is in event ID 4698 (scheduled task creation),
         hidden in the TaskContent Arguments field.

Grep approach:
  grep -i "4698" shield_security_logs.xml
  grep -i "cyn0x" shield_security_logs.xml

Python approach:
"""
import xml.etree.ElementTree as ET

tree = ET.parse("shield_security_logs.xml")
root = tree.getroot()
ns   = "http://schemas.microsoft.com/win/2004/08/events/event"

for event in root.findall(f"{{{ns}}}Event"):
    eid = event.find(f".//{{{ns}}}EventID")
    if eid is not None and eid.text == "4698":
        print(f"[!] Suspicious Event ID 4698 — Scheduled Task Created")
        for data in event.findall(f".//{{{ns}}}Data"):
            if data.get("Name") == "TaskContent":
                content = data.text
                import re
                flag = re.search(r'cyn0x\{[^}]+\}', content)
                if flag:
                    print(f"Flag: {flag.group()}")

# Output: cyn0x{sch3dul3d_t4sk_p3rs1st3nc3_d3t3ct3d}