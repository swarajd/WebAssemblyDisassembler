md = """| `i32.reinterpret/f32` | `0xbc` | | |
| `i64.reinterpret/f64` | `0xbd` | | |
| `f32.reinterpret/i32` | `0xbe` | | |
| `f64.reinterpret/i64` | `0xbf` | | |""".split("\n")

for line in md:
    parts = line.split("|")
    hex_ = parts[2].replace(' ', '').replace('`', '')
    name_ = parts[1].replace(' ', '').replace('`', '')
    print("\t{} : '{}',".format(hex_, name_))