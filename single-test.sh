#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

function success {
    printf "$*: ${GREEN}OK${NC}\n"
}

function fail {
    printf "$*: ${RED}WRONG${NC}\n"
}

if [ $# -ne 1 ]
then
    echo pass the test directory addrees
    exit 1
fi

test_dir="$1"
cp "$test_dir/input.txt" input.txt

python compiler.py
./runner.exe 2> /dev/null > stdout.txt

diff -Bbqi stdout.txt "$test_dir/expected.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    fail "stdout"
else
    success "stdout"
fi
