import os
import re

TESTS_DIR = "tests"

# Regex to capture: ENDPOINT = "METHOD /path"
pattern = re.compile(r'ENDPOINT\s*=\s*["\'](.+?)["\']')

tested_apis = set()

for root, _, files in os.walk(TESTS_DIR):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                content = f.read()
                matches = pattern.findall(content)
                for match in matches:
                    tested_apis.add(match)

os.makedirs("coverage", exist_ok=True)

with open("coverage/tested_apis.txt", "w") as f:
    for api in sorted(tested_apis):
        f.write(api + "\n")

print(f"✅ Found {len(tested_apis)} tested APIs")
print("📄 Written to coverage/tested_apis.txt")
