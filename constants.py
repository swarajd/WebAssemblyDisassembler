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

END_OPCODE = 0x0b

"""
Source: https://github.com/WebAssembly/website/blob/d7592a9b46729d1a76e72f73624fbe8bd5ad1caa/docs/design/BinaryEncoding.md#high-level-structure
"""
SECTION_IDS = {
    'type'       : 1,
    'import'     : 2,
    'function'   : 3,
    'table'      : 4,
    'memory'     : 5,
    'global'     : 6,
    'export'     : 7,
    'start'      : 8,
    'element'    : 9,
    'code'       : 10,
    'data'       : 11
}

"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#control-flow-operators-described-here
"""
OPCODES = {
    0x00 : ('unreachable', 'None'),
    0x01 : ('nop', 'None'),
    0x02 : ('block', 'block_type'),
    0x03 : ('loop', 'block_type'),
    0x04 : ('if', 'block_type'),
    0x05 : ('else', 'None'),
    0x0b : ('end', 'None'),
    0x0c : ('br', 'relative_depth.varuint32'),
    0x0d : ('br_if', 'relative_depth.varuint32'),
    0x0e : ('br_table', 'seebelow'),
    0x0f : ('return', 'None'),
    0x10 : ('call', 'function_index.varuint32'),
    0x11 : ('call_indirect', 'type_index.varuint32,reserved.varuint1'),
    0x1a : ('drop', 'None'),
    0x1b : ('select', 'None'),
    0x20 : ('get_local', 'local_index.varuint32'),
    0x21 : ('set_local', 'local_index.varuint32'),
    0x22 : ('tee_local', 'local_index.varuint32'),
    0x23 : ('get_global', 'global_index.varuint32'),
    0x24 : ('set_global', 'global_index.varuint32'),
    0x28 : ('i32.load', 'memory_immediate'),
    0x29 : ('i64.load', 'memory_immediate'),
    0x2a : ('f32.load', 'memory_immediate'),
    0x2b : ('f64.load', 'memory_immediate'),
    0x2c : ('i32.load8_s', 'memory_immediate'),
    0x2d : ('i32.load8_u', 'memory_immediate'),
    0x2e : ('i32.load16_s', 'memory_immediate'),
    0x2f : ('i32.load16_u', 'memory_immediate'),
    0x30 : ('i64.load8_s', 'memory_immediate'),
    0x31 : ('i64.load8_u', 'memory_immediate'),
    0x32 : ('i64.load16_s', 'memory_immediate'),
    0x33 : ('i64.load16_u', 'memory_immediate'),
    0x34 : ('i64.load32_s', 'memory_immediate'),
    0x35 : ('i64.load32_u', 'memory_immediate'),
    0x36 : ('i32.store', 'memory_immediate'),
    0x37 : ('i64.store', 'memory_immediate'),
    0x38 : ('f32.store', 'memory_immediate'),
    0x39 : ('f64.store', 'memory_immediate'),
    0x3a : ('i32.store8', 'memory_immediate'),
    0x3b : ('i32.store16', 'memory_immediate'),
    0x3c : ('i64.store8', 'memory_immediate'),
    0x3d : ('i64.store16', 'memory_immediate'),
    0x3e : ('i64.store32', 'memory_immediate'),
    0x3f : ('current_memory', 'reserved.varuint1'),
    0x40 : ('grow_memory', 'reserved.varuint1'),
    0x41 : ('i32.const', 'value.varint32'),
    0x42 : ('i64.const', 'value.varint64'),
    0x43 : ('f32.const', 'value.uint32'),
    0x44 : ('f64.const', 'value.uint64'),
    0x45 : ('i32.eqz', 'None'),
    0x46 : ('i32.eq', 'None'),
    0x47 : ('i32.ne', 'None'),
    0x48 : ('i32.lt_s', 'None'),
    0x49 : ('i32.lt_u', 'None'),
    0x4a : ('i32.gt_s', 'None'),
    0x4b : ('i32.gt_u', 'None'),
    0x4c : ('i32.le_s', 'None'),
    0x4d : ('i32.le_u', 'None'),
    0x4e : ('i32.ge_s', 'None'),
    0x4f : ('i32.ge_u', 'None'),
    0x50 : ('i64.eqz', 'None'),
    0x51 : ('i64.eq', 'None'),
    0x52 : ('i64.ne', 'None'),
    0x53 : ('i64.lt_s', 'None'),
    0x54 : ('i64.lt_u', 'None'),
    0x55 : ('i64.gt_s', 'None'),
    0x56 : ('i64.gt_u', 'None'),
    0x57 : ('i64.le_s', 'None'),
    0x58 : ('i64.le_u', 'None'),
    0x59 : ('i64.ge_s', 'None'),
    0x5a : ('i64.ge_u', 'None'),
    0x5b : ('f32.eq', 'None'),
    0x5c : ('f32.ne', 'None'),
    0x5d : ('f32.lt', 'None'),
    0x5e : ('f32.gt', 'None'),
    0x5f : ('f32.le', 'None'),
    0x60 : ('f32.ge', 'None'),
    0x61 : ('f64.eq', 'None'),
    0x62 : ('f64.ne', 'None'),
    0x63 : ('f64.lt', 'None'),
    0x64 : ('f64.gt', 'None'),
    0x65 : ('f64.le', 'None'),
    0x66 : ('f64.ge', 'None'),
    0x67 : ('i32.clz', 'None'),
    0x68 : ('i32.ctz', 'None'),
    0x69 : ('i32.popcnt', 'None'),
    0x6a : ('i32.add', 'None'),
    0x6b : ('i32.sub', 'None'),
    0x6c : ('i32.mul', 'None'),
    0x6d : ('i32.div_s', 'None'),
    0x6e : ('i32.div_u', 'None'),
    0x6f : ('i32.rem_s', 'None'),
    0x70 : ('i32.rem_u', 'None'),
    0x71 : ('i32.and', 'None'),
    0x72 : ('i32.or', 'None'),
    0x73 : ('i32.xor', 'None'),
    0x74 : ('i32.shl', 'None'),
    0x75 : ('i32.shr_s', 'None'),
    0x76 : ('i32.shr_u', 'None'),
    0x77 : ('i32.rotl', 'None'),
    0x78 : ('i32.rotr', 'None'),
    0x79 : ('i64.clz', 'None'),
    0x7a : ('i64.ctz', 'None'),
    0x7b : ('i64.popcnt', 'None'),
    0x7c : ('i64.add', 'None'),
    0x7d : ('i64.sub', 'None'),
    0x7e : ('i64.mul', 'None'),
    0x7f : ('i64.div_s', 'None'),
    0x80 : ('i64.div_u', 'None'),
    0x81 : ('i64.rem_s', 'None'),
    0x82 : ('i64.rem_u', 'None'),
    0x83 : ('i64.and', 'None'),
    0x84 : ('i64.or', 'None'),
    0x85 : ('i64.xor', 'None'),
    0x86 : ('i64.shl', 'None'),
    0x87 : ('i64.shr_s', 'None'),
    0x88 : ('i64.shr_u', 'None'),
    0x89 : ('i64.rotl', 'None'),
    0x8a : ('i64.rotr', 'None'),
    0x8b : ('f32.abs', 'None'),
    0x8c : ('f32.neg', 'None'),
    0x8d : ('f32.ceil', 'None'),
    0x8e : ('f32.floor', 'None'),
    0x8f : ('f32.trunc', 'None'),
    0x90 : ('f32.nearest', 'None'),
    0x91 : ('f32.sqrt', 'None'),
    0x92 : ('f32.add', 'None'),
    0x93 : ('f32.sub', 'None'),
    0x94 : ('f32.mul', 'None'),
    0x95 : ('f32.div', 'None'),
    0x96 : ('f32.min', 'None'),
    0x97 : ('f32.max', 'None'),
    0x98 : ('f32.copysign', 'None'),
    0x99 : ('f64.abs', 'None'),
    0x9a : ('f64.neg', 'None'),
    0x9b : ('f64.ceil', 'None'),
    0x9c : ('f64.floor', 'None'),
    0x9d : ('f64.trunc', 'None'),
    0x9e : ('f64.nearest', 'None'),
    0x9f : ('f64.sqrt', 'None'),
    0xa0 : ('f64.add', 'None'),
    0xa1 : ('f64.sub', 'None'),
    0xa2 : ('f64.mul', 'None'),
    0xa3 : ('f64.div', 'None'),
    0xa4 : ('f64.min', 'None'),
    0xa5 : ('f64.max', 'None'),
    0xa6 : ('f64.copysign', 'None'),
    0xa7 : ('i32.wrap/i64', 'None'),
    0xa8 : ('i32.trunc_s/f32', 'None'),
    0xa9 : ('i32.trunc_u/f32', 'None'),
    0xaa : ('i32.trunc_s/f64', 'None'),
    0xab : ('i32.trunc_u/f64', 'None'),
    0xac : ('i64.extend_s/i32', 'None'),
    0xad : ('i64.extend_u/i32', 'None'),
    0xae : ('i64.trunc_s/f32', 'None'),
    0xaf : ('i64.trunc_u/f32', 'None'),
    0xb0 : ('i64.trunc_s/f64', 'None'),
    0xb1 : ('i64.trunc_u/f64', 'None'),
    0xb2 : ('f32.convert_s/i32', 'None'),
    0xb3 : ('f32.convert_u/i32', 'None'),
    0xb4 : ('f32.convert_s/i64', 'None'),
    0xb5 : ('f32.convert_u/i64', 'None'),
    0xb6 : ('f32.demote/f64', 'None'),
    0xb7 : ('f64.convert_s/i32', 'None'),
    0xb8 : ('f64.convert_u/i32', 'None'),
    0xb9 : ('f64.convert_s/i64', 'None'),
    0xba : ('f64.convert_u/i64', 'None'),
    0xbb : ('f64.promote/f32', 'None'),
    0xbc : ('i32.reinterpret/f32', 'None'),
    0xbd : ('i64.reinterpret/f64', 'None'),
    0xbe : ('f32.reinterpret/i32', 'None'),
    0xbf : ('f64.reinterpret/i64', 'None'),
}