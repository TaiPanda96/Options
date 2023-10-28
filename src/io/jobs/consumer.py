from asyncio import Queue, sleep
from typing import List, Dict, Callable


class Consumer:
    """

    Consumer Job Implementation

        Consumer:
        - Get jobs from queue
        - Process jobs
    """

    def __init__(
        self,
        batch: List[Dict],
        queue: Queue,
        processor: Callable,
        result_queue: Queue,
    ):
        self.batch = batch
        self.queue = queue
        self.processor = processor
        self.result_queue = result_queue

    @classmethod
    async def consumer_factory(
        cls, queue: Queue, processor: Callable, result_queue: Queue
    ):
        """
        This is a factory method that creates a consumer for the jobs.
        """
        return cls(
            batch=[],
            queue=queue,
            processor=processor,
            result_queue=result_queue,
        )

    async def consume(self, processor: Callable, result_queue: Queue, **kwargs):
        """
        This is the consumer method that gets the jobs from the queue and processes them.
        """
        while True:
            job = await self.queue.get()
            result = await processor(job, **kwargs)
            await sleep(0)

            await result_queue.put(result)

            self.queue.task_done()
