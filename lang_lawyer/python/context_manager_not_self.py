class Inner:
    "Returned from Outer.__enter__, neither entered nor exited."
    def __enter__(self):
        print("Enter Inner")
        return None

    def __exit__(self, *args):
        print("Exit Inner, *args (exc_type, exc_value, traceback):", args)


class Outer:
    def __enter__(self):
        print("Enter Outer")
        return Inner()

    def __exit__(self, *args):
        print("Exit Outer, *args (exc_type, exc_value, traceback):", args)


with Outer() as ctx:
    print("  Inside Outer, ctx:", ctx)

with Inner() as ctx:
    print("  Inside Inner, will soon throw, ctx:", ctx)
    raise ValueError("Bad value")
