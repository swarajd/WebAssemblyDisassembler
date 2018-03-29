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
CONTROL_FLOW_OPS = {
    0x00 : 'unreachable',
    0x01 : 'nop',
    0x02 : 'block',
    0x03 : 'loop',
    0x04 : 'if',
    0x05 : 'else',
    0x0b : 'end',
    0x0c : 'br',
    0x0d : 'bf_if',
    0x0e : 'br_table',
    0x0f : 'return'
}


"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#call-operators-described-here
"""
CALL_OPERATORS = {
    0x10 : 'call',
    0x11 : 'call_indirect'
}

"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#parametric-operators-described-here
"""
PARAMETRIC_OPERATORS = {
    0x1a : 'drop',
    0x1b : 'select'
}


"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#variable-access-described-here
"""
VARIABLE_ACCESS = {
    0x20 : 'get_local',
    0x21 : 'set_local',
    0x22 : 'tee_local',
    0x23 : 'get_global',
    0x24 : 'set_global'
}

"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#memory-related-operators-described-here
"""
MEMORY_RELATED_OPERATORS = {
    0x28 : 'i32.load',
    0x29 : 'i64.load',
    0x2a : 'f32.load',
    0x2b : 'f64.load',
    0x2c : 'i32.load8_s',
    0x2d : 'i32.load8_u',
    0x2e : 'i32.load16_s',
    0x2f : 'i32.load16_u',
    0x30 : 'i64.load8_s',
    0x31 : 'i64.load8_u',
    0x32 : 'i64.load16_s',
    0x33 : 'i64.load16_u',
    0x34 : 'i64.load32_s',
    0x35 : 'i64.load32_u',
    0x36 : 'i32.store',
    0x37 : 'i64.store',
    0x38 : 'f32.store',
    0x39 : 'f64.store',
    0x3a : 'i32.store8',
    0x3b : 'i32.store16',
    0x3c : 'i64.store8',
    0x3d : 'i64.store16',
    0x3e : 'i64.store32',
    0x3f : 'current_memory',
    0x40 : 'grow_memory'
}

"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#comparison-operators-described-here
"""
COMPARISON_OPERATORS = {
    0x45 : 'i32.eqz',
	0x46 : 'i32.eq',
	0x47 : 'i32.ne',
	0x48 : 'i32.lt_s',
	0x49 : 'i32.lt_u',
	0x4a : 'i32.gt_s',
	0x4b : 'i32.gt_u',
	0x4c : 'i32.le_s',
	0x4d : 'i32.le_u',
	0x4e : 'i32.ge_s',
	0x4f : 'i32.ge_u',
	0x50 : 'i64.eqz',
	0x51 : 'i64.eq',
	0x52 : 'i64.ne',
	0x53 : 'i64.lt_s',
	0x54 : 'i64.lt_u',
	0x55 : 'i64.gt_s',
	0x56 : 'i64.gt_u',
	0x57 : 'i64.le_s',
	0x58 : 'i64.le_u',
	0x59 : 'i64.ge_s',
	0x5a : 'i64.ge_u',
	0x5b : 'f32.eq',
	0x5c : 'f32.ne',
	0x5d : 'f32.lt',
	0x5e : 'f32.gt',
	0x5f : 'f32.le',
	0x60 : 'f32.ge',
	0x61 : 'f64.eq',
	0x62 : 'f64.ne',
	0x63 : 'f64.lt',
	0x64 : 'f64.gt',
	0x65 : 'f64.le',
	0x66 : 'f64.ge'
}

"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#numeric-operators-described-here
"""
NUMERIC_OPERATORS = {
	0x67 : 'i32.clz',
	0x68 : 'i32.ctz',
	0x69 : 'i32.popcnt',
	0x6a : 'i32.add',
	0x6b : 'i32.sub',
	0x6c : 'i32.mul',
	0x6d : 'i32.div_s',
	0x6e : 'i32.div_u',
	0x6f : 'i32.rem_s',
	0x70 : 'i32.rem_u',
	0x71 : 'i32.and',
	0x72 : 'i32.or',
	0x73 : 'i32.xor',
	0x74 : 'i32.shl',
	0x75 : 'i32.shr_s',
	0x76 : 'i32.shr_u',
	0x77 : 'i32.rotl',
	0x78 : 'i32.rotr',
	0x79 : 'i64.clz',
	0x7a : 'i64.ctz',
	0x7b : 'i64.popcnt',
	0x7c : 'i64.add',
	0x7d : 'i64.sub',
	0x7e : 'i64.mul',
	0x7f : 'i64.div_s',
	0x80 : 'i64.div_u',
	0x81 : 'i64.rem_s',
	0x82 : 'i64.rem_u',
	0x83 : 'i64.and',
	0x84 : 'i64.or',
	0x85 : 'i64.xor',
	0x86 : 'i64.shl',
	0x87 : 'i64.shr_s',
	0x88 : 'i64.shr_u',
	0x89 : 'i64.rotl',
	0x8a : 'i64.rotr',
	0x8b : 'f32.abs',
	0x8c : 'f32.neg',
	0x8d : 'f32.ceil',
	0x8e : 'f32.floor',
	0x8f : 'f32.trunc',
	0x90 : 'f32.nearest',
	0x91 : 'f32.sqrt',
	0x92 : 'f32.add',
	0x93 : 'f32.sub',
	0x94 : 'f32.mul',
	0x95 : 'f32.div',
	0x96 : 'f32.min',
	0x97 : 'f32.max',
	0x98 : 'f32.copysign',
	0x99 : 'f64.abs',
	0x9a : 'f64.neg',
	0x9b : 'f64.ceil',
	0x9c : 'f64.floor',
	0x9d : 'f64.trunc',
	0x9e : 'f64.nearest',
	0x9f : 'f64.sqrt',
	0xa0 : 'f64.add',
	0xa1 : 'f64.sub',
	0xa2 : 'f64.mul',
	0xa3 : 'f64.div',
	0xa4 : 'f64.min',
	0xa5 : 'f64.max',
	0xa6 : 'f64.copysign'
}


"""
Source: https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#conversions-described-here
"""
CONVERSIONS = {
	0xa7 : 'i32.wrap/i64',
	0xa8 : 'i32.trunc_s/f32',
	0xa9 : 'i32.trunc_u/f32',
	0xaa : 'i32.trunc_s/f64',
	0xab : 'i32.trunc_u/f64',
	0xac : 'i64.extend_s/i32',
	0xad : 'i64.extend_u/i32',
	0xae : 'i64.trunc_s/f32',
	0xaf : 'i64.trunc_u/f32',
	0xb0 : 'i64.trunc_s/f64',
	0xb1 : 'i64.trunc_u/f64',
	0xb2 : 'f32.convert_s/i32',
	0xb3 : 'f32.convert_u/i32',
	0xb4 : 'f32.convert_s/i64',
	0xb5 : 'f32.convert_u/i64',
	0xb6 : 'f32.demote/f64',
	0xb7 : 'f64.convert_s/i32',
	0xb8 : 'f64.convert_u/i32',
	0xb9 : 'f64.convert_s/i64',
	0xba : 'f64.convert_u/i64',
	0xbb : 'f64.promote/f32'
}

REINTERPRETATIONS = {
	0xbc : 'i32.reinterpret/f32',
	0xbd : 'i64.reinterpret/f64',
	0xbe : 'f32.reinterpret/i32',
	0xbf : 'f64.reinterpret/i64'
}