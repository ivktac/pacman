#!/bin/bash

output_file="output.txt"

if [ -f $output_file ]; then
    rm $output_file
fi

find src -type f -name '*.py' -exec cat {} + >> "$output_file"

echo "All .py files have been concatenated into $output_file"