#!/bin/bash

test_dir="$1"
cp "$test_dir/input.txt" input.txt

python compiler.py

diff -Bbq lexical_errors.txt "$test_dir/lexical_errors.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    echo "lexical_errors: WRONG"
else
    echo "lexical_errors: OK"
fi

diff -Bbq symbol_table.txt "$test_dir/symbol_table.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    echo "symbol_table: WRONG"
else
    echo "symbol_table: OK"
fi

diff -Bbq tokens.txt "$test_dir/tokens.txt" 2>&1 > /dev/null
if [ $? -ne 0 ]
then
    echo "tokens: WRONG"
else
    echo "tokens: OK"
fi
