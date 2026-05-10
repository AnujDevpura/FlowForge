import asyncio

from worker.service import worker_loop


def main():
    asyncio.run(
        worker_loop()
    )


if __name__ == "__main__":
    main()