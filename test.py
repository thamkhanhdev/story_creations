import re
from fontTools.ttLib import TTFont

font = TTFont(r"C:\Users\khanh\Downloads\dc027189e0ba4cd.woff2")
cmap = font['cmap'].getBestCmap()

def decode_gid_text(raw_text, cmap):
    def repl(match):
        gid = int(match.group(1))
        return cmap.get(gid, f"[UNK:{gid}]")
    return re.sub(r"gid(\d+)", repl, raw_text)

raw_text = '“魔尊gid58612gid58422！”'
decoded = decode_gid_text(raw_text, cmap)
# In toàn bộ mapping
for gid, char in cmap.items():
    print(gid, "->", char)
