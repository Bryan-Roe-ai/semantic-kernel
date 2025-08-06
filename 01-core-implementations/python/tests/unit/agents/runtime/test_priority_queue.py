import pytest

from semantic_kernel.agents.runtime.in_process.queue import PriorityQueue

@pytest.mark.asyncio
async def test_priority_queue_order():
    q: PriorityQueue[int] = PriorityQueue()
    await q.put(1, priority=5)
    await q.put(2, priority=1)
    await q.put(3, priority=3)

    assert await q.get() == 2
    q.task_done()
    assert await q.get() == 3
    q.task_done()
    assert await q.get() == 1
    q.task_done()
