# https://stackoverflow.com/questions/33409888/how-can-i-await-inside-future-like-objects-await/
# super annoying

# Changelog:
# 2019-07-19: well, there was still something missing from the
# initial version:
# - return values from the coroutines
# - asyncio.run() as nice 3.7 sugar
# - asyncio.create_task() - 3.7's sensible name for ensure_future
# - @asyncio.coroutine decorator on sync_await() - questionable?

import asyncio


# https://docs.python.org/3.7/library/asyncio-task.html#generator-based-coroutines
# Note: Support for generator-based coroutines is deprecated and is scheduled for removal in Python 3.10.
@asyncio.coroutine  # Not sure, if this is recommended (but 'not enforced')
def sync_await(gen):
    if hasattr(gen, '__await__'):
        # 3.7
        print('yield from gen.__await__()')
        return (yield from gen.__await__())
    else:
        # 3.6
        print('yield from gen')
        return (yield from gen)


async def coro_with_return():
    await asyncio.sleep(1)
    return 1


class Waiting:
    def __await__(self):
        # "cantrip", i.e. procedure
        print('gen = asyncio.sleep(2)')
        yield from sync_await(asyncio.sleep(2))
        print('ok')

        # function with return
        # (first version didn't have this)
        print('gen = coro_with_return()')
        result = yield from sync_await(coro_with_return())
        print('Got result:', result)

        # native function with return, a group of awaitables
        fake_future = asyncio.futures.Future()

        if hasattr(asyncio, 'create_task'):
            # 3.7
            real_task = asyncio.create_task(coro_with_return())
        else:
            # 3.6
            real_task = asyncio.ensure_future(coro_with_return())

        awaitables = [fake_future, real_task]

        print('gen = asyncio.wait(awaitables, return_when=FIRST_COMPLETED)')
        done, pending = yield from sync_await(
            asyncio.wait(awaitables, return_when=asyncio.FIRST_COMPLETED)
        )
        print(done, pending)


async def main():
    await Waiting()


if __name__ == "__main__":
    if hasattr(asyncio, 'run'):
        # 3.7
        asyncio.run(main())
    else:
        # 3.6
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
