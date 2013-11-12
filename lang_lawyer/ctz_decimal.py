
def ctz_str(longint):
    manipulandum = str(longint)
    return len(manipulandum)-len(manipulandum.rstrip('0'))

def ctz_int(string):
    manipulandum = int(string)
    if not manipulandum:
        return 1
    num = 0
    while manipulandum % 10 == 0:
        num += 1
        manipulandum /= 10
    return num

if __name__ == '__main__':
    import timeit
    for test in ['"12345000000000"', '12345000000000', '25', '"25"', '1'+'0'*50, '"1'+'0'*50+'"']:
        print("ctz_str(%s):" % test)
        print(timeit.timeit('ctz_str(%s)' % test, setup="from __main__ import ctz_str"))
        print("ctz_int(%s):" % test)
        print(timeit.timeit('ctz_int(%s)' % test, setup="from __main__ import ctz_int"))

