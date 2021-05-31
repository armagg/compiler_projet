#!/bin/bash

function clean_files {
    rm -f input.txt lexical_errors.txt symbol_table.txt tokens.txt
    rm -f parse_tree.txt syntax_errors.txt
}

if [ $# -ne 1 ]
then
    echo pass the tests root addrees
    exit 1
fi

samples_dir="$1"

for test_dir in "$samples_dir"/T*
do
    clean_files

    test_name=`basename $test_dir`

    echo Test $test_name
    ./single-test.sh $test_dir
    echo
done

clean_files
