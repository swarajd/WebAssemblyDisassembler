(module
  (type $t0 (func (param f64) (result f64)))
  (func $fac (type $t0) (param $p0 f64) (result f64)
    (if $I0 (result f64)
      (f64.lt
        (get_local $p0)
        (f64.const 0x1p+0 (;=1;)))
      (then
        (f64.const 0x1p+0 (;=1;)))
      (else
        (f64.mul
          (get_local $p0)
          (call $fac
            (f64.sub
              (get_local $p0)
              (f64.const 0x1p+0 (;=1;))))))))
  (export "fac" (func $fac)))
