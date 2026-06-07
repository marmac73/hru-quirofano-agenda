import re

js_path = "app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Let's inspect the lines that contain "in st" or "in s.status.upper()"
# Example: "COMPLETA" in st
# We want to replace it with: st.includes("COMPLETA")
js_content_fixed = js_content

# Replace "SUBSTRING" in st -> st.includes("SUBSTRING")
pattern1 = r'"([^"]+)"\s+in\s+st'
js_content_fixed = re.sub(pattern1, r'st.includes("\1")', js_content_fixed)

# Replace "SUBSTRING" in s.status.upper() -> s.status.toUpperCase().includes("SUBSTRING")
pattern2 = r'"([^"]+)"\s+in\s+s\.status\.upper\(\)'
js_content_fixed = re.sub(pattern2, r's.status.toUpperCase().includes("\1")', js_content_fixed)

# Let's check if there are other matches
# Let's write the file back
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content_fixed)

print("JS corrections completed in app.js!")
