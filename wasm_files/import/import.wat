(module
  (type $t0 (func (param i32)))
  (type $t1 (func (param i32 i32)))
  (type $t2 (func (result i32)))
  (import "host" "print" (func $host.print (type $t0)))
  (import "host" "print" (func $host.print_1 (type $t1)))
  (func $test (type $t2) (result i32)
    (call $host.print
      (i32.const 100))
    (call $host.print_1
      (i32.const 200)
      (i32.const 300))
    (return
      (i32.const 1)))
  (export "test" (func $test)))
