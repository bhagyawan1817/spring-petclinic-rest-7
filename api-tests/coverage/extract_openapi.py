import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:9966/petclinic")
SPEC_URL = f"{BASE_URL}/v3/api-docs"

print(f"Fetching OpenAPI spec from: {SPEC_URL}")

response = requests.get(SPEC_URL)
response.raise_for_status()

spec = response.json()
paths = spec.get("paths", {})

all_apis = set()

ALLOWED_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}

for path, methods in paths.items():
    if not path.startswith("/api/"):
        continue

    for method in methods.keys():
        method = method.upper()
        if method in ALLOWED_METHODS:
            all_apis.add(f"{method} {path}")

os.makedirs("coverage", exist_ok=True)

with open("coverage/all_apis.txt", "w") as f:
    for api in sorted(all_apis):
        f.write(api + "\n")

print(f"✅ Found {len(all_apis)} APIs from OpenAPI")
print("📄 Written to coverage/all_apis.txt")
