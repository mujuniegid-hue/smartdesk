import time
from assistant import load_documents
from triage import handle_message

# Each test: (customer message, should the owner be flagged?, word expected in reply or None)
TESTS = [
    ("What time do you open?", False, "8"),
    ("Do you deliver?", False, "5,000"),
    ("How much is a battery replacement?", False, "40,000"),
    ("Do you fix laptops?", False, None),
    ("My phone is still broken after your repair! I want my money back!", True, None),
    ("Can you unlock my iCloud account?", True, None),
]

documents = load_documents()
passed = 0
skipped = 0

for message, expect_owner, keyword in TESTS:
    start = time.time()
    result = handle_message(message, documents)
    seconds = time.time() - start

    if "unavailable" in result.reason:
        print(f"SKIP  ({seconds:.1f}s) AI unavailable: {message}")
        skipped += 1
        time.sleep(2)
        continue

    ok = result.needs_owner == expect_owner
    if keyword and keyword not in result.reply:
        ok = False

    status = "PASS" if ok else "FAIL"
    print(f"{status}  ({seconds:.1f}s) {message}")
    if not ok:
        print(f"      needs_owner={result.needs_owner}, reply={result.reply}")
    else:
        passed += 1
    time.sleep(2)

print(f"\n{passed} passed, {skipped} skipped, {len(TESTS) - passed - skipped} failed")