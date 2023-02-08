
class Base:
    def hello(self):
        print(self, "original")


class Base(Base):
    def hello(self):
        print(self, "redefined")

    def orig_hell(self):
        super().hello()

b = Base()
b.hello()
b.orig_hell()
