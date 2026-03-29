import aiohttp
import asyncio

SERVER = "https://gleaming-truth-production-ed48.up.railway.app"

async def get_sessions():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SERVER}/sessions") as resp:
            data = await resp.json()
            return data.get("sessions", [])  # FIX


async def main():
    print("🚀 WORKER START")

    while True:
        sessions = await get_sessions()
        print("sessions:", sessions)

        if not sessions:
            print("❌ No sessions found")

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
