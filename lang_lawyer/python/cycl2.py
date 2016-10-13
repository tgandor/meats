
import cycl1

def dep2(n):
    if n > 0:
        print n,
        cycl1.dep1(n-1)

if __name__=='__main__':
    dep2(int(raw_input()))

