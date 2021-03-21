#!/bin/bash

function clean_files {
    rm -f input.txt lexical_errors.txt symbol_table.txt tokens.txt
}

samples_dir="$1"

for i in {1..10}
do
    clean_files

    test_name=T`printf "%02d" $i`
    test_dir="$samples_dir/$test_name"
    cp "$test_dir/input.txt" input.txt

    python compiler.py

    diff -Bbq lexical_errors.txt "$test_dir/lexical_errors.txt" 2> /dev/null
    if [ $? -ne 0 ]
    then
        echo "$i: WRONG -- lexical_errors"
        continue
    fi

    diff -Bbq symbol_table.txt "$test_dir/symbol_table.txt" 2> /dev/null
    if [ $? -ne 0 ]
    then
        echo "$i: WRONG -- symbol_table"
        continue
    fi

    diff -Bbq tokens.txt "$test_dir/tokens.txt" 2> /dev/null
    if [ $? -ne 0 ]
    then
        echo "$i: WRONG -- tokens"
        continue
    fi

    echo "$i: OK"
done

clean_files
