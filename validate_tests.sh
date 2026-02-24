#!/bin/bash

# directories
OUTPUT_ATF_DIR="tests/output/atf"
OUTPUT_TERMINAL_DIR="tests/output/terminal"
EXPECTED_ATF_DIR="tests/expected/atf"
EXPECTED_TERMINAL_DIR="tests/expected/terminal"

# color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET_COLOR='\033[0m'

# .ATF FILES
# transaction file counters
ATF_PASS_COUNT=0
ATF_FAIL_COUNT=0
ATF_TOTAL_COUNT=0

echo "┌──────────────────────────┐"
echo "│ Validating Transactions  │"
echo "└──────────────────────────┘"

# check all .atf files
for actual_file in "$OUTPUT_ATF_DIR"/*.atf; do
    ATF_TOTAL_COUNT=$((ATF_TOTAL_COUNT + 1))

    # get test name
    filename=$(basename "$actual_file")
    test_name="${filename%.atf}"
    expected_file="$EXPECTED_ATF_DIR/$filename"

    # compare files
    if diff -q "$actual_file" "$expected_file" > /dev/null 2>&1; then
        printf "[${GREEN}PASS${RESET_COLOR}] test: %s\n" "$test_name"
        ATF_PASS_COUNT=$((ATF_PASS_COUNT + 1))
    else
        printf "[${RED}FAIL${RESET_COLOR}] test: %s\n" "$test_name"
        echo "       expected: $expected_file"
        echo "       actual:   $actual_file"
        echo "       ─── diff (first 10 lines) ───"
        # unified diff is way easier to read
        diff -u "$actual_file" "$expected_file" | head -n 10
        echo "       ───────────────────────────"
        ATF_FAIL_COUNT=$((ATF_FAIL_COUNT + 1))
    fi
done

echo "┌───────────┬────────────┬───────────┐"
printf "│ Total: %d │ ${GREEN}Passed: %d${RESET_COLOR} │ ${RED}Failed: %d${RESET_COLOR} │\n" \
    "$ATF_TOTAL_COUNT" "$ATF_PASS_COUNT" "$ATF_FAIL_COUNT"
echo "└───────────┴────────────┴───────────┘"

# .OUT FILES
# terminal output file counters
OUT_PASS_COUNT=0
OUT_FAIL_COUNT=0
OUT_TOTAL_COUNT=0

echo ""
echo "┌────────────────────────────┐"
echo "│ Validating Terminal Output │"
echo "└────────────────────────────┘"

# check all .out files
for actual_file in "$OUTPUT_TERMINAL_DIR"/*.out; do
    OUT_TOTAL_COUNT=$((OUT_TOTAL_COUNT + 1))
    
    # get test name
    filename=$(basename "$actual_file")
    test_name="${filename%.out}"
    expected_file="$EXPECTED_TERMINAL_DIR/$filename"

    if diff -q "$actual_file" "$expected_file" > /dev/null 2>&1; then
        printf "[${GREEN}PASS${RESET_COLOR}] test: %s\n" "$test_name"
        OUT_PASS_COUNT=$((OUT_PASS_COUNT + 1))
    else
        printf "[${RED}FAIL${RESET_COLOR}] test: %s\n" "$test_name"
        echo "       expected: $expected_file"
        echo "       actual:   $actual_file"
        echo "       ─── diff (first 10 lines) ───"
        # unified diff is way easier to read
        diff -u "$actual_file" "$expected_file" | head -n 10
        echo "       ───────────────────────────"
        OUT_FAIL_COUNT=$((OUT_FAIL_COUNT + 1))
    fi
done

echo "┌───────────┬────────────┬───────────┐"
printf "│ Total: %d │ ${GREEN}Passed: %d${RESET_COLOR} │ ${RED}Failed: %d${RESET_COLOR} │\n" \
    "$OUT_TOTAL_COUNT" "$OUT_PASS_COUNT" "$OUT_FAIL_COUNT"
echo "└───────────┴────────────┴───────────┘"

# exit if any test failed
if [ "$ATF_FAIL_COUNT" -ne 0 ] || [ "$OUT_FAIL_COUNT" -ne 0 ]; then
    exit 1
fi

exit 0