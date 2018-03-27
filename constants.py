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