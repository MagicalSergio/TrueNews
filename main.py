import asyncio
import signal
from src.scanner.scanner_impl import ScannerImpl
import logging
import sys

sys.stdout.reconfigure(line_buffering=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler(f"logs/root.log", "+w")],
)


async def main():
    try:
        scanner = ScannerImpl()
        scanner.start()

        stop_event = asyncio.Event()

        # Обработка сигналов для корректного завершения
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)

        await stop_event.wait()  # Ждём сигнала завершения
        scanner.stop()
    except Exception as e:
        logging.critical()


if __name__ == "__main__":
    asyncio.run(main())
