import asyncio
import aiosqlite

async def async_fetch_users():
    """Asynchronously fetch all users from the database"""
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        print("All users:")
        for row in results:
            print(row)
        return results

async def async_fetch_older_users():
    """Asynchronously fetch users older than 40 from the database"""
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        print("Users older than 40:")
        for row in results:
            print(row)
        return results

async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather"""
    print("Starting concurrent database queries...")
    
    # Run both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print(f"\nConcurrent execution completed!")
    print(f"Total users fetched: {len(all_users)}")
    print(f"Users older than 40: {len(older_users)}")

# Run the concurrent fetch
asyncio.run(fetch_concurrently())