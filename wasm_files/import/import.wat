(module
  (type (;0;) (func (param i32)))
  (type (;1;) (func (param i32 i32)))
  (type (;2;) (func (result i32)))
  (import "host" "print" (func (;0;) (type 0)))
  (import "host" "print" (func (;1;) (type 1)))
  (func (;2;) (type 2) (result i32)
    i32.const 100
    call 0
    i32.const 200
    i32.const 300
    call 1
    i32.const 1
    return)
  (export "test" (func 2)))
