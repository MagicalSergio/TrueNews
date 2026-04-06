from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext
from playwright.async_api._context_manager import PlaywrightContextManager
import asyncio


class SmartBrowser:
    _playwright_cm: PlaywrightContextManager
    _playwright: Playwright
    _browser: Browser
    _context: BrowserContext
    _semaphore = asyncio.Semaphore()

    async def __aenter__(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        self._context = await self._browser.new_context()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._context.close()
        await self._browser.close()
        await self._playwright.stop()

    async def get(self, url: str):
        async with self._semaphore:
            page = await self._context.new_page()
            return await page.goto(url)
