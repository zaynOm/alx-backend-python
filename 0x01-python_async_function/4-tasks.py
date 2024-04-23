#!/usr/bin/env python3
"Tasks"
from typing import List

task_wait_random = __import__("3-tasks").wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    "Call task_wait_random n times with the specified max_delay"
    res = [await task_wait_random(max_delay) for _ in range(n)]
    return sorted(res)
