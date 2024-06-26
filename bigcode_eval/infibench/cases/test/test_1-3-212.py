import re
def judge(func_name):
    f1 = getattr(M(), func_name)
    f2 = getattr(M3D(), func_name)


    x1 = re.findall('<bound method (.*?)\.{} of'.format(func_name), str(f1))[0]
    x2 = re.findall('<bound method (.*?)\.{} of'.format(func_name), str(f2))[0]
    return x1 == x2

cube = M3D().set_width(2).set_height(3).set_depth(5)
assert judge('set_width') and judge('set_height')
