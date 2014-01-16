
def dep1(n):
    from circ2 import dep2
    if n > 0:
        print n,
        dep2(n-1)

if __name__=='__main__':
    dep1(int(raw_input()))
