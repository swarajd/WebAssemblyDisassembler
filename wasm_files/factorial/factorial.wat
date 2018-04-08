(module
  (type (;0;) (func (param f64) (result f64)))
  (func (;0;) (type 0) (param f64) (result f64)
    get_local 0
    f64.const 0x1p+0 (;=1;)
    f64.lt
    if (result f64)  ;; label = @1
      f64.const 0x1p+0 (;=1;)
    else
      get_local 0
      get_local 0
      f64.const 0x1p+0 (;=1;)
      f64.sub
      call 0
      f64.mul
    end)
  (export "fac" (func 0)))
