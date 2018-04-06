(module
  (type $t0 (func))
  (type $t1 (func (param i32)))
  (import "host" "print" (func $host.print (type $t1)))
  (func $f1 (type $t0))
  (table $T0 2 2 anyfunc)
  (memory $M0 1 1 shared)
  (global $g0 (mut i32) (i32.const 0))
  (elem (i32.const 0) $f1 $f1))
