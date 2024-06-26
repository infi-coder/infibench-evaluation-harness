
def f(hour, mins, dura):
    time_hour = (hour + dura//60 + (mins+ dura%60)//60) % 24
    time_min = (mins+ dura%60)%60
    return str(time_hour) + ":" + str(time_min)

def assertEqual(a, b):
    a1, a2 = a.split(':')
    b1, b2 = b.split(':')
    a1, a2, b1, b2 = int(a1), int(a2), int(b1), int(b2)
    return (a1 == b1) and (a2 == b2)

assert assertEqual(f(1, 30, 30), computeEndTime(1, 30, 30))

assert assertEqual(f(12, 59, 2), computeEndTime(12, 59, 2))

assert assertEqual(f(23, 59, 2), computeEndTime(23, 59, 2))

assert assertEqual(f(23, 58, 1), computeEndTime(23, 58, 1))