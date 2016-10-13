
class Holder(object):
    def __init__(self, something):
        self._held = something

    @property
    def held(self):
        return self._held

h = Holder(42)

print h.held  # 42
# print h.held() # TypeError: 'int' object is not callable
