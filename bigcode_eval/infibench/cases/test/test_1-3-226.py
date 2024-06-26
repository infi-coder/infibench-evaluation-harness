

def f(s):
    return s.split("_", 1)[-1]

assert f("a_b_c") == splitOne("a_b_c")
assert f("a_b_c_d") == splitOne("a_b_c_d")
assert f("a") == splitOne("a")
assert f("aabb") == splitOne("aabb")
assert f("aaaa_bb") == splitOne("aaaa_bb")