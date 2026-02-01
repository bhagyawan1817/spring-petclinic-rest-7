from pathlib import Path

all_apis_file = Path("coverage/all_apis.txt")
tested_apis_file = Path("coverage/tested_apis.txt")

all_apis = set(all_apis_file.read_text().splitlines())
tested_apis = set(tested_apis_file.read_text().splitlines())

missing_apis = sorted(all_apis - tested_apis)

if missing_apis:
    print("\n❌ API COVERAGE CHECK FAILED")
    print("The following APIs are NOT covered by automation:\n")
    for api in missing_apis:
        print(f" - {api}")
    print(f"\nTotal missing APIs: {len(missing_apis)}")
    raise SystemExit(1)

print("✅ API coverage check PASSED (all APIs are tested)")
