import asyncio


async def main():
    for i in range(10):
        print(i)
        asyncio.sleep(1)


asyncio.run(main())
