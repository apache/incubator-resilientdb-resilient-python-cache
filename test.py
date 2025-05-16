import asyncio
from resilient_python_cache import ResilientPythonCache, MongoConfig, ResilientDBConfig

async def main():
    mongo_config = MongoConfig(
        uri="xxxx",
        db_name="resdb-cache",
        collection_name="resdb-collection"
    )
        
    resilient_db_config = ResilientDBConfig(
        base_url="resilientdb://localhost:18000",
        http_secure=True,
        ws_secure=True
    )

    cache = ResilientPythonCache(mongo_config, resilient_db_config)

    cache.on("connected", lambda: print("WebSocket connected."))
    cache.on("data", lambda new_blocks: print("Received new blocks:", new_blocks))
    cache.on("error", lambda error: print("Error:", error))
    cache.on("closed", lambda: print("Connection closed."))

    try:
        await cache.initialize()
        print("Synchronization initialized.")

        try:
            await asyncio.Future()  # Run indefinitely
        except asyncio.CancelledError:
            pass

    except Exception as error:
        print("Error during sync initialization:", error)
    finally:
        await cache.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user")