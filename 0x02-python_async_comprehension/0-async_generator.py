#!/usr/bin/env python3
"Async Generator"
import asyncio
import random


async def async_generator():
    "Generate 10 random floats asynchronously"
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
