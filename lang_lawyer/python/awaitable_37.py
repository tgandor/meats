# https://stackoverflow.com/questions/33409888/how-can-i-await-inside-future-like-objects-await/
# super annoying

    import asyncio


    class Waiting:
        def __await__(self):
            yield from asyncio.sleep(2).__await__()
            print('ok')

    async def main():
        await Waiting()

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
