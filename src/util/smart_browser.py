from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext
from playwright.async_api._context_manager import PlaywrightContextManager
import asyncio
import random
import logging
from src.util.create_logger import get_logger
from pyvirtualdisplay import Display


class SmartBrowser:
    _playwright_cm: PlaywrightContextManager
    _playwright: Playwright
    _browser: Browser
    _context: BrowserContext
    _semaphore: asyncio.Semaphore
    _display: Display
    _logger = get_logger("smart_browser")

    async def __aenter__(self):
        self._semaphore = asyncio.Semaphore(1)

        self._display = Display(size=(1920, 1080))
        self._display.start()
        
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._context.close()
        await self._browser.close()
        await self._playwright.stop()
        self._display.stop()

    async def get(self, url: str):
        async with self._semaphore:
            try:
                logging.info(f"Request: {url}")
                await asyncio.sleep(random.uniform(1, 3))
                return await self._page.goto(url)
            except Exception:
                logging.error(f"Request failed: {url}")
                self._logger.error(f"Error while requesting: {url}", exc_info=True)
