#!/bin/sh
tests=(
    "element"
    "empty"
    "emptymemorydata"
    "factorial"
    "global"
    "import"
    "simple"
    "start"
    "stuff"
)

for test in "${tests[@]}"; do
    echo "Running $test"
    python3.6 main.py ./wasm_files/${test}/${test}.wasm
    echo ""
done
