
import cycl2

def dep1(n):
    if n > 0:
        print n,
        cycl2.dep2(n-1)

if __name__=='__main__':
    dep1(int(raw_input()))
