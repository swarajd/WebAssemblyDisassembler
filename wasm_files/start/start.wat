(module
  (type $t0 (func))
  (type $t1 (func (result i32)))
  (func $f0 (type $t0)
    (i32.store
      (i32.const 0)
      (i32.const 42)))
  (func $get (type $t1) (result i32)
    (i32.load
      (i32.const 0)))
  (memory $M0 1)
  (export "get" (func $get))
  (start 0))
