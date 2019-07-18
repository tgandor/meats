# https://stackoverflow.com/questions/33409888/how-can-i-await-inside-future-like-objects-await/
# super annoying

import asyncio


def sync_await(gen):
    if hasattr(gen, '__await__'):
        # 3.7
        print('yield from gen.__await__()')
        yield from gen.__await__()
    else:
        # 3.6
        print('yield from gen')
        yield from gen


class Waiting:
    def __await__(self):
        yield from sync_await(asyncio.sleep(2))
        print('ok')


async def main():
    await Waiting()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
