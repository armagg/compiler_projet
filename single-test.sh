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

test_dir="$1"
cp "$test_dir/input.txt" input.txt

python compiler.py

diff -Bbq lexical_errors.txt "$test_dir/lexical_errors.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    fail "lexical_errors"
else
    success "lexical_errors"
fi

diff -Bbq symbol_table.txt "$test_dir/symbol_table.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    fail "symbol_table"
else
    success "symbol_table"
fi

diff -Bbq tokens.txt "$test_dir/tokens.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    fail "tokens"
else
    success "tokens"
fi
