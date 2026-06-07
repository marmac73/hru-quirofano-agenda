with open("database.js", "r", encoding="utf-8") as f:
    content = f.read()

print("Length of database.js:", len(content))
print("First 200 characters:")
print(content[:200])
print("\nLast 200 characters:")
print(content[-200:])
