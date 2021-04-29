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

diff -Bbqi syntax_errors.txt "$test_dir/syntax_errors.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    fail "syntax_errors"
else
    success "syntax_errors"
fi

diff -Bbqi parse_tree.txt "$test_dir/parse_tree.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    fail "parse_tree"
else
    success "parse_tree"
fi
