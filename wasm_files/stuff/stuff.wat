(module
  (type (;0;) (func (param i32) (result i32)))
  (type (;1;) (func (param f32)))
  (type (;2;) (func))
  (import "foo" "bar" (func (;0;) (type 1)))
  (func (;1;) (type 2))
  (func (;2;) (type 1) (param f32)
    i32.const 42
    drop)
  (table (;0;) 0 1 anyfunc)
  (memory (;0;) 1 1)
  (export "e" (func 1))
  (start 1)
  (data (i32.const 0) "hi"))
