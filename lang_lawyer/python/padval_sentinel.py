from itertools import islice, chain, repeat


def chunk_pad(it, size, padval=None):
    it = chain(iter(it), repeat(padval))
    return iter(lambda: tuple(islice(it, size)), (padval,) * size)


_no_padding = object()


def chunk(it, size, padval=_no_padding):
    if padval == _no_padding:
        it = iter(it)
        sentinel = ()
    else:
        it = chain(iter(it), repeat(padval))
        sentinel = (padval,) * size
    return iter(lambda: tuple(islice(it, size)), sentinel)


# just another SO discussion. Chunking + sentinel = no good.
print(list(chunk_pad([1, 2, None, None, 5], 2)))
