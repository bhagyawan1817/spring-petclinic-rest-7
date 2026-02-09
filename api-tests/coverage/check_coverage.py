from pathlib import Path

all_apis = set(Path("coverage/all_apis.txt").read_text().splitlines())
tested_apis = set(Path("coverage/tested_apis.txt").read_text().splitlines())

missing_apis = sorted(all_apis - tested_apis)

report_file = Path("coverage/api_coverage_report.txt")

with report_file.open("w") as f:
    if missing_apis:
        f.write("API COVERAGE CHECK FAILED\n\n")
        f.write("The following APIs are NOT covered by automation:\n\n")
        for api in missing_apis:
            f.write(f"- {api}\n")
        f.write(f"\nTotal missing APIs: {len(missing_apis)}\n")
    else:
        f.write("API COVERAGE CHECK PASSED\n")

if missing_apis:
    print("\n❌ API COVERAGE CHECK FAILED")
    print(report_file.read_text())
    raise SystemExit(1)

print("✅ API COVERAGE CHECK PASSED")