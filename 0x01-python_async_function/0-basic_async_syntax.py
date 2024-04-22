#!/usr/bin/env python3
"The basics of async"
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    "Wait for a random delay 0 - max_delay seconds and returns it"
    sec = random.uniform(0, max_delay)
    await asyncio.sleep(sec)
    return sec
