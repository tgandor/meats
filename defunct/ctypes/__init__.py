
class FakeCDLL(object):
    def LoadLibrary(self, library):
		raise OSError

cdll = FakeCDLL()
