# https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#language-types
LANGUAGE_TYPES = {
    0x7f : 'i32',
    0x7e : 'i64',
    0x7d : 'f32',
    0x7c : 'f64',
    0x70 : 'anyfunc',
    0x60 : 'func',
    0x40 : 'pseudo_type'
}

"""
A single-byte unsigned integer indicating the kind of definition being
imported/exported or defined:
Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#external_kind
"""
EXTERNAL_KIND_TABLE = {
    0 : 'function',
    1 : 'table',
    2 : 'memory',
    3 : 'global'
}

"""
These operators have an immediate operand of their associated type which is produced as their result value.
All possible values of all types are supported (including NaN values of all possible bit patterns).
Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#constants-described-here
"""
CONSTANTS = {
    0x41 : 'i32.const',
    0x42 : 'i64.const',
    0x43 : 'f32.const',
    0x44 : 'f64.const',
}