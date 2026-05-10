import asyncio

from scheduler.service import scheduler_loop


def main():
    asyncio.run(
        scheduler_loop()
    )


if __name__ == "__main__":
    main()