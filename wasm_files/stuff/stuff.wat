(module
  (type $t0 (func (param i32) (result i32)))
  (type $t1 (func (param f32)))
  (type $t2 (func))
  (import "foo" "bar" (func $foo.bar (type $t1)))
  (func $e (type $t2))
  (func $f2 (type $t1) (param $p0 f32)
    (drop
      (i32.const 42)))
  (table $T0 0 1 anyfunc)
  (memory $M0 1 1)
  (export "e" (func $e))
  (start 1)
  (data (i32.const 0) "hi"))
