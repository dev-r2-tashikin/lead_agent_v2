import asyncio

async def main():
    async for  i in range(100):
        print(i)


asyncio.run(main())