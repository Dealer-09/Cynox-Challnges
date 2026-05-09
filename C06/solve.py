from PIL import Image
from PIL.ExifTags import TAGS

img  = Image.open("shield_dossier.jpg")
exif = img.getexif()

print("All EXIF fields:")
for tag_id, val in exif.items():
    print(f"  {TAGS.get(tag_id, tag_id):25s}: {val}")

# Flag is split across three fields — in order:
# Artist (315) + Make (271) + Software (305)
flag = exif[315] + exif[271] + exif[305]
print(f"\nFlag: {flag}")
# Output: cyn0x{3x1f_t3lls_4ll_s3cr3ts}
