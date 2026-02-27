#!/bin/bash

: '
ATM Test Runner Script

This script automatically executes all ATM test cases located in the
tests/inputs directory.

For each test case:
1) A temporary copy of the accounts file is created
2) The ATM program is executed using redirected input
3) Output transaction (.atf) and terminal (.out) files are generated
4) The exit status is evaluated to determine pass/fail

The script tracks total, passed, and failed tests,
and returns a non-zero exit code if any test fails.
'

# directories
INPUT_DIR="tests/inputs"
OUTPUT_ATF_DIR="tests/output/atf"
OUTPUT_TERMINAL_DIR="tests/output/terminal"
ACCOUNTS_FILE="tests/accounts/currentaccounts.txt"
TEMP_ACCOUNTS="tests/accounts/temp_currentaccounts.txt"

# color codes to make the output easier to read
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET_COLOR='\033[0m'

# variables to count test passes and fails
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

# create output directories if they don't exist
mkdir -p "$OUTPUT_ATF_DIR"
mkdir -p "$OUTPUT_TERMINAL_DIR"

echo "┌───────────────────┐"
echo "│ Running ATM Tests │"
echo "└───────────────────┘"

# loop through all .in files in inputs directory
for input_file in "$INPUT_DIR"/*.in; do
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    
    # get test name
    filename=$(basename "$input_file")
    test_name="${filename%.in}"
      
    # copy accounts file to temp location
    cp "$ACCOUNTS_FILE" "$TEMP_ACCOUNTS"
    
    # define output file paths
    output_atf="$OUTPUT_ATF_DIR/$test_name.atf"
    output_terminal="$OUTPUT_TERMINAL_DIR/$test_name.out"
    
    # run the ATM program
    python3 main.py "$TEMP_ACCOUNTS" "$output_atf" < "$input_file" > "$output_terminal" 2>&1
    exit_code=$?  # capture exit code immediately
    
    if [ $exit_code -eq 0 ]; then
        printf "[${GREEN}PASS${RESET_COLOR}] test: %s\n" "$test_name"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        printf "[${RED}FAIL${RESET_COLOR}] test: %s\n" "$test_name"
        printf "       exit code: %d\n" "$exit_code"
        printf "       output: %s\n" "$output_terminal"

        # show last 5 lines for quick debugging
        echo "       ─── last 5 lines ───"
        tail -n 5 "$output_terminal"
        echo "       ────────────────────"

        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    
    # clean up temp accounts file
    rm -f "$TEMP_ACCOUNTS"
done

echo   ""
echo   "┌───────────┬────────────┬───────────┐"
printf "│ Total: %d │ ${GREEN}Passed: %d${RESET_COLOR} │ ${RED}Failed: %d${RESET_COLOR} │\n" "$TOTAL_COUNT" "$PASS_COUNT" "$FAIL_COUNT"
echo   "└───────────┴────────────┴───────────┘"

# exit if any test failed
if [ "$FAIL_COUNT" -ne 0 ]; then
    exit 1
fi

exit 0
