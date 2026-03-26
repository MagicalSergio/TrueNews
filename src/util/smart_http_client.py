from httpx import AsyncClient
import asyncio
import random
from icecream import ic


USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
    # Mobile Android
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung Galaxy S23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
]


class SmartHttpClient(AsyncClient):
    def __init__(
        self,
        *,
        auth=None,
        params=None,
        headers=None,
        cookies=None,
        verify=True,
        cert=None,
        http1=True,
        http2=False,
        proxy=None,
        mounts=None,
        follow_redirects=False,
        event_hooks=None,
        base_url="",
        transport=None,
        trust_env=True,
        default_encoding="utf-8",
    ):
        super().__init__(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            proxy=proxy,
            mounts=mounts,
            follow_redirects=follow_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            transport=transport,
            trust_env=trust_env,
            default_encoding=default_encoding,
        )

        self.semaphore = asyncio.Semaphore()

    async def get(
        self,
        url,
    ):
        async with self.semaphore:
            await asyncio.sleep(random.uniform(1, 3))
            return await super().get(
                url,
                headers=[
                    ["X-Forwarded-For", f"{self._generate_ip()}"],
                    ["User-Agent", f"{self._random_ua()}"],
                ],
                follow_redirects=True,
            )

    def _generate_ip(self):
        while True:
            sections = [random.randint(0, 255) for _ in range(4)]

            # Исключаем приватные и зарезервированные диапазоны
            first = sections[0]
            if first == 0:  # 0.0.0.0/8
                continue
            if first == 10:  # 10.0.0.0/8 (приватная)
                continue
            if first == 127:  # 127.0.0.0/8 (loopback)
                continue
            if first == 169 and sections[1] == 254:  # 169.254.0.0/16 (link-local)
                continue
            if first == 172 and 16 <= sections[1] <= 31:  # 172.16.0.0/12 (приватная)
                continue
            if first == 192 and sections[1] == 168:  # 192.168.0.0/16 (приватная)
                continue
            if first >= 224:  # Multicast и зарезервированные
                continue

            return ".".join(map(str, sections))

    def _random_ua(self):
        return random.choice(USER_AGENTS)