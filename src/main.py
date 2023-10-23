"""
Async io setup
"""
import asyncio

async def main():
    """
    This is the main function.
    """
    print("Hello ...")
    await asyncio.sleep(1)
    print("... World!")

asyncio.run(main())
