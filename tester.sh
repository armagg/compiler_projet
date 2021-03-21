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

    echo Test \#$i
    ./single-test.sh $test_dir
    echo
done

clean_files
